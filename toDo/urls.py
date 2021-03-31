from django.urls import path
from .views import Disp_tasks, Edit_View, Create_Task, Delete_View, CustomLoginView, RegisterView, Complete_View

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('',Disp_tasks,name='home'),
    path('create/',Create_Task,name='Create_Task'),
    path('task/<int:id>/',Edit_View,name='Edit_View'),
    path('task/delete/<int:id>/',Delete_View,name='Delete_View'),
    path('task/complete/<int:id>/',Complete_View,name='complete'),
]
