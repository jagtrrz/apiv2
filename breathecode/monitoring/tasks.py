from django.utils import timezone
from celery import shared_task, Task
from .actions import run_app_diagnostic, run_script, run_endpoint_diagnostic
from .models import Application, MonitorScript, Endpoint
from breathecode.notify.actions import send_email_message, send_slack_raw
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    #                                           seconds
    retry_kwargs = {'max_retries': 5, 'countdown': 60 * 5 }
    retry_backoff = True

# @shared_task(bind=True, base=BaseTaskWithRetry)
# def monitor_app(self,app_id):
#     logger.debug("Starting monitor_app")
#     app = Application.objects.get(id=app_id)

#     now = timezone.now()
#     if app.paused_until is not None and app.paused_until > now:
#         logger.debug(f"Ignoring App: {app.title} monitor because its paused")
#         return True

#     logger.debug(f"Running diagnostic for: {app.title} ")
#     result = run_app_diagnostic(app)
#     if result["status"] != "OPERATIONAL":
#         if app.notify_email:
#             send_email_message("diagnostic", app.notify_email, {
#                 "subject": f"Errors have been found on {app.title} diagnostic",
#                 "details": result["details"]
#             })

#         if (app.notify_slack_channel and app.academy and
#                 hasattr(app.academy, 'slackteam') and
#                 hasattr(app.academy.slackteam.owner, 'credentialsslack')):
#             send_slack_raw(
#                 "diagnostic",
#                 app.academy.slackteam.owner.credentialsslack.token,
#                 app.notify_slack_channel.slack_id, {
#                     "subject": f"Errors have been found on {app.title} diagnostic",
#                     **result,
#                 }
#             )

#         return False

#     return True

@shared_task(bind=True, base=BaseTaskWithRetry)
def test_endpoint(self, endpoint_id):
    logger.debug("Starting monitor_app")
    endpoint = Endpoint.objects.get(id=endpoint_id)

    now = timezone.now()
    if endpoint.paused_until is not None and endpoint.paused_until > now:
        logger.debug(f"Ignoring App: {endpoint.url} monitor because its paused")
        return True

    logger.debug(f"Running diagnostic for: {endpoint.url} ")
    result = run_endpoint_diagnostic(endpoint.id)
    if result["status"] != "OPERATIONAL":
        if endpoint.application.notify_email:
            send_email_message("diagnostic", endpoint.application.notify_email, {
                "subject": f"Errors have been found on {endpoint.application.title} diagnostic",
                "details": result["details"]
            })

        if (endpoint.application.notify_slack_channel and endpoint.application.academy and
                hasattr(endpoint.application.academy, 'slackteam') and
                hasattr(endpoint.application.academy.slackteam.owner, 'credentialsslack')):
            send_slack_raw(
                "diagnostic",
                endpoint.application.academy.slackteam.owner.credentialsslack.token,
                endpoint.application.notify_slack_channel.slack_id, {
                    "subject": f"Errors have been found on {endpoint.application.title} diagnostic",
                    **result,
                }
            )

@shared_task(bind=True, base=BaseTaskWithRetry)
def monitor_app(self, app_id):
    logger.debug("Starting monitor_app")
    endpoints = Endpoint.objects.filter(application__id=app_id).values_list('id', flat=True)

    for endpoint_id in endpoints:
        test_endpoint.delay(endpoint_id)

@shared_task(bind=True, base=BaseTaskWithRetry)
def execute_scripts(self, script_id):
    logger.debug("Starting execute_scripts")
    script = MonitorScript.objects.get(id=script_id)
    app = script.application

    now = timezone.now()
    if script.paused_until is not None and script.paused_until > now:
        logger.debug("Ignoring script ex because its paused")
        return True

    result = run_script(script)
    if result["status"] != "OPERATIONAL":
        if app.notify_email:
            send_email_message("diagnostic", app.notify_email, {
                "subject": f"Errors have been found on {app.title} script {script.id} (slug: {script.script_slug})",
                "details": result["text"]
            })
        if (app.notify_slack_channel and app.academy and
                hasattr(app.academy, 'slackteam') and
                hasattr(app.academy.slackteam.owner, 'credentialsslack')):
            try:
                send_slack_raw(
                    "diagnostic",
                    app.academy.slackteam.owner.credentialsslack.token,
                    app.notify_slack_channel.slack_id, {
                        "subject": f"Errors have been found on {app.title} script {script.id} (slug: {script.script_slug})",
                        **result,
                    }
                )
            except Exception:
                return False
        return False

    return True
