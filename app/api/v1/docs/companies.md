# Юрлица


[/companies/](#companies-list)

[/companies/{uuid}/](#companies-detail)

[/companies/{uuid}/archivate/](#companies-archivate)

[/companies/{uuid}/activate/](#companies-activate)


`/companies/{uuid}/branches/`
`/companies/{uuid}/branches/{uuid}`
`/companies/{uuid}/branches/{uuid}/archivate/`
`/companies/{uuid}/branches/{uuid}/activate/`


<a name="companies-list"></a>
## /companies/

Методы:

- `GET`

Доступ у админов.

Пример ответа для админов.
```
[
    {
        'uuid': '4395f795-8632-4126-907c-451d921cbc45',
        'url': 'http://testserver/api/v1/companies/4395f795-8632-4126-907c-451d921cbc45/', 'city': 'Port Adammouth',
        'address': '2540 Wright Burg Suite 133\nPort Lindsayhaven, AK 58521',
        'title': 'Rodriguez-Riley',
        'status': 1
    },
    {
        'uuid': 'ad9dd353-850e-4eb6-9a66-bac55441f9a1',
        'url': 'http://testserver/api/v1/companies/ad9dd353-850e-4eb6-9a66-bac55441f9a1/', 'city': 'Hughesview',
        'address': 'PSC 4604, Box 6536\nAPO AE 66132',
        'title': 'Buck, Nielsen and Miller',
        'status': 1
    },
    {
        'uuid': '6614cc27-7680-4bda-bbec-ead77471ee42',
        'url': 'http://testserver/api/v1/companies/6614cc27-7680-4bda-bbec-ead77471ee42/', 'city': 'Lake Karenburgh',
        'address': '5790 Thompson Passage\nEnglishville, MD 84150',
        'title': 'Nicholson PLC',
        'status': 1
    }
]
```

- `POST`

Доступ у админов.

Примерные данные:
```
{
    'title':
    'Casey, Martinez and Smith',
    'inn': 'iGHQIrbISLWf',
    'ogrn': 'OyaRmIEoiZEyLrF',
    'city': 'South James',
    'address': '9203 Carla Valley\nNorth Jonathanhaven, IL 66255',
    'email': 'courtneywilliams@kelly.com',
    'phone': '308-312-1104x99951',
    'logo': <File: answer.jpg>,
    'tagline': 'Versatile global success',
    'user': '0a5e9616-0d1d-4bbd-a790-4fd3b5e14bcc'
}
```

Примерный ответ:
```
{
    'user': 'gibsondaniel',
    'title': 'Casey, Martinez and Smith',
    'logo': 'http://testserver/media/logo/2020/12/30/answer_DL1UGNA.jpg',
    'tagline': 'Versatile global success',
    'inn': 'iGHQIrbISLWf',
    'ogrn': 'OyaRmIEoiZEyLrF',
    'city': 'South James',
    'address': '9203 Carla Valley\nNorth Jonathanhaven, IL 66255',
    'email': 'courtneywilliams@kelly.com',
    'phone': '308-312-1104x99951'
}
```

Ошибки:

- Ошибка учетной записи:
```
{'user': ['Учетная запись не зарегистрирована']}
```

- Ошибка в данных:
```
{'title': ['Обязательное поле.']}
```


<a name="companies-detail"></a>
## /companies/{uuid}/

Методы:

- `GET`

Доступ у админов и допущенных лиц.

Примерный ответ для админов:
```
{
    'uuid': '4afa42e3-06aa-4257-af0b-708fffea5c18',
    'user': {
        'username': 'jacobbrown',
        'uuid': '6333bd75-9b1c-407e-807a-1e744bfb33bd'
    },
    'title': 'Johnson and Sons',
    'logo': 'http://testserver/media/logo/2020/12/30/yard_ONwDztJ.jpg',
    'tagline': 'Fully-configurable bandwidth-monitored success',
    'inn': 'PmpFXLjKGCJb',
    'ogrn': 'tjhIzKjGqXtiKos',
    'city': 'Port Mark',
    'address': '4319 Gardner Corner\nPort Brittanyhaven, WI 71435',
    'email': 'huntergriffith@johnson.org',
    'phone': '001-173-595-0094x4141',
    'url': 'http://testserver/api/v1/companies/4afa42e3-06aa-4257-af0b-708fffea5c18/',
    'branches': []
}
```


Примерный ответ для допущенных лиц:
```
{
    'title':
    'Miller Group',
    'logo': 'http://testserver/media/logo/2020/12/30/send_CfIEaY7.jpg',
    tagline': 'Exclusive context-sensitive service-desk',
    'inn': 'XxcXNMpKPdKi',
    'ogrn': 'xmBBuxeAdQIqmbz',
    'city': 'Morrisborough',
    'address': '862 Crystal Fork Suite 070\nWest Shaun, WI 38515',
    'email': 'jblackwell@campos.net',
    'phone': '0674770746',
    'branches': []
}
```

- `PATCH`

Доступ у админов и допущенных лиц.

Примерный ответ для админов:
```
{
    'uuid': 'c2eab563-7859-4157-996a-a101e01ad666',
    'user': {
        'username': 'shannonjacob',
        'uuid': '9c5a9382-45c5-4087-935e-d75f167f4cfe'
    },
    'title': 'Sanchez, Castillo and Meyer',
    'logo': 'http://testserver/media/logo/2020/12/31/beat_DoCIZEx.jpg',
    'tagline': 'Balanced dynamic initiative',
    'inn': 'wYvOHhcBBfAa',
    'ogrn': 'TsvQavbzRXUIhEf',
    'city': 'West Josephview',
    'address': '752 James Common\nPort Zacharyland, KS 29943',
    'email': 'carl70@sharp-carrillo.com',
    'phone': '+1-220-985-7871x99477',
    'url': 'http://testserver/api/v1/companies/c2eab563-7859-4157-996a-a101e01ad666/',
    'branches': []
}
```

Примерный ответ для допущенных лиц:
```
{
    'title': 'Morton Ltd',
    'logo': 'http://testserver/media/logo/2020/12/31/beat_5CFMSQk.jpg',
    'tagline': 'De-engineered real-time algorithm',
    'inn': 'BgxyHHmcwbyl',
    'ogrn': 'NUOMniHowCzAnoW',
    'city': 'Smithshire',
    'address': '506 Griffin Mountains\nNorth Brianfort, NY 25363',
    'email': 'timothymccarthy@chapman.biz',
    'phone': '(821)549-0116x87926',
    'branches': []
}
```

- `DELETE`

Доступ только у админов.

При удалении юрлица будет одновременно удалена учетная запись.


<a name="companies-archivate"></a>
## /companies/{uuiu}/archivate/

Меняет статус объекта на `company.Company.ARCHIVED`

Метод `GET`

Доступ только у админов.

Ответ {'status': 'ok}


<a name="companies-activate"></a>
## /companies/{uuiu}/activate/

Меняет статус объекта на `company.Company.ACTIVE`

Метод `GET`

Доступ только у админов.

Ответ {'status': 'ok}

