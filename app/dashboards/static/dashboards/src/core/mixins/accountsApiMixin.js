/**
 * 
 */

import { companyAccountsApi, employeeAccountsApi, adminAccountsApi } from '@/core/services/http/clients';
import roles from '@/core/services/roles';


export default {
  props: {
    accountRole: String
  },
  computed: {
    api() {
      if (this.accountRole === roles.company[0]) {
        return companyAccountsApi()
      } else if (this.accountRole === roles.employee[0]) {
        return employeeAccountsApi()
      } else if (this.accountRole === roles.admin[0]) {
        return adminAccountsApi()
      } else {
        throw Error('Не определена роль учетной записи.')
      }
    }
  },

}