from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_image, name='index'),
    path('<str:image_name>/', views.show_image)
]
