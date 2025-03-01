from django.contrib import admin
from django.urls import path, include
from .views import (
    create_lead, sync_tags_with_active_campaign, sync_automations_with_active_campaign,
    receive_facebook_lead, get_leads, get_leads_report, AcademyLeadView, AcademyTagView,
    AcademyAutomationView
)
from rest_framework.authtoken import views

app_name='marketing'
urlpatterns = [
    path('lead', create_lead, name="lead"),
    path('lead/all', get_leads, name="lead_all"),
    path('academy/lead', AcademyLeadView.as_view(), name="academy_lead"),
    path('academy/<int:academy_id>/tag/sync', sync_tags_with_active_campaign, name="academy_id_tag_sync"),
    path('academy/<int:academt_id>/automation/sync', sync_automations_with_active_campaign, name="academy_id_automation_sync"),
    
    path('academy/tag', AcademyTagView.as_view(), name="academy_tag"),
    path('academy/automation', AcademyAutomationView.as_view(), name="academy_automation"),

    path('facebook/lead', receive_facebook_lead, name="facebook_all"),
    path('report/lead', get_leads_report, name="report_lead"),
    # path('report/summary', get_summary, name="report_summary"),
]
