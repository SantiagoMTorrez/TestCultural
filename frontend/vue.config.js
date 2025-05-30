const { defineConfig } = require('@vue/cli-service')
const path = require('path');
module.exports = defineConfig({
    devServer: {
    host: '0.0.0.0',
    port: 8081,
    allowedHosts: 'all'
  },
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  }
})
