module.exports = {
    devServer: {
        proxy: {
            '/api': {
                port: 8000,
                target: 'http://localhost:8000/',
                changeOrigin: true
            },
        }
    }
}