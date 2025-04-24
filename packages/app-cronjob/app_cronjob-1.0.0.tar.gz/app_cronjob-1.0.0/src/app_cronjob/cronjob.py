"""Python implementation of Perl App::Cronjob wrapper
This copies all the behavior of the Perl package so it can be used as a drop-in replacement.

Changes:
* lock-dir option
* logging output format change
* Email header ID
"""

import getpass
import hashlib
import logging
import mailbox
import os
import re
import shlex
import socket
import smtplib
import subprocess
import textwrap
from contextlib import contextmanager
from datetime import datetime
from email.message import EmailMessage
from enum import Enum

import click

from filelock import Timeout as LockTimeout, FileLock


class CronJob:
    """Main implementation of cronjob"""

    def __init__(self, **kwargs) -> None:
        """Initialize class and sanity check

        Command Line Arguments:
        command, subject, rcpt, errors_only, sender, job_name, timeout, exit_code, ignore_errors,
        email_header, temp_ignore_lock_errors, lock_dir, lock, mail_transport, smtp_server,
        verbose, shell
        """
        log_level = logging.WARNING
        if kwargs.get('verbose') > 1:
            log_level = logging.DEBUG
        elif kwargs.get('verbose') > 0:
            log_level = logging.INFO
        logging.basicConfig(level=log_level)
        self.log = logging.getLogger(__name__)

        # Command Input and validation
        self.command = self._validate_command(kwargs.get('command'))
        self.log.debug(shlex.split(self.command))
        self.subject = kwargs.get('subject') or self.command
        self.rcpt = kwargs.get('rcpt') or self._get_default_recipient()
        self.errors_only = kwargs.get('errors_only')
        self.shell = kwargs.get('shell')
        self.sender = kwargs.get('sender') or self._get_default_sender()
        self.job_name = self._validate_job_name(kwargs.get('job_name'))
        self.timeout = kwargs.get('timeout')
        self.ignore_errors = [CronJobErrorType(x) for x in kwargs.get('ignore_errors')]
        self.email_headers = self._validate_email_headers(kwargs.get('email_header'))
        self.temp_ignore_lock_errors = kwargs.get('temp_ignore_lock_errors')
        self.lockfile_dir = kwargs.get('lock_dir') or self._get_default_lockfile_dir()
        self.use_lock = kwargs.get('lock')
        self.mail_transport = CronJobMailTransportType(kwargs.get('mail_transport'))
        self.smtp_server = kwargs.get('smtp_server') or self._get_default_smtp_server()
        self.exit_code = [0] + list(kwargs.get('exit_code'))

        # Calculated Values
        self.job_id = kwargs.get('job_name') or hashlib.sha256(self.subject.encode()).hexdigest()
        self.irt_header = f'<{self.job_id}@{socket.getfqdn()}>'

        # Change logger to use job_id
        self.log.debug(self.__dict__)
        self.log = logging.getLogger(f'{__name__}:{self.job_id}')
        # self.log.debug(self.__dict__)

        # Other validation
        if self.temp_ignore_lock_errors and CronJobErrorType.LOCK in self.ignore_errors:
            raise click.BadOptionUsage('temp-ignore-lock-errors', '--temp-ignore-lock-errors and --ignore-errors=lock are incompatible')

    @contextmanager
    def acquire_lock(self):
        """
        Detect if an an instance with the label is already running, globally
        at the operating system level.
        """
        if self.use_lock:
            lock_name = os.path.join(self.lockfile_dir, f"cronjob.{self.job_id}")
            file_lock = FileLock(lock_name, blocking=False)
            try:
                with file_lock:
                    lock_stat = os.stat(lock_name)
                    self.lock_acquired_at = datetime.fromtimestamp(lock_stat.st_ctime)
                    yield file_lock

            except LockTimeout:
                lock_stat = os.stat(lock_name)
                self.lock_acquired_at = datetime.fromtimestamp(lock_stat.st_ctime)
                raise CronJobException(f'An instance of this script is already running or the lock can not be acquired. Lockfile created {lock_stat.st_ctime}', CronJobErrorType.LOCK) from None

        else:
            self.lock_acquired_at = datetime.now()
            yield None

    def _validate_command(self, command: str) -> str:
        """Check that command exists and is executable"""
        if os.path.isabs(command):
            return command
            # It would be nice to validate that the command exists during setup, but this
            # doesn't work on Windows/MinGW because
            # `/bin/sleep 2`` becomes `C:/Program Files/Git/usr/bin/sleep 2`
            # if os.path.exists(command) and os.access(os.path.abspath(command), os.X_OK):
            #     return command
            # else:
            #     exe = command.split(' ')[0]
            #     path = shutil.which(exe)
            #     self.log.debug(f'Found path {path} for command {exe} from ')

        raise click.BadOptionUsage('command', 'Command should be an absolute path')

    def _get_default_sender(self) -> str:
        """Get default sender if none was specified"""
        username = getpass.getuser()
        hostname = socket.getfqdn()
        return f'"cron/{hostname}" <{username}@{hostname}>'

    def _get_default_recipient(self) -> list:
        """Get default recipient if none was specified"""
        if 'MAILTO' in os.environ:
            mailto = os.environ.get('MAILTO')
            self.log.debug(f'Setting recipients from env: {mailto}')
            return [email.strip() for email in mailto.split(',')]
        return ['root']

    def _validate_email_headers(self, email_headers):
        """Validate email headers that can be overridden

        Valid:
            X-Me: ABC
            X-My:DEF
            XForce123:G#ff24
            blah = HJ
            foo=d24fv=4f2=f24fc::2q4ce
            a=b
        Invalid:
            1one=2two
            foobar
            444
        """
        regex = re.compile(r'^(?P<key>[A-Za-z][\w\-]*)(?:\s?[=:]\s?)(?P<value>.+)$')
        headers = set()
        for item in email_headers:
            match = regex.fullmatch(item)
            if match:
                key = match.group('key')
                value = match.group('value')
                if key.lower() in ['to', 'from', 'subject']:
                    raise click.BadOptionUsage('email-header', f'Header {item} can not replace a built-in')
                headers.add({'key': key, 'value': value})
            else:
                raise click.BadOptionUsage('email-header', f'Invalid header {item}')
        return headers

    def _validate_job_name(self, job_name) -> str | None:
        """Check that job_name is a string"""
        if job_name:
            regex = re.compile(r'^[-_A-Za-z0-9]+$')
            matches = regex.match(job_name)
            if matches:
                return matches.group()
            raise click.BadOptionUsage('job-name', 'Invalid job name')
        return None

    def _get_default_lockfile_dir(self) -> str:
        """Get directory for lock file"""
        if 'APP_CRONJOB_LOCKDIR' in os.environ:
            return os.environ.get('APP_CRONJOB_LOCKDIR')
        return '/tmp'

    def _get_default_smtp_server(self):
        """Localhost or Maildir"""
        match self.mail_transport:
            case CronJobMailTransportType.SMTP:
                return 'localhost'
            case CronJobMailTransportType.MAILDIR:
                return os.path.join(os.getcwd(), 'Maildir')
            case CronJobMailTransportType.LOG | CronJobMailTransportType.STDOUT:
                pass
            case _:
                raise click.BadOptionUsage('smtp-server', 'We could not determine how to send your message. Please use the --smtp-server option.')

    def send_email_report(self, execution_time: int, status: int, failure_type: Enum, stdout: str = None, stderr: str = None) -> None:
        """Send email report for job"""

        message_body = textwrap.dedent(f"""\
        Command: {self.command}
        Time   : {execution_time}
        Status : {status}
        """)

        if failure_type:
            message_body += textwrap.dedent(f"""\
            Failed : {failure_type.value}
            """)

        message_body += textwrap.dedent(f"""\

        Output :

        {stdout or '(no output)'}
        """)

        if stderr:
            message_body += textwrap.dedent(f"""\

            Errors :

            {stderr}
            """)

        msg = EmailMessage()
        msg['Subject'] = self.subject if failure_type == CronJobErrorType.NONE else f'FAIL ({failure_type.value}): {self.subject}'
        msg['From'] = self.sender
        msg['To'] = self.rcpt
        msg['In-Reply-To'] = self.irt_header
        msg['Auto-Submitted'] = 'auto-generated'
        for h in self.email_headers:
            msg.add_header(h['key'], h['value'])
        msg.set_content(message_body)

        if not self.mail_transport == CronJobMailTransportType.LOG:
            self.log.debug(msg)
        match self.mail_transport:
            case CronJobMailTransportType.LOG:
                self.log.info(msg)
            case CronJobMailTransportType.STDOUT:
                print(msg)
            case CronJobMailTransportType.SMTP:
                s = smtplib.SMTP(self.smtp_server)
                s.send_message(msg)
                s.quit()
            case CronJobMailTransportType.MAILDIR:
                self.log.warning('Maildir support has not been tested.')
                maildir = mailbox.Maildir(self.smtp_server)
                maildir.add(msg)

    def run(self):
        """Actually execute the job"""
        send_email = False
        failure_type = CronJobErrorType.NONE
        status = None
        stdout = None
        stderr = None

        self.run_started_at = datetime.now()
        try:
            with self.acquire_lock():
                self.log.debug(f'Trying to run {self.command}. Shell mode: {self.shell}')
                result = subprocess.run(self.command, capture_output=True, check=True, timeout=self.timeout, shell=self.shell, text=True)
                exec_time_taken = datetime.now() - self.run_started_at

                status = result.returncode
                has_output = len(result.stdout) > 0 or len(result.stderr) > 0
                if has_output and not self.errors_only:
                    send_email = True
                stdout = result.stdout
                stderr = result.stderr
                self.log.debug(f'Job completed with status {status} after {exec_time_taken}')

        except subprocess.CalledProcessError as e:
            now = datetime.now()
            exec_time_taken = now - self.run_started_at
            status = e.returncode
            if e.returncode in self.exit_code:
                """Expected exit code is not an error and doesn't change email status"""
                self.log.debug(f'Ignoring exitcode {e.returncode}')
                self.log.debug(f'Job completed with status {status} after {exec_time_taken}')
            else:
                """Unexpected exit code is an error and can change email status"""
                self.log.error(f'Process returned exit code {e.returncode}')
                failure_type = CronJobErrorType.EXITCODE
                if CronJobErrorType.EXITCODE not in self.ignore_errors:
                    send_email = True

        except subprocess.TimeoutExpired:
            now = datetime.now()
            exec_time_taken = now - self.run_started_at
            failure_type = CronJobErrorType.TIMEOUT
            if CronJobErrorType.TIMEOUT not in self.ignore_errors:
                send_email = True
            # TODO
        except CronJobException as e:
            now = datetime.now()
            exec_time_taken = now - self.run_started_at
            lock_time_taken = now - self.lock_acquired_at
            failure_type = CronJobErrorType(e.error_type)
            self.log.debug(f'Got error {e.error_type}')
            if e.error_type in self.ignore_errors:
                self.log.debug(f'Ignoring error {e.error_type}')
                pass
            elif self.temp_ignore_lock_errors:
                if e.error_type == CronJobErrorType.LOCK and \
                        self.lock_acquired_at and \
                        lock_time_taken.seconds < self.temp_ignore_lock_errors:
                    self.log.debug(f'Ignoring lock timeout: {lock_time_taken.seconds} < {self.temp_ignore_lock_errors}')
                else:
                    failure_type = CronJobErrorType.OLD_LOCKFILE
                    send_email = True
            else:
                send_email = True

        if send_email:
            self.send_email_report(exec_time_taken, status=status, failure_type=failure_type, stdout=stdout, stderr=stderr)


class ChoiceableEnum(Enum):
    @classmethod
    def choices(cls):
        choice_list = list(map(lambda x: x.value, filter(lambda x: x.value is not None, cls)))
        return choice_list


class CronJobErrorType(ChoiceableEnum):
    NONE = None
    LOCK = "lock"
    LOCKFILE = "lockfile"
    TIMEOUT = "timeout"
    EXITCODE = "exitcode"
    OLD_LOCKFILE = "old_lockfile"


class CronJobMailTransportType(ChoiceableEnum):
    SMTP = "smtp"
    MAILDIR = "maildir"
    LOG = "log"
    STDOUT = "stdout"


class CronJobException(Exception):
    def __init__(self, message, error_type: CronJobErrorType, exit_code: int = None):
        super().__init__(message)
        self.error_type = error_type


@click.command(context_settings={'show_default': True, 'max_content_width': 240})
@click.option('-c', '--command', help='Command to run', required=True)
@click.option('-s', '--subject', 'subject', help='Subject of email to send (defaults to command)')
@click.option('-r', '--rcpt', help='recipient of mail; may be given many times. Otherwise, checks MAILTO environment variable. Defaults to root.', multiple=True)
@click.option('-E', '--errors-only', help='do not send mail if exit code 0, even with output', default=False, is_flag=True)
@click.option('-C', '--exit-code', help="Exit codes considered not errors (0 is always on this list)", default=[], type=int, multiple=True)
@click.option('-f', '--sender', help='sender for message')
@click.option('-j', '--job-name', help='job name; used for locking if given')
@click.option('-t', '--timeout', help='fail if the child has not completed within n seconds', type=int)
@click.option('--ignore-errors', help='error types to ignore when determining whether to send email (like: lock)', default=[], type=click.Choice(CronJobErrorType.choices()), multiple=True)
@click.option('--email-header', help='add header to the report email (example: --email-header=X-Me=ABC --email-header="X-My: App")', default=[], multiple=True)
@click.option('--temp-ignore-lock-errors', help='failure to lock only signals an error after this long', type=int)
@click.option('--lock/--no-lock', help='lock this job', default=True)
@click.option('--lock-dir', help='Lockfile location. Checks APP_CRONJOB_LOCKDIR, defaults to /tmp')
@click.option('--mail-transport', type=click.Choice(CronJobMailTransportType.choices()), default=CronJobMailTransportType.SMTP)
@click.option('--smtp-server', help='Set SMTP server (for Maildir location if using that transport type)')
@click.option('--shell', help='DANGEROUS: use shell executor', default=False, is_flag=True)
@click.option('-v', '--verbose', help='specify multiple times for more verbosity', count=True)
def cli(command, subject, rcpt, errors_only, sender, job_name, timeout, exit_code, ignore_errors, email_header, temp_ignore_lock_errors, lock_dir, lock, mail_transport, smtp_server, verbose, shell):
    cronjob = CronJob(**locals())
    return cronjob.run()
