import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
    server: {
         proxy: {
             '/api': {
                 target: 'http://127.0.0.1:5000',
                 changeOrigin: true,
                 rewrite: (path) => path.replace(/^\/api/, '')
             }
         },
        allowedHosts: ["client", "localhost"],
    },
    plugins: [
        vue(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
})
