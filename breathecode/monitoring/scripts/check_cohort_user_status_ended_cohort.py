#!/usr/bin/env python
"""
Checks for cohort users with status active on ended cohort
"""
from breathecode.utils import ScriptNotification
from breathecode.admissions.models import CohortUser
from django.utils import timezone

active_user_on_ended_cohort = CohortUser.objects.filter(
    cohort__stage="ENDED", educational_status="ACTIVE", cohort__academy__id=academy.id)

active_user_on_ended_cohort_list = [
    "- " + item.user.first_name + " " + item.user.last_name + " (" +item.user.email + ") => " + item.cohort.name for item in active_user_on_ended_cohort]

active_user_on_ended_cohort_list_names = (
    "\n").join(active_user_on_ended_cohort_list)

if len(active_user_on_ended_cohort_list):
    raise ScriptNotification(
        f"This users: {active_user_on_ended_cohort_list_names} are active on ended cohorts")

print("Everything up to date")
