from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class SwipeMail(EmailMultiAlternatives):
    string_template = None
    html_template = None

    from_email = None
    to = []
    to_customers = []

    cc = []
    cc_customers = []

    reply_to = None
    subject = None

    def __init__(self, to=None, to_customers=None, attachments=None, cc=None, cc_customers=None, reply_to=None,
                 connection=None):
        if to_customers:
            for user in to_customers:
                self.to_customers.append(user) if user not in self.to_customers else None
        if to:
            for mail_addr in to:
                self.to.append(mail_addr) if mail_addr not in self.to else None
        for user in self.to_customers:
            self.to.append(user.email) if user.email not in self.to else None

        if cc_customers:
            for user in cc_customers:
                self.cc_customers.append(user) if user not in self.cc_customers else None
        if cc:
            for mail_addr in cc:
                self.cc.append(mail_addr) if mail_addr not in self.cc else None
        for user in self.cc_customers:
            self.cc.append(user.email) if user.email not in self.cc else None

        super().__init__(subject=self.subject, from_email=self.from_email, to=self.to, attachments=attachments,
                         cc=self.cc, reply_to=reply_to or self.reply_to, connection=connection)

    def send(self, fail_silently=False):
        if isinstance(self.html_template, str):
            html_template = get_template(self.html_template)
        else:
            html_template = self.html_template

        if isinstance(self.string_template, str):
            string_template = get_template(self.string_template)
        else:
            string_template = self.string_template

        if string_template:
            self.attach_alternative(string_template.render(self.get_context()), 'text/plain')

        if html_template:
            self.attach_alternative(html_template.render(self.get_context()), 'text/html')

        super().send(fail_silently)

    def get_context(self):
        """
        :return: the context used in the rendering of the template
        :rtype: Context
        """
        return Context({
            'subject': self.subject,
            'to': self.to,

        })
