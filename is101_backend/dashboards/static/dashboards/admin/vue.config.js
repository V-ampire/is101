module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  filenameHashing: false,
  // удаление плагинов webpack связанных с HTML
  chainWebpack: config => {
    config.plugins.delete('html')
    config.plugins.delete('preload')
    config.plugins.delete('prefetch')
  },
  configureWebpack: {
    devtool: 'source-map'
  }
}