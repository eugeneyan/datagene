"""
Email class for sending emails
To run:
cd ~/eugeneyan/kaggle/eutils
python -m eutils.utils.util_email
"""
import smtplib
import time
from email import utils
from email.mime.text import MIMEText

from eutils import config


class SMTPConnection(object):
    """
    SMTP Connection Object
    """

    def __init__(self, host, port=0, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = None

    def __enter__(self):
        """
        Enter SMTP connection
        :return:
        """
        self.conn = smtplib.SMTP(host=self.host, port=self.port)
        if self.user:
            self.conn.ehlo()
            self.conn.starttls()
            self.conn.ehlo()
            self.conn.login(user=self.user, password=self.password)
        return self.conn

    def __exit__(self, _type, value, trackback):
        """
        Exit SMTP connection
        :return:
        """
        if self.conn:
            self.conn.quit()


class Email(object):
    """
    Email Object
    """

    def __init__(self, **config):
        self.verbose = config.get('verbose', True)

        self.host = config['host']
        self.port = int(config.get('port', 0))
        self.user = config.get('user', None)
        self.password = config.get('password', None)

        self.from_addr = config.get('from', '')
        self.to_addrs = config.get('to', [])
        self.cc_addrs = config.get('cc', [])

        self.content_type = config.get('content_type', 'plain')

    # pylint: disable=C0301
    def send(self, subject='', content='', from_addr=None, to_addrs=None, cc_addrs=None, content_type=None):
        """
        Sends email
        :param subject: email subject
        :param content: content (can be HTML)
        :param from_addr: email address to send from
        :param to_addrs: email address to send to
        :param cc_addrs: email address to cc
        :param content_type:
        :return: None
        """

        from_addr = from_addr or self.from_addr
        to_addrs = to_addrs or self.to_addrs
        cc_addrs = cc_addrs or self.cc_addrs
        content_type = content_type or self.content_type

        if isinstance(to_addrs, (str, unicode)):
            to_addrs = [to_addrs]
        assert type(to_addrs in (list, set, tuple))

        msg = MIMEText(content, content_type)
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addrs)
        if cc_addrs:
            msg['CC'] = ', '.join(cc_addrs)
        msg['Subject'] = subject
        msg['Date'] = utils.formatdate(timeval=time.time(), localtime=True)  # Local
        if self.verbose:
            print msg

        with SMTPConnection(self.host, self.port, self.user, self.password) as s:
            s.sendmail(from_addr, to_addrs, msg.as_string())


def send_email(subject, content, to, user_email=config.MY_EMAIL, user_password=config.MY_EMAIL_PW):
    """
    Wrapper for Email class to send email
    :param subject: email subject
    :param content: content (can be HTML)
    :param to: email address to send to

    :param user_email: email address to end from
    :param user_password: password of email address to send from
    :return: None
    """
    user = user_email
    password = user_password
    e = Email(host='smtp.gmail.com', port=587, user=user, password=password)
    e.send(subject, content, user, to)


if __name__ == '__main__':
    # pylint: disable=C0301
    # send_email(subject='test2', content='test_content', to=['eugene.yan@lazada.com'])
    send_email(subject='[eutils] eutils email test succeeded',
               content='eutils email test succeeded', to=['eugeneyanziyou@gmail.com'])
