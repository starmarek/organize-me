import Vue from "vue";
import App from "@/App.vue";

import store from "@/store";
import router from "@/router";

import Buefy from "buefy";

import "@fortawesome/fontawesome-free/js/all.js";

Vue.use(Buefy, {
    defaultIconPack: "fas",
});

Vue.config.productionTip = false;

// Vue.use(VueRouter)

const vue = new Vue({
    router,
    store,
    render: (h) => h(App),
});

vue.$mount("#app");
