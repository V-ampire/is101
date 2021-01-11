# Должности

Должности являются общими для всех юрлиц и филиалов.


[/positions/](#positions-list)

[/positions/{uuid}/](#positions-detail)

[/positions/{uuid}/archivate/](#positions-archivate)

[/positions/{uuid}/activate/](#positions-activate)


<a name="positions-list"></a>
## /positions/

Методы:

- `GET`

Админам доступен полный доступ.

Для юрлиц доступен только список активных должностей.

Пример ответа для админов:
```
[
    {
        'uuid': '40f9f536-d7e2-46cc-bb69-89405e20166e',
        'title': 'Producer, television/film/video',
        'status': 1
    },
    {
        'uuid': 'dfa7c77b-b284-4d21-a9bd-ea3268231c9e',
        'title': 'Armed forces logistics/support/administrative officer',
        'status': 1
    },
    {
        'uuid': '83c147f0-e910-4a2e-8d4c-fdce1e6cc2dc',
        'title': 'Therapist, nutritional',
        'status': 0
    },
    {
        'uuid': '4ee62832-b586-450b-a15d-4ed1abdebf00',
        'title': 'Retail manager',
        'status': 0
    },
    {
        'uuid': 'd8483702-21bc-4acc-b231-40130b58ef1c',
        'title': 'Astronomer',
        'status': 0
    }
]
```

Пример ответа для юрлиц:
```
[
    {
        'uuid': '966d61b4-82c4-4e97-b4ae-fc6830bae5c4',
        'title': 'Police officer',
        'status': 1
    },
    {
        'uuid': '4b23c05a-af08-4cfc-8876-e9f9fb43849d',
        'title': 'Facilities manager',
        'status': 1
    },
    {
        'uuid': '613e175a-6984-4c47-8e33-2139d752afec',
        'title': 'Building control surveyor',
        'status': 1
    }
]
```

