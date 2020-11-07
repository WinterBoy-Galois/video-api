
#
# List of available features
#
PLAN_FEATURES = [
	'feature_upload',
	'feature_vimeo',
	'feature_brightcove',
	'feature_own_hosting',
    'feature_wistia',
    'feature_custom_hosting',
   	'feature_endscreen',
	'feature_advanced_settings',
	'feature_advanced_library',
	'feature_email_collector',
    'feature_integrations',
    'feature_custom_analytics',
    'feature_movingimage',
    'feature_teams', 
    'feature_theme',
    'feature_icon',
    'feature_advanced_video_settings', 
    'feature_dev',
    'feature_advanced_analytics',
    'feature_whitelabel'
]

PLAN_DEFAULTS = {

    'id': False,

	'subscribable': False,
	'listable': False,

	'group': 'free',
    'coupons': False,

    'max_projects': 5000,
    'max_views_month': 10000000,
    'name': 'Videopath Plan',
    'price_eur': 0,
    'price_usd': 0,
    'price_gbp': 0,
    'payment_interval': 'month',
    'value': 1

}

PLANS = {

	###################
	# CURRENT
	###################

	# free plan, simple
    'free': {

        'group': 'free',
        'subscribable': True,
        'listable': True,
        
        #
        # variants
        #
        'variants': {
            'free': {
                'name': 'Free',
                'price_eur': 0,
                'price_usd': 0,
                'price_gbp': 0,
                'payment_interval': 'month',
                'value': 1000,
            }
        }

    },


    # starter plan with 2 variants
    '201509-starter': {

        'group': 'starter',
        'subscribable': True,

        #
        # features
        #
        'feature_endscreen': True,
        'feature_advanced_library': True,
        'feature_advanced_analytics': True,
        'feature_vimeo': True,
        'feature_wistia': True,

        #
        # variants
        #
        'variants': {

             'monthly-15': {
                'name': 'Basic Monthly',
                'price_eur': 1500,
                'price_usd': 2000,
                'price_gbp': 1200,
                'payment_interval': 'month',
                'value': 2001,
                'subscribable': False
            },   

            'monthly-25': {
                'name': 'Basic Monthly',
                'price_eur': 2500,
                'price_usd': 2500,
                'price_gbp': 2500,
                'payment_interval': 'month',
                'value': 2001,
                'subscribable': False
            },   

            'monthly-20-discount': {
                'coupons': ['partners-starter'],
                'name': 'Basic Monthly (20% Partners Discount)',
                'price_eur': 5900,
                'price_usd': 7900,
                'price_gbp': 4500,
                'payment_interval': 'month',
                'value': 2002,
            },   

            'monthly': {
                'name': 'Basic Monthly',
                'price_eur': 7900,
                'price_usd': 9900,
                'price_gbp': 5900,
                'payment_interval': 'month',
                'value': 2003,
                'listable': True,
            },

            'yearly-20-discount': {
                'coupons': ['partners-starter'],
                'name': 'Basic Yearly (20% Partners Discount)',
                'price_eur': 64000,
                'price_usd': 80000,
                'price_gbp': 65000,
                'payment_interval': 'year',
                'value': 2004,
            },   

            'yearly': {
                'name': 'Basic Yearly',
                'price_eur': 80000,
                'price_usd': 100000,
                'price_gbp': 65000,
                'payment_interval': 'year',
                'value': 2005,
                'listable': True,
            },



        }

    },

    # pro plan
    '201412-pro-plus': {

        'group': 'pro-plus',
        'subscribable': True,

        #
        # features
        #
        'feature_endscreen': True,
        'feature_advanced_settings': True,
        'feature_vimeo': True,
        'feature_wistia': True,
        'feature_custom_analytics': True,
        'feature_custom_hosting': True,
        'feature_theme': True,
        'feature_icon': True,
        'feature_advanced_library': True,
        'feature_advanced_analytics': True,

        #
        # variants
        #
        'variants': {

            'monthly-25-jobviddy': {
                'name': 'Professional Monthly (25% Discount) Andy',
                'price_eur': 25900,
                'price_usd': 29900,
                'price_gbp': 22500,
                'payment_interval': 'month',
                'value': 4001,
                'feature_advanced_video_settings': True,
                'subscribable': False
            },

            'monthly-20-discount': {
                'name': 'Professional Monthly (20% Partners Discount)',
                'coupons': ['partners-pro-plus'],
                'price_eur': 27900,
                'price_usd': 31900,
                'price_gbp': 23900,
                'payment_interval': 'month',
                'value': 4002,
            },

            'monthly': {
                'name': 'Professional Monthly',
                'price_eur': 34900,
                'price_usd': 39900,
                'price_gbp': 29900,
                'payment_interval': 'month',
                'value': 4003,
                'listable': True,
            },

            'yearly-20-discount': {
                'name': 'Professional Yearly (20% Partners Discount)',
                'coupons': ['partners-pro-plus'],
                'price_eur': 280000,
                'price_usd': 340000,
                'price_gbp': 220000,
                'payment_interval': 'year',
                'value': 4004,
            },

            'yearly': {
                'name': 'Professional Yearly',
                'price_eur': 350000,
                'price_usd': 425000,
                'price_gbp': 280000,
                'payment_interval': 'year',
                'value': 4005,
                'listable': True,
            },

            

            
        }
    },

    # pro plan
    '201412-enterprise': {

        'group': 'enterprise',
        'subscribable': True,

        #
        # features
        #
        'feature_endscreen': True,
        'feature_advanced_settings': True,
        'feature_vimeo': True,
        'feature_wistia': True,
        'feature_custom_analytics': True,
        'feature_custom_hosting': True,
        'feature_theme': True,
        'feature_icon': True,
        'feature_advanced_library': True,
        'feature_advanced_analytics': True,
        'feature_email_collector': True,
        'feature_advanced_video_settings': True,
        'feature_brightcove': True,


        #
        # variants
        #
        'variants': {

            'monthly-20-discount': {
                'name': 'Enterprise Monthly (20% Partners Discount)',
                'coupons': ['partners-enterprise'],
                'price_eur': 100000,
                'price_usd': 110000,
                'price_gbp': 83900,
                'payment_interval': 'month',
                'value': 6001
            },

            'monthly': {
                'name': 'Enterprise Monthly',
                'price_eur': 129900,
                'price_usd': 139900,
                'price_gbp': 104900,
                'payment_interval': 'month',
                'value': 6002
            },

            'yearly-20-discount': {
                'name': 'Enterprise Yearly (20% Partners Discount)',
                'coupons': ['partners-enterprise'],
                'price_eur': 1100000,
                'price_usd': 1200000,
                'price_gbp': 800000,
                'payment_interval': 'year',
                'value': 6003
            },

            'yearly': {
                'name': 'Enterprise Yearly',
                'price_eur': 1400000,
                'price_usd': 1500000,
                'price_gbp': 1000000,
                'payment_interval': 'year',
                'value': 6004
            }
        }
    },

    ###################
	# INDIVIDUAL
	###################

    'individual': {

        'group': 'individual',

        'variants': {

            'individual': {
                'name': 'Individual Plan',
                'price_eur': 0,
                'value': 8000
            },

            'meisterclass': {

                'name': 'Individual meisterclasss',

                'price_eur': 3500,
                'payment_interval': 'month',

                'feature_upload': False,
                'feature_endscreen': True,

                'value': 8001,
            },

            'escp': {
                'name': 'Individual escp',

                'price_eur': 3500,
                'payment_interval': 'month',

                'feature_endscreen': True,
                'feature_vimeo': True,
                'feature_upload': True,
                'feature_theme': True,
                'feature_advanced_library': True,

                'value': 8002,
            },

            'sspss': {

                'name': 'Individual SSPSS',

                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_theme': True,
                'feature_advanced_library': True,

                'value': 8003,
            },

            'agency-evaluation': {

                'name': 'Agency Evaluation',

                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_analytics': True,

                'value': 8004,
            },

            'brightcove': {
                'name': 'Pro',

                # features
                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_custom_analytics': True,
                'feature_brightcove': True,
                'feature_custom_hosting': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_video_settings': True, 
                'feature_integrations': True,
                'feature_advanced_analytics': True,

                'value': 8005
            },

            'coop': {
                'name': 'Coop Enterprise',

                # features
                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_custom_analytics': True,
                'feature_brightcove': True,
                'feature_custom_hosting': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_video_settings': True, 
                'feature_integrations': True,
                'feature_advanced_analytics': True,

                'value': 8006
            },

            'moodfilm': {
                'name': 'Moodfilm enterprise',
                # features
                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_custom_analytics': True,
                'feature_brightcove': True,
                'feature_custom_hosting': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_video_settings': True, 
                'feature_integrations': True,
                'feature_advanced_analytics': True,
                'feature_email_collector': True,
                'feature_whitelabel': True,

                'price_eur': 34900,
                'price_usd': 39900,
                'price_gbp': 29900,
                'payment_interval': 'month',

            },

            'veedu': {
                'name': 'Enterprise Monthly',

                #
                # features
                #
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_vimeo': True,
                'feature_wistia': True,
                'feature_custom_analytics': True,
                'feature_custom_hosting': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_analytics': True,
                'feature_email_collector': True,
                'feature_advanced_video_settings': True,
                'feature_brightcove': True,

                'price_eur': 76500,
                'price_usd': 76500,
                'price_gbp': 76500,


            },


            'staff': {
                'name': 'videopath staff account',

                # features
                'feature_vimeo': True,
                'feature_upload': True,
                'feature_endscreen': True,
                'feature_advanced_settings': True,
                'feature_wistia': True,
                'feature_dev': True,        
                'feature_custom_analytics': True,
                'feature_brightcove': True,
                'feature_custom_hosting': True,
                'feature_theme': True,
                'feature_icon': True,
                'feature_advanced_library': True,
                'feature_advanced_video_settings': True, 
                'feature_integrations': True,
                'feature_email_collector': True,
                'feature_teams': True,
                'feature_advanced_analytics': True,
                'feature_movingimage': True,


                'value': 9999,
            }

        }
    }
}


DEFAULT_PLAN = 'free-free'

#
# Merge and flatten out variants
#
def _merge_variants(PLANS):
	result={}
	for plan_id, plan in PLANS.iteritems():
		for variant_id, variant in plan.pop('variants').iteritems():
			key = plan_id + '-' + variant_id
			result[key] = dict(PLAN_DEFAULTS.items()+plan.items() + variant.items() + [('id', key)])
	return result
PLANS = _merge_variants(PLANS)
PLANS_SORTED = sorted(PLANS.values(), key= lambda plan: plan["value"])
PLANS_CHOICES = map(lambda plan: (plan["id"], "{0:04d} {1} ({2})".format(plan["value"], plan["name"], plan["id"])), PLANS_SORTED)

#
# Set default
#
DEFAULT_PLAN = PLANS[DEFAULT_PLAN]

def SUBSCRIBABLE_PLANS(group):

    def _filter(p):
        if not p['subscribable']: return False
        if (not group or group == '') and p["listable"]: return True
        if p['coupons'] and group in p['coupons']: return True
        if not p['coupons'] and group == p["group"]: return True
        return False

    return filter(_filter, PLANS.values())


#
# Do structural checks
#
def _check_plan(plan):
    assert plan['id'], 'Plan {1} should have an ID'.format(plan['name'])
    for key in plan:
        assert (key in PLAN_DEFAULTS or key in PLAN_FEATURES), 'Unknown plan setting {0} in plan {1}'.format(key, plan['name'])

for key, p in PLANS.iteritems():
    _check_plan(p)



