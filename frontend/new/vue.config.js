module.exports = {
    devServer: {
        port: 1024,
        disableHostCheck: true,
        proxy: {                  // redirect API request to testing sever 
            '^/api': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true,
                logLevel: 'debug',
                pathRewrite: {'^/api':'/'},
            },
        }
    },
}