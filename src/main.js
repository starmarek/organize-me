import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";

import Buefy from "buefy";

Vue.use(Buefy);

Vue.config.productionTip = false;

// handle auth when user open / refresh the app
if (store.getters["auth/isAuthenticated"]) {
    store.dispatch("auth/setAxiosHeaders");
    if (store.getters["auth/isAccessTokenExpired"]) {
        store.dispatch("auth/endAuthSession", true);
        router.push("/login");
    } else {
        store.dispatch("auth/refreshAccessToken");
        store.dispatch("auth/startTokenRefreshCounter");
    }
}

const vue = new Vue({
    router,
    store,
    render: (h) => h(App),
});

vue.$mount("#app");
