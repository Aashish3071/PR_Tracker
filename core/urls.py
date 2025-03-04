from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('coverages/', views.coverage_list, name='coverage_list'),
    path('coverages/add/', views.add_coverage, name='add_coverage'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('coverage-report/', views.coverage_report, name='coverage_report'),
    path('ave-report/', views.ave_report, name='ave_report'),
    path('ave-report/export/', views.export_ave_report, name='export_ave_report'),
    path('custom-formulas/', views.custom_formula_list, name='custom_formula_list'),
    path('custom-formulas/add/', views.add_custom_formula, name='add_custom_formula'),
    path('custom-formulas/edit/<int:formula_id>/', views.edit_custom_formula, name='edit_custom_formula'),
    path('custom-formulas/delete/<int:formula_id>/', views.delete_custom_formula, name='delete_custom_formula'),
    path('custom-formulas/test/<int:formula_id>/', views.test_custom_formula, name='test_custom_formula'),
    
    # Report Template URLs
    path('report-templates/', views.report_template_list, name='report_template_list'),
    path('report-templates/upload/', views.upload_report_template, name='upload_report_template'),
    path('report-templates/edit/<int:template_id>/', views.edit_report_template, name='edit_report_template'),
    path('report-templates/delete/<int:template_id>/', views.delete_report_template, name='delete_report_template'),
    path('report-templates/generate/<int:template_id>/', views.generate_report, name='generate_report'),
    path('report-templates/download/<int:report_id>/', views.download_generated_report, name='download_generated_report'),
    
    # AJAX endpoints
    path('get-editions/', views.get_editions, name='get_editions'),
    path('get-campaigns/', views.get_campaigns, name='get_campaigns'),
    
    # Add new data URLs
    path('publications/add/', views.add_publication, name='add_publication'),
    path('editions/add/', views.add_edition, name='add_edition'),
    path('clients/add/', views.add_client, name='add_client'),
    path('campaigns/add/', views.add_campaign, name='add_campaign'),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
]
