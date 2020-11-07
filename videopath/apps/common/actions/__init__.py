
#
# Default action exception
#
class ActionException(Exception):
	pass

#
# Permission denied exception
#
class PermissionDeniedException(Exception):
	pass

#
# User does not have the right plan
#
class UpgradeNeededException(Exception):
	pass