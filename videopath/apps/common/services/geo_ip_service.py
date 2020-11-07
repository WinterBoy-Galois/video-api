import pygeoip
import os

def record_by_address(ip):
	dat_path = os.path.dirname(os.path.abspath(__file__)) + "/assets/GeoIP.dat"
	try:
	    gi = pygeoip.GeoIP(dat_path, pygeoip.MEMORY_CACHE)
	    country = gi.country_code_by_addr(ip)
	    country_index = pygeoip.const.COUNTRY_CODES.index(country)
	    country_full = pygeoip.const.COUNTRY_NAMES[country_index]
	    continent = pygeoip.const.CONTINENT_NAMES[pygeoip.const.COUNTRY_CODES.index(country)]
	    return {
	    	"continent": continent,
	    	"country": country,
	    	"country_full": country_full
	    }
	except:
	    return {
	    	"continent": "--",
	    	"country": "--",
	    	"country_full": "--"
	    }


def record_from_request(request):
	# get correct ip
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
	    ip = x_forwarded_for.split(',')[0]
	else:
	    ip = request.META.get('REMOTE_ADDR')
	return record_by_address(ip)

