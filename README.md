# CRM система для управления сервисными центрами по ремонту техники


## Тебования

`python 3.6+`


## Деплоймент

### Клонируем проект

`git clone git@github.com:V-ampire/is101.git`

### Виртуальное окружение

`virtualenv .venv`

`cd app ; pip install -r requirements.txt`

`source .venv/bin/activate`


### Настраиваем django-приложение

Создать файл .env:
```
SECRET_KEY=
DEBUG=off
ALLOWED_HOSTS=
DB_NAME=
DB_USER=
DB_PASSWORD=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=true
```

Модуль настроек:

`export DJANGO_SETTINGS_MODULE=config.settings.prod`

База данных и статика:

```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

Добавляем конфиги:
```
sudo ln -s $project_path/nginx/is101.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/systemd/gunicorn.socket /etc/systemd/system/
sudo ln -s $project_path/systemd/gunicorn.service /etc/systemd/system/
sudo ln -s $project_path/systemd/celery.service /etc/systemd/system/

sudo systemctl daemon-reload ; \
sudo systemctl start gunicorn ; \
sudo systemctl enable gunicorn ; \
sudo systemctl start celery ; \
sudo systemctl enable celery ; \
sudo service nginx restart
```


## Роли пользователей

- [Администратор](#role_admin)
- [Юр. лицо](#role_company)
- Работник


<a name="role_admin"></a>
### Администратор

- Администратор может создавать, редактировать и удалять юр. лица и работников, а также учетные записи для них.

- Администратор не может создавать, редактировать или удалять других админинстраторов, а также учетные записи для них.

- Администратор может редактировать следующие поля юр. лиц:
    - Учетную запись (логин, пароль)
    - Данные о юр. лице (ИНН, ОГРН, адрес и т.д.)
    - Филиалы

Вход: `/accounts/login/admin/`


<a name="role_company"></a>
### Юр. лицо

- Юр. лицо может редактировать следующую информацию о себе:
    - Данные о юр. лице (ИНН, ОГРН, адрес и т.д.)
    - Юрлицо **не может** менять свою учетную запись.
    - Юрлицо может добавлять свои филиалы.



## Вход в систему

При входе:
- Проверяется роль учетной записи
-


