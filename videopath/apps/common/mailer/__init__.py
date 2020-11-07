import conf

from django.template import Context
from django.template.loader import get_template

from videopath.apps.common.services import service_provider

mail_service = service_provider.get_service("mail")

#
# agents
#
agents = {
    "ree": {
        "email": "desiree@videopath.com",
        "name": "Desiree dela Rosa"
    }
}

#
# prepare mail variables
#
def prepare_mail(mailtype, variables, user = None, receiver = None):

    # get config for mail
    mailconf = conf.mails.get(mailtype, {})

    # update some defaults
    fvariables = {
        'to': 'void@videopath.com'
    }

    # default agent
    fvariables.update(conf.agents.get('default'))

    agent = mailconf.get('agent', 'default')

    # set sender
    if agent == 'user' and user:
        fvariables.update({
            "replyto": user.email,
            })
    elif agent != 'user':
        fvariables.update(conf.agents.get(agent))

    if user:
        fvariables.update({
            'to': [{'email':user.email}],
            'username':user.username,
            'user': user
            })

    if receiver:
        fvariables.update({
            'to': [{'email': receiver}]
            })


    fvariables.update(variables)
    c = Context(fvariables)

    return {
        'subject': mailconf.get('subject'),
        'text': get_template('mails/{0}.txt'.format(mailtype)).render(c),
        'html': get_template('mails/{0}.html'.format(mailtype)).render(c),
        'tags': [mailtype],
        'from_email': fvariables['from_email'],
        'from_name': fvariables['from_name'],
        'replyto': fvariables['replyto'],
        'to': fvariables['to']
    }

#
# send a mail
#
def send_mail(mailtype, variables, user = None, receiver = None):
    conf = prepare_mail(mailtype, variables, user, receiver)
    mail_service.mandrill_send(conf)


