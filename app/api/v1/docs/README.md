# Документация по API


## Должности

`/positions/`
`/positions/{uuid}/`
`/positions/{uuid}/archivate/`
`/positions/{uuid}/activate/`


## Юрлица


`/companies/`

`/companies/{uuid}/`

`/companies/{uuid}/archivate/`

`/companies/{uuid}/activate/`


## Филиалы

`/companies/{uuid}/branches/`
`/companies/{uuid}/branches/{uuid}`
`/companies/{uuid}/branches/{uuid}/archivate/`
`/companies/{uuid}/branches/{uuid}/activate/`


## Работники

`/companies/{uuid}/branches/{uuid}/employees/`
`/companies/{uuid}/branches/{uuid}/employees/{uuid}/`
`/companies/{uuid}/branches/{uuid}/employees/{uuid}/archivate/`
`/companies/{uuid}/branches/{uuid}/employees/{uuid}/activate/`
`/companies/{uuid}/branches/{uuid}/employees/{uuid}/change-position/`


## accounts

Ресурс для действий [аккаунтами](../accounts/README.md).

Назначение:
- Создание/чтение/удаление учетных записей
- Отключение/включение учетных записей
- Изменение пароля


## companies

Ресурс для действий с [юрлицами](./companies.md)

Назначение:
- Создание/чтение/изменение/удаление юрлиц.


## positions

Ресурс для действий с [должностями](./positions.md)
