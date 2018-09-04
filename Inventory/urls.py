from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('question/new/', views.Question_new, name='question_new'),
    path('add_inventory', views.gtable, name='add_inventory'),
    path('records', views.showfile, name='records'),
]
