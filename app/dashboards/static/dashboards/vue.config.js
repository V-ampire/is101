const path = require('path');

module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  filenameHashing: false,
  pages: {
    admin: {
      // точка входа для страницы
      entry: 'src/admin/main.js',
      // исходный шаблон
      template: 'public/admin.html',
      // в результате будет dist/index.html
      filename: 'admin.html',
      // когда используется опция title, то <title> в шаблоне
      // должен быть <title><%= htmlWebpackPlugin.options.title %></title>
      title: 'Admin',
      // все фрагменты, добавляемые на этой странице, по умолчанию
      // это извлечённые общий фрагмент и вендорный фрагмент.
      chunks: ['chunk-vendors', 'chunk-common', 'admin'],
    }
  }
}