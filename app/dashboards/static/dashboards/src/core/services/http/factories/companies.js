/**
 * Фабрики данных для ресурсов api юрлиц.
 */
import config from '@/config';
import statuses from "@/core/services/statuses";
import roles from "@/core/services/accounts/roles";

import faker from 'faker';
import { randomKeyFromObject } from '@/core/services/http/factories/utils'


export function UserDetailData (fields={}) {
  /**
   * Фабрика данных учетной записи для ресурса информации о юрлице.
   */
  return {
    "username": faker.internet.userName() || fields.username,
    "uuid": faker.random.uuid() || fields.uuid,
    "role": randomKeyFromObject(roles) || fields.role,
    "is_active": randomKeyFromObject({true: true, false: false}) || fields.is_active
  }
}


export function CompanyDetailDataAdmin (fields={}) {
  /**
   * Возвращает подробную информацию о юрлице для админов.
   */
  const uuid = faker.random.uuid() || fields.uuid

  return {
    'uuid': uuid,
    'user': UserDetailData() || fields.user,
    'title': faker.company.companyName() || fields.title,
    'logo': faker.image.imageUrl() || fields.logo,
    'tagline': faker.lorem.sentence() || fields.tagline,
    'inn': String(faker.random.number()) || fields.inn,
    'ogrn': String(faker.random.number()) || fields.ogrn,
    'city': faker.address.city() || fields.city,
    'address': faker.address.streetAddress() || fields.address,
    'email': faker.internet.email() || fields.email,
    'phone': faker.phone.phoneNumber() || fields.phone,
    'url': `${config.apiRoot}/companies/${uuid}/` || fields.url,
    //'branches': branches || fields.branches,
    'status': randomKeyFromObject(statuses) || fields.status,
  }
}


 export function CompaniesListDataAdmin (count=1) {
    /**
    * Возвращает список юрлиц для админов.
    * @count - количество компаний в списке
    */
    let companiesList = [];

    for(let i = 0; i < count; i++) {
      const company = CompanyDetailDataAdmin();
      companiesList.push({
        "uuid": company.uuid,
        "url": company.url,
        "city": company.city,
        "address": company.address,
        "title": company.title,
        "status": company.status,
      });
    };
    return companiesList
 }


 export function CompanyCreateData (fields={}) {
   /**
    * Возвращает данные для создания юрлица.
    */
    const company = CompanyDetailDataAdmin();
    return {
      'user': faker.random.uuid() || fields.user,
      'title': company.title,
      'logo': company.logo,
      'tagline': company.tagline,
      'inn': company.inn,
      'ogrn': company.ogrn,
      'city': company.city,
      'address': company.address,
      'email': company.email,
      'phone': company.phone,
    }
 }
 