from django.urls import path
from .views import *
from admin_panel.api import views as api_views

app_name = 'admin-panel-api'

urlpatterns = [
    path('v1/user-register/',api_views.RegisterAPICreate.as_view(), name ='user'),
    path('v1/user-update/',api_views.UserUpdateView.as_view(), name ='user'),
    path('v1/user-detail/',api_views.UserSelfDetail.as_view(), name ='user'),

    path('v1/page/',api_views.PageAPIList.as_view(), name ='page'),

    path('v1/subpage/',api_views.SubpageAPIList.as_view(), name ='subpage'),
]