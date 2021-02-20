import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import Messages from "@/components/Messages";
import UsersDashboard from "@/components/user/UsersDashboard.vue";
import Login from "@/components/layout/Login.vue";
import UsersCreation from "@/components/user/UsersCreation.vue";

Vue.use(Router);

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
        },
        {
            path: "/messages",
            name: "messages",
            component: Messages,
        },
        {
            path: "/users",
            name: "users-dashboard",
            component: UsersDashboard,
        },
        {
            path: "/users/creation",
            name: "users-creation",
            component: UsersCreation,
        },
    ],
});
