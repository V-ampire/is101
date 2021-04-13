from django.template import loader
from django.core import mail

from accounts import factories
from accounts import emails

import pytest
from faker import Faker
from factory_generator import generate_to_dict


@pytest.mark.django_db
def test_get_subject():
    creator = factories.AdminUserAccountModelFactory()
    message = emails.CreatedEmail(creator.uuid, [])
    expected = loader.render_to_string('accounts/emails/created_account_subject_template.html')
    tested = message.get_subject()
    assert expected == tested


@pytest.mark.django_db
def test_get_message():
    creator = factories.AdminUserAccountModelFactory()
    account_data = generate_to_dict(factories.AdminUserAccountModelFactory)
    expected_fields = [
        emails.MessageField('Пароль', account_data['password']),
        emails.MessageField('Логин', account_data['username']),
    ]
    message = emails.CreatedEmail(creator.uuid, expected_fields)
    expected = loader.render_to_string(
        'accounts/emails/created_account_message_template.html', 
        {'fields': expected_fields}
    )
    tested = message.get_message()
    assert expected == tested
    

@pytest.mark.django_db
def test_send(mocker):
    mock_send = mocker.patch('accounts.emails.send_mail')
    creator = factories.AdminUserAccountModelFactory()
    account_data = generate_to_dict(factories.AdminUserAccountModelFactory)
    expected_fields = [
        emails.MessageField('Пароль', account_data['password']),
        emails.MessageField('Логин', account_data['username']),
    ]
    message = emails.CreatedEmail(creator.uuid, expected_fields)
    expected_subject = message.get_subject()
    expected_message = message.get_message()
    expected_from_email = None
    expected_fail_silently=False
    message.send()
    mock_send.assert_called_with(
        expected_subject,
        expected_message,
        expected_from_email,
        [creator.email],
        fail_silently=expected_fail_silently,
    )