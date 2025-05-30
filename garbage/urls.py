# garbage/urls.py
from django.urls import path
from . import views

app_name = 'garbage'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_report, name='upload_report'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('remove_report/<int:report_id>/', views.remove_report, name='remove_report'),
    path('logout/', views.logout_view, name='logout'),
    path('acknowledge/<int:report_id>/', views.acknowledge_notification, name='acknowledge_notification'),  # AJAX notification
    
 
]
