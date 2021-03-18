import { ApiClient, EmployeeApiClient, PositionsClient } from '@/core/services/http/base';


export function companiesApi() {
  const endpoint = '/companies';

  return new ApiClient(endpoint)
}


export function branchesApi(companyUuid) {
  const endpoint = `/companies/${companyUuid}/branches`;

  return new ApiClient(endpoint)
}


export function employeesApi(companyUuid, branchUuid) {
  const endpoint = `/companies/${companyUuid}/branches/${branchUuid}/employees`;

  return new EmployeeApiClient(endpoint)
}


export function positionsApi() {
  const endpoint = '/positions';

  return new PositionsClient(endpoint)
}