from django.urls import path
from .views import (
    AcademyView, CohortUserView, AcademyCohortView,
    get_timezones, UserView, UserMeView, AcademyCohortUserView,
    get_single_course, SyllabusView, CertificateView,
    CertificateAllView, get_all_academies, get_cohorts
)

app_name = 'admissions'
urlpatterns = [
    # depcrecated methods, soon to be deleted
    path('cohort/all', get_cohorts, name="cohort_all"),
    path('cohort/user', CohortUserView.as_view(), name="cohort_user"),
    path('cohort/<int:cohort_id>/user/<int:user_id>', CohortUserView.as_view(),
         name="cohort_id_user_id"),
    path('cohort/<int:cohort_id>/user',
         CohortUserView.as_view(), name="cohort_id_user"),

    # new endpoints (replacing above)
    path('academy/cohort/user', AcademyCohortUserView.as_view(),
         name="academy_cohort_user"),
    path('academy/cohort/<str:cohort_id>',
         AcademyCohortView.as_view(), name="academy_cohort_id"),
    path('academy/cohort/<int:cohort_id>/user/<int:user_id>',
         AcademyCohortUserView.as_view()),
    path('academy/cohort/<int:cohort_id>/user',
         AcademyCohortUserView.as_view()),

    path('academy/', get_all_academies, name="academy"),
    path('academy/me', AcademyView.as_view(), name="academy_me"),
    path('academy/cohort', AcademyCohortView.as_view(), name="academy_cohort"),
    path('user/me', UserMeView.as_view(), name="user_me"),
    path('user', UserView.as_view(), name="user"),

    path('certificate', CertificateAllView.as_view(), name="certificate"),
    path('certificate/<str:certificate_slug>/', get_single_course,
         name="certificate_slug"),
    path('academy/certificate', CertificateView.as_view(),
         name="academy_certificate"),
    path('certificate/<str:certificate_slug>/syllabus', SyllabusView.as_view(),
         name="certificate_slug_syllabus"),
    path('certificate/<str:certificate_slug>/syllabus/<int:version>',
         SyllabusView.as_view(), name="certificate_slug_syllabus_version"),
    path('certificate/<str:certificate_slug>/academy/<int:academy_id>/syllabus/'
         '<int:version>', SyllabusView.as_view(),
         name="certificate_slug_academy_id_syllabus_version"),
    path('certificate/<str:certificate_slug>/academy/<int:academy_id>/syllabus',
         SyllabusView.as_view(), name="certificate_slug_academy_id_syllabus"),

    path('catalog/timezones', get_timezones, name="timezones_all"),
]
