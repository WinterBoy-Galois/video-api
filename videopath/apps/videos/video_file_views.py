
#
# All views that have to do with uploading and transcoding of a video file
#

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from videopath.apps.videos.models import Video, Source
from videopath.apps.files.util.aws_util import confirm_subscription
from videopath.apps.common.mailer import send_mail
from videopath.apps.files.util.aws_util import get_upload_endpoint, verify_upload, start_transcoding_video


#
# Handle file uploads
#
@api_view(['POST', 'GET'])
def video_request_upload_ticket(request, video_id=None):

    # only allow request if video is found and user is owner
    video = Video.objects.get_video_for_user(request.user, pk=video_id)

    source = Source.objects.create(service='videopath', status=Source.STATUS_WAITING)
    video.draft.source = source
    video.draft.save()

    return Response({
        'ticket_id': source.key, 
        'endpoint': get_upload_endpoint(key=source.key)
    })


@api_view(['POST', 'GET'])
def video_upload_complete(request, ticket_id=None):

    source = get_object_or_404(Source, key=ticket_id)

    file_found = verify_upload(ticket_id=ticket_id)
    jobStarted = 0
    if file_found:
        source.status = Source.STATUS_PROCESSING
        source.save()
        job = start_transcoding_video(source)

        # save data in file
        if job:
            jobStarted = 1
        else:
            source.state = Source.STATUS_ERROR
            
    return Response({
        'ticket_id': ticket_id,
        'file_found': file_found, 
        'job_started': jobStarted
    })


#
# Process AWS notifications
#
@csrf_exempt
def process_notification(request, type):
    
    # load body
    try:
        post = json.loads(request.body)
    except BaseException:
        return HttpResponse() 

    # respond to aws subscription request
    if post['Type'] == 'SubscriptionConfirmation':
        if 'Token' in post and 'TopicArn' in post:
            confirm_subscription(post['TopicArn'], post['Token'])
            return HttpResponse()

    # retrieve video file
    message = json.loads(post['Message'])
    key = message['input']['key']
    state = message["state"]

    try:
        source = Source.objects.get(key=key)
    except Source.DoesNotExist:
        return HttpResponse()

    # parse status out of type
    if state == 'PROGRESSING':
        source.status = Source.STATUS_PROCESSING

    elif state == 'COMPLETED':
        thumbs_no = '00001' #'00002' if message['outputs'][0]['duration'] > 65 else '00001'
        source.aspect = float( message['outputs'][0]['width'] ) / float(message['outputs'][0]['height'])
        source.duration = message['outputs'][0]['duration']
        source.status = Source.STATUS_OK
        source.file_mp4 = key + '.mp4'
        source.file_webm = key + '.webm'
        source.thumbnail_small = key + '/'+ thumbs_no + '.jpg'
        source.thumbnail_large = key + '/' + thumbs_no + '-hd.jpg'
        revision = source.revisions.first()
        send_mail('transcode_complete', {'title': revision.title, 'video_id':revision.video.id}, revision.video.team.owner)

    elif state == 'ERROR':
        source.status = Source.STATUS_ERROR
        source.description = message['outputs'][0]['statusDetail']
        revision = source.revisions.first()
        send_mail('transcode_error', {'title': revision.title, 'video_id':revision.video.id}, revision.video.team.owner)


    source.save()

    # respond with empty json
    return HttpResponse()
