
import { createApp } from 'vue'
import App from './App.vue'
import Home from './pages/Home.vue'
import {createRouter, createWebHistory} from "vue-router";
import DevLogin from "@/pages/DevLogin.vue";
import Queue from "@/pages/Queue.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Home},
        { path: '/dev-login', component: DevLogin},
        { path: '/queue', component: Queue}
    ]
})

const app = createApp(App)

app.use(router)

app.mount('#app')

