from django.conf.urls import url

from photo_recognition import views

urlpatterns = [
    url('/image/upload', views.image_upload),
    url('/result/get', views.query_result)
]
