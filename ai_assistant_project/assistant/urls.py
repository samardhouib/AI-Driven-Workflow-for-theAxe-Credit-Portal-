from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete_history_entry/<int:entry_index>/', views.delete_history_entry, name='delete_history_entry'),
    path('download_output/', views.download_output, name='download_output'),
]
