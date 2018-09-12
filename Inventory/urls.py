from django.urls import path
from . import views

urlpatterns = [
    path('question', views.post_list, name='post_list'),
    path('question/new/', views.Question_new, name='question_new'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
    path('withdraw_inventory', views.withdraw_inventory, name='withdraw_inventory'),
    path('records', views.showfile, name='records'),
    path('', views.InventoryTable, name='index'),
]
