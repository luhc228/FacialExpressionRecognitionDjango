import sys
import threading

from django.http import HttpResponse
import json
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from visualize import detect as detector


@csrf_exempt
def image_upload(request):
    """
        上传图片接口
        @param image
    """

    global image_path
    global output_path
    if request.method == "POST":
        try:
            image = request.FILES['image']
            suffix = image.name.split('.')[-1]
            image_name = str(uuid.uuid1()) + '.' + suffix
            image_path = '%s/%s' % (settings.UPLOAD_DIR, image_name)
            with open(image_path, 'wb') as pic:
                for c in image.chunks():
                    pic.write(c)

            result_image_name = 'r_' + image_name
            output_path = '%s/%s' % (settings.RESULT_DIR, result_image_name)

        except Exception as e:
            response = {
                'success': False,
                'message': 'Upload fail',
            }
        else:
            response = {
                'success': True,
                'message': 'Upload successfully',
                'data': {
                    'resultImageName': result_image_name,
                    'imagePath': image_path,
                    'outputPath': output_path,
                }
            }

        return HttpResponse(content=json.dumps(response, ensure_ascii=False))


@csrf_exempt
def run_detector(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_path = data['imagePath']
            output_path = data['outputPath']
            detector(image_path, output_path)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'message': 'Run detector fail',
            }
        else:
            response = {
                'success': True,
                'message': 'Run detector successfully',
            }

        return HttpResponse(content=json.dumps(response, ensure_ascii=False))


def query_result(request):
    """
        HTTP轮询，检查处理是否完成，完成后返回结果，未完成返回False
    """
    if request.method == "GET":
        try:
            result_name = request.GET.get('imagename')
            image_path = '%s/%s/%s' % (settings.RESULT_ROOT, settings.RESULT_URL, result_name)
            open(image_path, "rb").read()

        except Exception as e:
            response = {
                'success': False,
                'message': 'No result, please wait a moment',
            }

        else:
            image_path = '%s%s%s' % (settings.STATIC_URL, settings.RESULT_URL, result_name)
            image_path = image_path.replace('//', '/')
            response = {
                'success': True,
                'message': 'upload success',
                'data': {
                    'imageUrl': image_path
                }
            }

        return HttpResponse(content=json.dumps(response, ensure_ascii=False),
                            content_type='application/json;charset = utf-8')
