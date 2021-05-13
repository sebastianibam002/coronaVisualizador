from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("upload_file", views.upload_file, name="upload_file"),
    path("executive_view", views.executive_view, name="executive"), 
    path("download", views.download, name="download")
]


urlpatterns += staticfiles_urlpatterns()