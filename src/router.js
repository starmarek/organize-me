import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import Messages from "@/components/Messages";
import UsersDashboard from "@/components/user/UsersDashboard.vue";
import Login from "@/components/layout/Login.vue";
import UsersCreation from "@/components/user/UsersCreation.vue";

import store from "@/store";

Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
    if (!store.getters["auth/isAuthenticated"]) {
        next();
        return;
    }
    next("/");
};

const ifAuthenticated = (to, from, next) => {
    if (store.getters["auth/isAuthenticated"]) {
        next();
        return;
    }
    next("/login");
};

export default new Router({
    routes: [
        {
            path: "/",
            name: "home",
            component: Home,
        },
        {
            path: "/login",
            name: "login",
            component: Login,
            beforeEnter: ifNotAuthenticated,
        },
        {
            path: "/messages",
            name: "messages",
            component: Messages,
            beforeEnter: ifAuthenticated,
        },
        {
            path: "/users",
            name: "users-dashboard",
            component: UsersDashboard,
            beforeEnter: ifAuthenticated,
        },
        {
            path: "/users/creation",
            name: "users-creation",
            component: UsersCreation,
            beforeEnter: ifAuthenticated,
        },
    ],
});
