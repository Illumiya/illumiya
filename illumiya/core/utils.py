'''
All core utils here!
'''

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import _get_queryset

from django.conf import settings

def send_email(subject,
               to_email,
               html_template_name,
               context,
               from_email=settings.DEFAULT_FROM_EMAIL):
    '''
    :param subject:
    :param to_email:
    :param html_template_name:
    :param context:
    :param from_email:
    :return:
    '''

    html_content = render_to_string(html_template_name, context)

    msg = EmailMessage(subject, html_content, from_email, to_email)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def get_object_or_none(klass,
                       *ar,
                       **kw):
    """
    Returns object if it exists or None.

    kclass may be Model, Manager, Object.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*ar,
                            **kw)
    except queryset.model.DoesNotExist:
        return None