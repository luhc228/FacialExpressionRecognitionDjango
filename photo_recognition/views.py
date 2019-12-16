from django.http import HttpResponse
import json
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def image_upload(request):
    """
        上传图片接口
        @param image
    """
    if request.method == "POST":
        image = request.FILES['image']
        suffix = image.name.split('.')[-1]
        image_name = str(uuid.uuid1()) + '.' + suffix
        image_path = '%s/%s' % (settings.UPLOAD_DIR, image_name)
        with open(image_path, 'wb') as pic:
            for c in image.chunks():
                pic.write(c)

        result_image_name = 'r_' + image_name

        response = {
            'success': True,
            'message': 'Upload successfully',
            'data': {
                'resultImageName': result_image_name
            }
        }
    else:
        response = {
            'success': False,
            'message': 'Upload fail',
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
