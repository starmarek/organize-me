import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";

import { NotificationProgrammatic as Notification } from "buefy";
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
        store
            .dispatch("auth/refreshAccessToken")
            .then(() => {
                store.dispatch("auth/startTokenRefreshCounter");
            })
            .catch(() => {
                Notification.open({
                    duration: 8000,
                    message: `Refresh auth error. This should have never happened. Please sign in again. Please report this to administrator.`,
                    position: "is-top-right",
                    type: "is-danger",
                    hasIcon: true,
                });
                store.dispatch("auth/endAuthSession");
                router.push("/login");
            });
    }
}

const vue = new Vue({
    router,
    store,
    render: (h) => h(App),
});

vue.$mount("#app");
