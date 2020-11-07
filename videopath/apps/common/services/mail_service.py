from django.conf import settings

from inlinestyler.utils import inline_css

logger = settings.LOGGER

import sendgrid


def check_access():
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    status, msg = sg.apikeys.get()
    return status == 200

def sendgrid_send(m):
    sg = sendgrid.SendGridClient(settings.SENDGRID_API_KEY)

    # create message
    message = sendgrid.Mail()

    message.set_subject(m.get('subject', ''))
    message.set_from(m.get('from_email', ''))
    message.set_from_name(m.get('from_name', ''))

    if 'replyto' in m:
        message.set_replyto(m['replyto'])

    if 'text' in m:
        message.set_text(m['text'])
    if 'html' in m:
        message.set_html(inline_css(m['html']))

    for recipient in m.get('to', []):
        message.add_to(recipient['email'])

    for tag in m.get('tags', []):
        message.add_category(tag)

    sg.send(message)


def mandrill_send(m):
    return sendgrid_send(m)

#
# for now, just abstract the mandrill sending here
#
# def mandrill_send(message):

#     # prefix messages sent from dev
#     subject_prefix = "[Dev] " if (settings.STAGING or settings.LOCAL or settings.CONTINOUS_INTEGRATION) else ""
#     message["subject"] = subject_prefix + message.get("subject", 0)

#     try:
#         m = Mandrill(settings.MANDRILL_APIKEY)
#         m.messages.send(message=message, async=False, ip_pool='Main Pool')
#     except:
#         logger.error("error sending mail")



#
# Check acccess
#
# def check_access():
# 	try:
# 		m = Mandrill(settings.MANDRILL_APIKEY)
# 		m.users.ping()
# 		return True
# 	except Exception as e:
# 		return str(e)
