import api from "@/services/api";
import jwt_decode from "jwt-decode";

const state = {
    accessToken: localStorage.getItem("accessToken"),
    refreshToken: localStorage.getItem("refreshToken"),
};

const getters = {
    accessToken: (state) => state.accessToken,
    accessTokenDecoded: (state) => jwt_decode(state.accessToken),
    refreshTokenDecoded: (state) => jwt_decode(state.refreshToken),
    refreshToken: (state) => state.accessToken,
    isAuthenticated: (state) => !!state.accessToken,
};

const actions = {
    getTokenPair({ dispatch }, credentials) {
        return new Promise((resolve, reject) => {
            api.post("token/", credentials)
                .then((response) => {
                    dispatch("setTokens", response.data);
                    api.defaults.headers.common["Authorization"] =
                        "Bearer " + response.data.access;
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    refreshAccessToken({ commit, getters }) {
        return new Promise((resolve, reject) => {
            api.post("token/refresh/", { refresh: getters.refreshToken })
                .then((response) => {
                    commit("setAccessToken", response.data.access);
                    api.defaults.headers.common["Authorization"] =
                        "Bearer " + response.data.access;
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    setTokens({ commit }, data) {
        commit("setAccessToken", data.access);
        commit("setRefreshToken", data.refresh);
    },
};

const mutations = {
    setRefreshToken(state, token) {
        state.refreshToken = token;
        localStorage.setItem("refreshToken", token);
    },
    setAccessToken(state, token) {
        state.accessToken = token;
        localStorage.setItem("accessToken", token);
    },
    removeTokens(state) {
        state.accessToken = "";
        state.refreshToken = "";
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
