import statuses from "@/core/services/statuses";
import roles from "@/core/services/accounts/roles";

import faker from 'faker';


function randomFromObject(object) {
  const keys = Object.keys(object);
  const index = Math.floor(Math.random() * keys.length)
  return object[keys[index]]
}


export function CompanyUserData(fields=[]) {
  const companyData = {
    uuid: faker.random.uuid(),
    username: faker.internet.userName(),
    is_active: faker.random.boolean(),
    role: roles.company,
    is_staff: false,
    date_joined: faker.date.past(),
  };

  if (fields.length > 0) {
    if (fields.indexOf('uuid') == -1) {
      delete companyData.uuid
    }
    if (fields.indexOf('username') == -1) {
      delete companyData.username
    }
    if (fields.indexOf('is_active') == -1) {
      delete companyData.is_active
    }
    if (fields.indexOf('role') == -1) {
      delete companyData.role
    }
    if (fields.indexOf('is_staff') == -1) {
      delete companyData.is_staff
    }
    if (fields.indexOf('date_joined') == -1) {
      delete companyData.date_joined
    }
  }
  return companyData
}


export function CompanyProfileData(fields=[]) {

  const companyData = {
    "uuid": faker.random.uuid(),
    "title": faker.company.companyName(),
    "logo": faker.image.imageUrl(),
    "tagline": faker.lorem.sentence(),
    "inn": String(faker.random.number()),
    "ogrn": String(faker.random.number()),
    "city": faker.address.city(),
    "address": faker.address.streetAddress(),
    "email": faker.internet.email(),
    "phone": faker.phone.phoneNumber(),
    "status": randomFromObject(statuses)
  };

  if (fields.length > 0) {
    if (fields.indexOf('uuid') == -1) {
      delete companyData.uuid
    }
    if (fields.indexOf('title') == -1) {
      delete companyData.title
    }
    if (fields.indexOf('logo') == -1) {
      delete companyData.logo
    }
    if (fields.indexOf('tagline') == -1) {
      delete companyData.tagline
    }
    if (fields.indexOf('inn') == -1) {
      delete companyData.inn
    }
    if (fields.indexOf('ogrn') == -1) {
      delete companyData.ogrn
    }
    if (fields.indexOf('city') == -1) {
      delete companyData.city
    }
    if (fields.indexOf('address') == -1) {
      delete companyData.address
    }
    if (fields.indexOf('phone') == -1) {
      delete companyData.phone
    }
    if (fields.indexOf('status') == -1) {
      delete companyData.status
    }
  }
  return companyData
}
