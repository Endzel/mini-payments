import hashlib
import logging

from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError as MKApiClientError
from mailchimp_transactional import Client as TransactionalClient
from mailchimp_transactional.api_client import ApiClientError as TransacApiClientError
from rest_framework import status

from my_module.exceptions import CustomException

log = logging.getLogger("my_module")


class Mailchimp(object):
    """
    Main handler class that manages the integration with Mailchimp's Transactional API.
    Its purpose will mainly be to send automated emails using existing templates filled with context.
    """

    def __init__(self):
        self.__client = TransactionalClient(settings.MANDRILL_API_KEY)

    def build_static_content(self):
        return {
            "STATIC_MAILING": settings.STATIC_MAILING,
            "MYCOMPANY_URL": settings.MYCOMPANY_URL,
            "MYCOMPANY_LOGO": settings.MYCOMPANY_LOGO,
            "APP_STORE_BUTTON": settings.APP_STORE_BUTTON,
            "GOOGLE_PLAY_BUTTON": settings.GOOGLE_PLAY_BUTTON,
            "SHARE_URL": settings.SHARE_URL,
        }

    def build_attachments_list(self, attachments: list):
        # Expects a list of objects typed PDF files.
        attachments_list = []
        for attachment in attachments:
            attachments_list.append(
                {
                    "type": "application/pdf",
                    "name": attachment["filename"],
                    "content": attachment["file"],
                }
            )
        return attachments_list

    def build_recipient_list(self, email_list: list):
        recipient_list = []
        if settings.ENVIRONMENT in ["Dev", "Local"]:
            email_list = settings.BACKEND_EMAIL_LIST
        elif settings.ENVIRONMENT in ["Qa"]:
            email_list = settings.QA_EMAIL_LIST
        elif settings.ENVIRONMENT in ["Test"]:
            email_list = settings.TESTING_EMAIL_LIST

        for email in email_list:
            recipient_list.append({"email": email, "name": "", "type": "to"})

        return recipient_list

    def format_global_merge_vars(self, context: dict):
        global_merge_vars = []
        for key in context.keys():
            global_merge_vars.append({"name": key, "content": context[key]})
        return global_merge_vars

    def send_message_using_template(
        self,
        template_name: str,
        context: dict,
        email_list: list,
        subject: str = None,
        language: str = None,
        attachments: list = None,
        *args,
        **kwargs,
    ):
        try:
            if language:
                template_name = f"{template_name}-{language}"
            template_args = {
                "template_name": template_name,
                "template_content": [{}],
                "message": {
                    "from_email": settings.FROM_MAILCHIMP_EMAIL,
                    "from_name": "MyCompany",
                    "merge_language": "handlebars",
                    "to": self.build_recipient_list(email_list),
                    "global_merge_vars": self.format_global_merge_vars(context),
                },
            }
            if subject:
                template_args["message"]["subject"] = subject
            if attachments:
                template_args["message"]["attachments"] = self.build_attachments_list(
                    attachments
                )
            response = self.__client.messages.send_template(template_args)
            log.debug("Message using template sent successfully: {}".format(response))
            return response
        except TransacApiClientError as error:
            log.info(f"An exception occurred: {error.text}")
            raise CustomException(
                detail=error.text,
                code="send_message_using_template",
                http_status_code=status.HTTP_400_BAD_REQUEST,
            )

    def ping(self, *args, **kwargs):
        try:
            response = self.__client.users.ping()
            log.debug("API called successfully: {}".format(response))
        except TransacApiClientError as error:
            log.warning("An exception occurred: {}".format(error.text))
            raise CustomException(
                detail=error.text,
                code="mailchimp_ping",
                http_status_code=status.HTTP_400_BAD_REQUEST,
            )
