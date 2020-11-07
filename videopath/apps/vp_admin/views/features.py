
from .decorators import group_membership_required
from django.template.response import SimpleTemplateResponse
from django.db import connection
from videopath.apps.vp_admin.views import helpers

EXCLUDED_USER_NAMES = [
	"anna",
	"marketing",
	"david"
]

@group_membership_required('insights')
def view(request):


	#
	# General Query Building blocks
	#
	SELECT_PUBLISHED_REVISIONS = "SELECT COUNT(*) FROM videos_video as v JOIN videos_videorevision as vr ON(v.current_revision_id = vr.id) JOIN users_team as t ON (t.id = v.team_id) JOIN auth_user as u ON (u.id = t.owner_id) "
	SELECT_PUBLISHED_MARKERS = SELECT_PUBLISHED_REVISIONS + " JOIN videos_marker vm ON (vm.video_revision_id = vr.id)"
	SELECT_PUBLISHED_CONTENT_BLOCKS = SELECT_PUBLISHED_MARKERS + " JOIN videos_markercontent vmc ON (vmc.marker_id = vm.id)"
	SELECT_VIDEO_SOURCES = SELECT_PUBLISHED_REVISIONS + " JOIN videos_source as s ON (vr.source_id = s.id)"

	result = "Staff videos are not included in these statistics. <br />Only published videos are counted."

	#
	# Overall stats
	#
	result += helpers.header("Overall Stats (Published)")

	num_videos = get_result(SELECT_PUBLISHED_REVISIONS)
	num_markers = get_result(SELECT_PUBLISHED_MARKERS)
	num_blocks = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS)

	table = []
	table.append(["Published Videos", num_videos])
	table.append(["Published Markers", num_markers])
	table.append(["Published Content Blocks", num_blocks])
	table.append([""])
	table.append(["Markers per publ. Video", num_markers / num_videos])
	table.append(["Content Blocks per publ. Video", num_blocks / num_videos])
	table.append(["Content Blocks per publ. Marker", num_blocks / num_markers])
	result += helpers.table(table, ["Feature", "All", "Upgraded"])

	#
	# Import Source Stats
	#
	result += helpers.header("Import Source Stats (Published)")

	num_uploaded = get_result(SELECT_VIDEO_SOURCES + " WHERE s.service like 'videopath'")

	num_youtube = get_result(SELECT_VIDEO_SOURCES + " WHERE s.service like 'youtube'")
	num_vimeo = get_result(SELECT_VIDEO_SOURCES + " WHERE s.service like 'vimeo'")
	num_wistia = get_result(SELECT_VIDEO_SOURCES + " WHERE s.service like 'wistia'")
	num_brightcove = get_result(SELECT_VIDEO_SOURCES + " WHERE s.service like 'brightcove'")

	table = [["Import Source", 'Videos']]
	table.append(["Uploaded Files", num_uploaded])
	table.append(["Youtube Hosting", num_youtube])
	table.append(["Vimeo Hosting", num_vimeo])
	table.append(["Wistia Hosting", num_wistia])
	table.append(["Brightcove Hosting", num_brightcove])
	result += helpers.chart(table,'column')

	#
	# Video Feature Stats
	#
	result += helpers.header("Video Feature Stats (Published)")

	num_custom_colors = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.ui_color_1 != '#424242'")
	num_continuous_playback = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.continuous_playback = true")
	num_equal_marker_lengths = get_result(SELECT_PUBLISHED_REVISIONS +  "WHERE vr.ui_equal_marker_lengths = true")
	num_custom_thumbnail = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.custom_thumbnail_id != 0")
	num_disable_share_buttons = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.ui_disable_share_buttons = true")
	num_fit_video = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.ui_fit_video = true")
	num_custom_tracking_code = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.custom_tracking_code != ''")
	num_password = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.password !=''")
	# num_iphone_enabled = get_result(SELECT_PUBLISHED_REVISIONS + " WHERE vr.iphone_images > 20")

	table = [['Feature', 'Videos']]
	table.append(["Custom Colors", num_custom_colors])
	table.append(["Custom Thumbnail", num_custom_thumbnail])
	table.append(["Disabled Share Buttons", num_disable_share_buttons])
	table.append(["Equal Marker Lengths", num_equal_marker_lengths])
	table.append(["Fit Video", num_fit_video])
	table.append(["Custom Tracking Code", num_custom_tracking_code])
	table.append(["Password Protection", num_password])
	table.append(["Continuous Playback", num_continuous_playback])
	# table.append(["Iphone enabled", num_iphone_enabled])
	result += helpers.chart(table,'column')


	#
	# Content Block Stats
	#
	result += helpers.header("Content Block Stats (Published)")
	

	num_text_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'text'")
	num_image_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'image'")
	num_social_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'social'")
	num_media_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'media'")
	num_website_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'website'")
	num_maps_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'maps'")
	num_button_block = get_result(SELECT_PUBLISHED_CONTENT_BLOCKS + " WHERE vmc.type = 'simple_button'")


	table = [["Type", "Amount"]]
	table.append(["Text ", num_text_block])
	table.append(["Image ", num_image_block])
	table.append(["Social ", num_social_block])
	table.append(["Media ", num_media_block])
	table.append(["Website ", num_website_block])
	table.append(["Button ", num_button_block])
	table.append(["Maps ", num_maps_block])
	result += helpers.chart(table,'pie')


	return SimpleTemplateResponse("insights/base.html", {
	    "title": "Features",
	    "insight_content": result
	    })

def line(title, result):
	return title + ": " + str(result) + "<br />"

def get_result(query):

	# exclude certain user names
	s = " u.username NOT IN (" 
	for n in EXCLUDED_USER_NAMES:
		s += "'" + n + "',"
	s = s[:-1]
	s += ")"

	if "WHERE" in query:
		query += " AND " + s
	else:
		query += " WHERE " + s

	cursor = connection.cursor()
	cursor.execute(query)
	val_all = cursor.fetchone()[0]


	return val_all
