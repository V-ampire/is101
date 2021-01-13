# Учетные записи

- [Юрлица](#companies)
- [Работники](#employees)


<a name="companies"></a>
## Юрлица.


### Ресурсы

- `/accounts/companies/`

Доступ: Администраторы.

Методы:

- GET - Возвращает список учетных записей юрлиц.
- POST - Создает учетную запись для юрлица.


- `/accounts/companies/{uuid}/`

Доступ: Администраторы.

Методы:

- GET - Информация об учетной записи юрлица.
- PATCH - Обновить информацию об учетной записи юрлица, обновление пароля недоступно.
- DELETE - Удалить учетную запись


- `/accounts/companies/{uuid}/change-password/`

Доступ: Администраторы.

Методы:

- POST - Изменить пароль учетной записи.


- `/accounts/companies/{uuid}/deactivate/`

Доступ: Администраторы.

Методы:

- GET - Деактивировать учетную запись, вход в систему станет недоступен.


- `/accounts/companies/{uuid}/activate/`

Доступ: Администраторы.

Методы:

- GET - Активировать учетную запись, вход в систему станет доступен.



<a name="employees"></a>
## Работники

- `/accounts/employees/`

Администраторы.

`/accounts/employees/{uuid}/`
`/accounts/employees/{uuid}/change-password/`
`/accounts/employees/{uuid}/deactivate/`
