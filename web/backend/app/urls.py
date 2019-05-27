from django.urls import path

from . import views
app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/versions/',views.get_versions, name='get all versions'),
    path('api/jokes/',views.get_jokes,name='get all jokes'),
    path('api/versions/<int:version>',views.get_version, name='get version'),
    path('api/versions/create',views.create_version,name='create new training version')

]