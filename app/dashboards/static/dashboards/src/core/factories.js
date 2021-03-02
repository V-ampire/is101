import config from '@/config';
import statuses from "@/core/services/statuses";
import roles from "@/core/services/accounts/roles";

import faker from 'faker';


function keyFromObject(object) {
  const keys = Object.keys(object);
  const index = Math.floor(Math.random() * keys.length)
  return keys[index]
}



export function UserDetailData () {
  /**
   * Фабрика данных учетной записи для ресурса информации о юрлице.
   */
  return {
    "username": faker.internet.userName(),
    "uuid": faker.random.uuid(),
    "role": keyFromObject(roles),
    "is_active": keyFromObject({true: true, false: false})
  }
}


export function CompanyDataForList(fields={}) {
  const uuid = faker.random.uuid();

  return {
    "uuid": uuid || fields.uuid,
    "url": `${config.apiRoot}/companies/${uuid}/` || fields.url,
    "city": faker.address.city() || fields.city,
    "address": faker.address.streetAddress() || fields.address,
    "title": faker.company.companyName() || fields.title,
    "status": keyFromObject(statuses) || fields.status
  }
}


export function CompanyListData (n) {
  /**
   * Фабрика данных юрлица для ресурса списка.
   */
  let companiesList = [];

  for(let i = 0; i < n; i++) {
    companiesList.push(CompanyDataForList());
  };

  return companiesList
}


export function CompanyDetailData() {
  /**
   * Фабрика данных юрлица для ресурса подробной информации.
   */
  const uuid = faker.random.uuid()
  let branches = [];
  const length = 5;

  for(let i = 0; i < length; i++) {
    branches.push(BranchListData());
  };

  return {
    "uuid": uuid,
    "user": UserDetailData(),
    "title": faker.company.companyName(),
    "logo": faker.image.imageUrl(),
    "tagline": faker.lorem.sentence(),
    "inn": String(faker.random.number()),
    "ogrn": String(faker.random.number()),
    "city": faker.address.city(),
    "address": faker.address.streetAddress(),
    "email": faker.internet.email(),
    "phone": faker.phone.phoneNumber(),
    "url": `${config.apiRoot}/companies/${uuid}/`,
    "branches": branches,
    "status": keyFromObject(statuses)
  }
}


export function BranchListData() {
  /**
   * Фабрика данных филиала для ресурса информации о юрлице.
   */
  const uuid = faker.random.uuid()

  return {
    "uuid": uuid,
    "url": `${config.apiRoot}/companies/${faker.random.uuid()}/branches/${uuid}`,
    "city": faker.address.city(),
    "address": faker.address.streetAddress(),
    "phone": faker.phone.phoneNumber(),
    "status": keyFromObject(statuses)
  }
}