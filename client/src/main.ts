
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
import NotFound from "@/pages/NotFound.vue";
import AdminPage from "@/pages/AdminPage.vue";
import NoCourse from "@/pages/NoCourse.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: AppLayout, children: [{path: '/', component: Home}]},
        { path: '/dev-login', component: DevLogin},
        { path: '/:course/queue', component: AppLayout, children: [{path: '/:course/queue', component: Queue}]},
        { path: '/:course/manage', component: AppLayout, children: [{path: '/:course/manage', component: ManageCourse}]},
        { path: '/admin', component: AppLayout, children: [{path: '/admin', component: AdminPage}]},
        { path: '/:course/swipe', component: Swipe},
        { path: '/:course/swipe-auth', component: SwipeAuth},
        { path: '/nowhere', component: AppLayout, children: [{path: '/nowhere', component: NoCourse}]},
        { path: '/:pathMatch(.*)*', component: AppLayout, children: [{path: '/:pathMatch(.*)*', component: NotFound}]}
    ]
})

const app = createApp(App)

app.use(router)

app.mount('#app')

