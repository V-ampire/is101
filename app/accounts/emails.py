from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template import loader

from typing import NamedTuple, List, Optional
import logging


logger = logging.getLogger(__name__)


class MessageField(NamedTuple):
    """
    Класс для поля учетной записи.
    Содержит описание поля и значение, например ('Пароль', 'qwererty123')
    """
    label: str
    value: str


class CreatedEmail():
    """
    Ссообщение на email пользователя создавшего учетную запись.
    """
    default_message_template = 'accounts/emails/created_account_message_template.html'
    default_subject_template = 'accounts/emails/created_account_subject_template.html'

    def __init__(self, creator_uuid: str, fields: List[MessageField], 
                    message_template: Optional[str]=None, 
                    subject_template: Optional[str]=None) -> None:
        """
        Инициализация.
        :param creator_uuid: UUID пользователя создавшего учетную запись.
        :param field: Поля учетной записи, которые будут отображены в письме.
        """
        self.creator = get_user_model().objects.get(uuid=creator_uuid)
        self.fields = fields
        self.message_template = message_template if message_template else self.default_message_template
        self.subject_template = subject_template if subject_template else self.default_subject_template

    def get_subject(self):
        return loader.render_to_string(self.subject_template)

    def get_message(self):
        import pdb; pdb.set_trace()
        return loader.render_to_string(self.message_template, {'fields': self.fields})

    def send(self, subject: Optional[str]=None, message: Optional[str]=None, **kwargs):
        subject = subject if subject else self.get_subject()
        message = message if message else self.get_message()
        from_email = None
        return send_mail(
            subject, 
            message, 
            from_email, 
            [self.creator.email],
            fail_silently=False, 
            **kwargs
        )


def get_email_fields(serializer, include=[]):
    """
    Формирует список полей для email из данных сериалайзера.
    :param serializer: Экземпляр сериалайзера.
    :param include: Поля которые необходимо включить.
    """
    try:
        serializer_data = serializer.initial_data
    except AttributeError:
        logger.warning(
            f'Serializer {serializer} has no initial_data. Email will not contain information.'
        )
        return []

    fields = []
    for field_name in serializer.fields.keys():
        if include and field_name in include:
            fields.append(MessageField(
                label=serializer.fields[field_name].label,
                value=serializer_data[field_name]
            ))
    return fields