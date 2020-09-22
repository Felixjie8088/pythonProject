#coding: utf-8 
from __future__ import print_function, unicode_literals
from os.path import basename, exists
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib


class Email:
    def __init__(self, host='smtp.gmail.com', port=587, use_tls=True, username=None, password=None, subject=None, sender=None, to=None, cc=None, bcc=None):
        if not username or not password:
            raise ValueError('`username` and `password` must be provided')
      
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.username = username
        self.password = password
        
        self.message = MIMEMultipart('alternative')
        self.message['From'] = sender or self.username
        self.message['Subject'] = subject or ''
        
        if isinstance(to, list):
            to = ','.join(to)
        if isinstance(cc, list):
            cc = ','.join(cc)
        if isinstance(bcc, list):
            bcc = ','.join(bcc)
        
        if not to:
            raise ValueError('`to` must be provided')
      
        self.message['To'] = to
        self.message['Cc'] = cc or ''
        self.message['Bcc'] = bcc or ''
        
        self._success = None
        
    def content(self, content, subtype='plain'):
        self.message.attach(MIMEText(content, subtype))
        return self
      
    def text(self, text):
        return self.content(text, subtype='plain')
      
    def html(self, html):
        return self.content(html, subtype='html')
      
    def attachment(self, src, name=None):
        if isinstance(src, bytes):
            pass
        elif isinstance(src, str):
            if exists(src):
                path = src
                name = name or basename(path)
                with open(path, 'rb') as f:
                    src = f.read()
            else:
                src = src.encode()
        elif hasattr(src, 'read'):
            src = src.read()
            if hasattr(src, 'name'):
                name = name or basename(src.name)
            return self.attachment(src, name=name)
        else:
            raise TypeError('`src` got an unexpected class "%s"' % src.__class__)
        
        attachment = MIMEApplication(src, Name=name)
        self.message.attach(attachment)
        return self
      
    def send(self):
        print('Sending email...')
        self._send()
        return self
      
    def _send(self):
        try:
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            if self.use_tls:
                server.starttls()
                server.ehlo()
            server.login(self.username, self.password)

            sender = self.message['From']
            receivers = ','.join([self.message['To'], self.message['Cc'], self.message['Bcc']]).split(',')
            print('sender: %s' % sender)
            print('receivers: %s' % receivers)
            server.sendmail(sender, receivers, self.message.as_string())
            server.quit()
        except Exception as e:
            self._success = False
            print(e)
        else:
            print('Email sent successfully')
            self._success = True
            
    def retry(self, times=5):
        if not self._success:
            for i in range(times):
                print('Retrying sending email (attempt %d)...' % (i+1))
                self._send()
                if self._success:
                    break
        return self
