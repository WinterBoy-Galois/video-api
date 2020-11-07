import conf
from videopath.apps.common import mailer

from django.template import Context
from django.template.loader import get_template

from django.template.response import HttpResponse, SimpleTemplateResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def view(request):

	mail = request.GET.get('mail', 'signup')
	mailtype = request.GET.get('mailtype', 'html')

	testconf = conf.test_data.get(mail, {})
	mailconf = mailer.prepare_mail(mail, testconf, request.user)

	to = map(lambda x: x['email'], mailconf['to'])
	to = reduce(lambda x, y: x + ',' + y, to)

	return SimpleTemplateResponse("qa/mails.html", {
			'mails': conf.mails.keys(),
			'mail': mail,
			'mailtype': mailtype,

			'mailsubject': mailconf['subject'],
			'from_name': mailconf['from_name'],
			'from_email': mailconf['from_email'],
			'replyto': mailconf['replyto'],
			'to': to
	    })

@staff_member_required
def mailview(request, mail, mailtype):

	testconf = conf.test_data.get(mail, {})

	mailconf = mailer.prepare_mail(mail, testconf, request.user)
	message = mailconf['html'] 

	if mailtype == 'txt':
		c = Context({'mail': mailconf['text']})
		t = get_template('qa/plain_mail_wrapper.html')
		message = t.render(c)

	return HttpResponse(message)
