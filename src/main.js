import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";

import Buefy from "buefy";

import api from "@/services/api";

Vue.use(Buefy);

Vue.config.productionTip = false;

const token = localStorage.getItem("accessToken");
if (token) {
    api.defaults.headers.common["Authorization"] = "Bearer " + token;
}

const vue = new Vue({
    router,
    store,
    render: (h) => h(App),
});

vue.$mount("#app");
