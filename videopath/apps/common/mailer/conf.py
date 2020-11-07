import datetime

#
# register all mail types
#
mails = {

	#
	# signup sent after user signs up for our app
	#
	'signup': {
		'subject': "Hello from Videopath!"
	},


	'forgot_password': {
		'subject': "Videopath Password Reset"
	},

	'share_video': {
		'subject': "An interactive video was shared with you!",
		'agent': 'user'
	},

	#
	# subscriptions etc
	#
	'subscribe_will_change': {
		'subject': 'Subscription Info'
	},

	'subscribe_change': {
		'subject': 'Subscription Info'
	},

	'invoice_created': {
		'subject': "Videopath billing"
	},

	'payment_failed': {
		'subject': "Videopath payment failed"
	},


	#
	# quota
	#
	'quota_warning': {
		'subject': "You have almost used up your quota this month"
	},

	'quota_exceeded': {
		'subject': "You have exceeded your quota this month"
	},

	#
	# transcoding
	#
	'jpg_transcode_failed': {
		'subject': 'iPhone Trancoding Failed'
	},


	'jpg_transcode_succeeded': {
		'subject': 'iPhone Transcoding Successful'
	},

	'transcode_complete': {
		'subject': 'Your video is ready to edit'
	},

	'transcode_error': {
		'subject': 'Error processing your video'
	},


	#
	# Follow up emails
	#
	'welcome': {
		'subject': "How's Videopath working?",
		'agent': 'support'
	},

	'follow_up_three_weeks': {
		'subject': "Get the most out of Videopath",
		'agent': 'support'
	},

	'follow_up_six_weeks': {
		'subject': "Make Videopath work for you!",
		'agent': 'support'
	}

}

#
# agents
#
agents = {

	"default": {
    	"from_email": "support@videopath.com",
        "from_name": "Videopath Team",
        "replyto": "support@videopath.com",
    },

    "support": {
        "from_email": "desiree@videopath.com",
        "from_name": "Desiree dela Rosa",
        "replyto": "desiree@videopath.com",
    },

}

#
# data for displaying the test versions of the mail
#
test_data = {

	'forgot_password': {
		'password': '980LJSJ3n'
	},

	'share_video': {
		'message': "Hey there, check out my cool video!",
		'description': "Description of my video",
		'title': "My Video!",
		'link': "http://player.videopath.com/wmq2XEQj",
		'thumb_url': 'https://dobvnaghfdgn1.cloudfront.net/WjI1mIEE3GbpTFCz2GfNCXKLvS4A92tx-hd',
		'to': [{'email':'user1@example.com'}, {'email':'user2@example.com'}, {'email':'user3@example.com'}],
	},


	#
	# subscriptions etc
	#
	'subscribe_will_change': {
		'plan': 'Pro',
		'switch_date': datetime.date.today()
	},

	'subscribe_change': {
		'interval': 'Month',
		'plan': 'Pro',
		'is_free': False
	},

	'invoice_created': {
		"amount_due": 640000,
        "link": 'http://player.videopath.com/wmq2XEQj',
        "currency": "EUR"
	},

	'payment_failed': {
		"amount_due": 640000,
        "link": 'http://player.videopath.com/wmq2XEQj',
        "currency": "EUR"
	},


	#
	# transcoding
	#
	'jpg_transcode_failed': {
		'title': "My Project"
	},

	'jpg_transcode_succeeded': {
		'title': "My Project"
	},


	'transcode_complete': {
		'title': "My Project",
		'video_id': "12345678"
	},

	'transcode_error': {
		'title': "My Project"
	},

	


}