import api from "@/services/api";
import { NotificationProgrammatic as Notification } from "buefy";
import jwt_decode from "jwt-decode";

const state = {
    accessToken: localStorage.getItem("accessToken"),
    refreshToken: localStorage.getItem("refreshToken"),
    refreshTokenCounterID: "",
};

const getters = {
    accessToken: (state) => state.accessToken,
    accessTokenDecoded: (state) => jwt_decode(state.accessToken),
    refreshTokenDecoded: (state) => jwt_decode(state.refreshToken),
    refreshToken: (state) => state.refreshToken,
    isAuthenticated: (state) => !!state.accessToken,
    isAccessTokenExpired: (state, getters) => {
        const exp = getters.accessTokenDecoded.exp;
        if (new Date(exp * 1000) < new Date()) {
            return true;
        } else {
            return false;
        }
    },
    refreshTokenCounterID: (state) => state.refreshTokenCounterID,
};

const actions = {
    getTokenPair({ dispatch }, credentials) {
        return new Promise((resolve, reject) => {
            api.post("token/", credentials)
                .then((response) => {
                    dispatch("setTokens", response.data);
                    api.defaults.headers.common["Authorization"] =
                        "Bearer " + response.data.access;
                    dispatch("startTokenRefreshCounter");
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    refreshAccessToken({ commit, getters }) {
        return new Promise((resolve, reject) => {
            delete api.defaults.headers.common["Authorization"];
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
    startTokenRefreshCounter({ dispatch, commit }) {
        const ID = setInterval(() => {
            dispatch("refreshAccessToken");
        }, 10000);
        commit("setTokenRefreshCounterID", ID);
    },
    endAuthSession({ commit, getters }, notification = false) {
        commit("removeTokens");
        delete api.defaults.headers.common["Authorization"];
        const ID = getters.refreshTokenCounterID;
        if (ID != "") {
            clearInterval(ID);
        }
        if (notification) {
            Notification.open({
                duration: 8000,
                message: `Your session has expired, please sign in again.`,
                position: "is-top-right",
                type: "is-warning",
                hasIcon: true,
            });
        }
    },
};

const mutations = {
    setTokenRefreshCounterID(state, ID) {
        state.refreshTokenCounterID = ID;
    },
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
