
import { createApp } from 'vue'
import App from './App.vue'
import Home from './pages/Home.vue'
import {createRouter, createWebHistory} from "vue-router";
import DevLogin from "@/pages/DevLogin.vue";
import Queue from "@/pages/Queue.vue";
import ManageCourse from "@/pages/ManageCourse.vue";
import Swipe from "@/pages/Swipe.vue";
import SwipeAuth from "@/pages/SwipeAuth.vue";
import AppLayout from "@/layouts/AppLayout.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: AppLayout, children: [{path: '/', component: Home}]},
        { path: '/dev-login', component: DevLogin},
        { path: '/queue', component: AppLayout, children: [{path: '/queue', component: Queue}]},
        { path: '/manage', component: AppLayout, children: [{path: '/manage', component: ManageCourse}]},
        { path: '/swipe', component: Swipe},
        { path: '/swipe-auth', component: SwipeAuth}
    ]
})

const app = createApp(App)

app.use(router)

app.mount('#app')

