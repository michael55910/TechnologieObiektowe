module.exports = {
    devServer: {
        proxy: {
            '/': {
                port: 8000,
                target: 'http://localhost:8000/api',
                changeOrigin: true
            },
        }
    }
}