// Допустим имею такую структуру проекта:
// | - components/
//         ItemListTable.vue
// | - services/
//          http.js

// // ItemListTable.vue
// ...
// import api from '@/services/http'
// export default {
//   data () {
//     return {
//       headers: [
//         {text: 'Название', value: 'title'},
//         {text: 'Город', value: 'city' },
//         {text: 'Адрес', value: 'address' },    
//       ],
//       items: [],
//     }
//   },
//   mounted () {
//     this.getItems();
//   },
//   methods: {
//     async getItems () {
//       this.items = await api.getAll();
//     }
//   }
// }

// // http.js
// export default {
//   getAll() {
//     return axios.get('http://myapi/items')
//   }
// }

// // test.spes.js
// var faker = require('faker');

// const fakeCompanies = [
//   {
//     title: faker.company.companyName(),
//     city: faker.address.city(),
//     address: faker.address.streetAddress(),
//   },
//   {
//     title: faker.company.companyName(),
//     city: faker.address.city(),
//     address: faker.address.streetAddress(),
//   }
// ]

// jest.doMock('@/services/http/companies', () => {
//   return {
//     getAll: jest.fn().mockResolvedValue(fakeCompanies)
//   }
// });

// const localVue = createLocalVue();

// describe("Тест для компонента ItemListTable.vue", () => {

//   it("Инициализация компонента с данными от метода getItems()", () => {
//     const wrapper = shallowMount(ItemListTable, {
//       localVue,
//     });
//     const itemsTable = wrapper.findComponent(ItemListTable);

//     expect(itemsTable.exists()).toBe(true)

//   });
// })