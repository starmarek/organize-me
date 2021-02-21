import Vue from "vue";
import Vuex from "vuex";
import messages from "./modules/messages";
import auth from "./modules/auth";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        messages,
        auth,
    },
});
