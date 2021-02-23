import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import UsersDashboard from "@/components/user/UsersDashboard.vue";
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
