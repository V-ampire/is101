from accounts import emails

from celery.decorators import task
from typing import List


@task(bind=True)
def send_account_created_message(self, creator_uuid, message_fields: List[emails.MessageField]):
    """
    Отправить email с данными созданного аккаунта на почту пользователя создавшего его.
    """
    message = emails.CreatedEmail(creator_uuid, message_fields)
    message.send()