import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import Messages from "@/components/Messages";
import UsersDashboard from "@/components/user/UsersDashboard.vue";
import Login from "@/components/Login.vue";
import UsersCreation from "@/components/user/UsersCreation.vue";

import store from "@/store";

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: "/",
            name: "home",
            component: Home,
            meta: { requiresAuth: false, requiresNoAuth: false },
        },
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: { requiresAuth: false, requiresNoAuth: true },
        },
        {
            path: "/messages",
            name: "messages",
            component: Messages,
            meta: { requiresAuth: true, requiresNoAuth: false },
        },
        {
            path: "/users",
            name: "users-dashboard",
            component: UsersDashboard,
            meta: { requiresAuth: true, requiresNoAuth: false },
        },
        {
            path: "/users/creation",
            name: "users-creation",
            component: UsersCreation,
            meta: { requiresAuth: true, requiresNoAuth: false },
        },
    ],
    scrollBehavior() {
        return { x: 0, y: 0 };
    },
});
export default router;

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.getters["auth/isAuthenticated"]) {
            next();
        } else {
            next("/login");
        }
    } else if (to.matched.some((record) => record.meta.requiresNoAuth)) {
        if (!store.getters["auth/isAuthenticated"]) {
            next();
        } else {
            next("/");
        }
    } else {
        next();
    }
});
