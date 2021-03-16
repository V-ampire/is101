/**
 * Фабрики для ресурсов API
 */
import { CompanyUserData, CompanyProfileData } from '@/core/factories';
import config from '@/config';


export const CompanyApi = {
  list(count) {
    let companiesList = [];

    for(let i = 0; i < count; i++) {
      const company = CompanyProfileData([
        'uuid',
        'city',
        'address',
        'title',
        'status'
      ]);
      company.url = `${config.apiRoot}/companies/${company.uuid}/`;
      companiesList.push(company);
    };
    return companiesList
  },
  detail() {
    const company = CompanyProfileData([
      'uuid',
      'title',
      'logo',
      'tagline',
      'inn',
      'ogrn',
      'city',
      'address',
      'email',
      'phone',
      //'branches',
      'status',
    ]);
    company.user = CompanyUserData(['username', 'uuid', 'role', 'is_active'])
    company.url = `${config.apiRoot}/companies/${company.uuid}/`;
    return company
  },
  create() {
    const company = CompanyProfileData([
      'uuid',
      'title',
      'logo',
      'tagline',
      'inn',
      'ogrn',
      'city',
      'address',
      'email',
      'phone',
      //'branches',
      'status',
    ]);
    company.user = CompanyUserData(['username', 'uuid', 'role', 'is_active'])
    company.url = `${config.apiRoot}/companies/${company.uuid}/`;
    return company
  }
}


export const AccountsApi = {
  companies: {
    list(count) {
      const accountsList = [];
      for(let i = 0; i < count; i++) {
        const account = CompanyUserData([
          'username', 'uuid', 'password', 'is_active'
        ]);
        accountsList.push(account);
      }
      return accountsList
    },

    detail() {
      return CompanyUserData([
        'username', 'uuid', 'password', 'is_active'
      ])
    }
  }
}