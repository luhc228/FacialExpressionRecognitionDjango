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

        result_file_path = 'r_' + image_name

        response = {
            'success': True,
            'message': '上传图片成功',
            'data': {
                'resultfilePath': result_file_path
            }
        }
    else:
        response = {
            'success': False,
            'message': '上传失败',
        }

    return HttpResponse(content=json.dumps(response, ensure_ascii=False),
                        content_type='application/json;charset = utf-8')


def query_result(request):
    """
        HTTP轮询，检查处理是否完成，完成后返回结果，未完成返回False
    """
    if request.method == "GET":
        try:
            result_name = request.GET.get('filename')
            image_path = '%s/%s' % (settings.RESULT_DIR, result_name)
            image_data = open(image_path, "rb").read()
            print(image_data)
        except Exception as e:
            response = {
                'success': False,
                'message': 'No result, please wait a moment',
            }

        else:
            response = {
                'success': True,
                'message': '结果图获取成功',
            }

        return HttpResponse(content=json.dumps(response, ensure_ascii=False),
                            content_type='application/json;charset = utf-8')
