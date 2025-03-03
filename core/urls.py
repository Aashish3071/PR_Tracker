from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_coverage, name='add_coverage'),
    path('list/', views.coverage_list, name='coverage_list'),
    path('upload/', views.upload_coverage, name='upload_coverage'),
    path('report/', views.coverage_report, name='coverage_report'),
]