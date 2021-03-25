import { 
  ApiClient, 
  EmployeeApiClient, 
  PositionsClient, 
  AccountsClient, 
  BranchesClient } from '@/core/services/http/base';


export function companiesApi() {
  const endpoint = '/companies';

  return new ApiClient(endpoint)
}


export function branchesApi(companyUuid) {
  const endpoint = `/companies/${companyUuid}/branches`;

  return new BranchesClient(endpoint)
}


export function employeesApi(companyUuid, branchUuid) {
  const endpoint = `/companies/${companyUuid}/branches/${branchUuid}/employees`;

  return new EmployeeApiClient(endpoint)
}


export function positionsApi() {
  const endpoint = '/positions';

  return new PositionsClient(endpoint)
}


export function companyAccountsApi() {
  const endpoint = '/accounts/companies';

  return new AccountsClient(endpoint)
}


export function employeeAccountsApi() {
  const endpoint = '/accounts/employees';

  return new AccountsClient(endpoint)
}