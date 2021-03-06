from django.urls import path
from . import views

urlpatterns = [
    path('question', views.post_list, name='post_list'),
    path('question/new/', views.Question_new, name='question_new'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
    path('withdraw_inventory', views.withdraw_inventory, name='withdraw_inventory'),
    path('records', views.showfile, name='records'),
    path('', views.InventoryTable, name='index'),
    path('qr_code', views.qr_code, name='qr_code'),
    path('qr_code_results', views.qr_code_result, name='qr_code_results'),
]
