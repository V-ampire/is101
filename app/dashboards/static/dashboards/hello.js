
//console.log(accounts.companies.list())

import('./src/core/services/http/accounts.js')
  .then((module) => {
    console.log(module);
  });
