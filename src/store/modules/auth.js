import { api } from "@/services/api";
import { NotificationProgrammatic as Notification } from "buefy";
import authService from "../../services/authService";
import jwt_decode from "jwt-decode";
import router from "@/router";

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
    authUser: (state, getters) => getters.accessTokenDecoded.user,
};

const actions = {
    getTokenPair({ dispatch }, credentials) {
        return new Promise((resolve, reject) => {
            authService
                .fetchTokens(credentials)
                .then((data) => {
                    dispatch("setTokens", data);
                    dispatch("setAxiosHeaders");
                    dispatch("startTokenRefreshCounter");
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    refreshAccessToken({ commit, getters, dispatch }) {
        return new Promise((resolve, reject) => {
            authService
                .fetchRefreshedAccessToken(getters.refreshToken)
                .then((data) => {
                    commit("setAccessToken", data.access);
                    dispatch("setAxiosHeaders");
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    setAxiosHeaders({ getters }) {
        api.defaults.headers.common["Authorization"] = "Bearer " + getters.accessToken;
    },
    removeAxiosHeaders() {
        delete api.defaults.headers.common["Authorization"];
    },
    setTokens({ commit }, data) {
        commit("setAccessToken", data.access);
        commit("setRefreshToken", data.refresh);
    },
    startTokenRefreshCounter({ dispatch, commit }) {
        const ID = setInterval(() => {
            dispatch("refreshAccessToken").catch(() => {
                dispatch("endAuthSession");
                router.push("/login");
                Notification.open({
                    duration: 8000,
                    message: `Refresh auth error. This should have never happened. Please sign in again. Please report this to administrator.`,
                    position: "is-top-right",
                    type: "is-danger",
                    hasIcon: true,
                });
            });
        }, 10000);
        commit("setTokenRefreshCounterID", ID);
    },
    endAuthSession({ commit, getters, dispatch }, notification = false) {
        commit("removeTokens");
        dispatch("removeAxiosHeaders");

        const ID = getters.refreshTokenCounterID;
        // when user refresh the page, and the token is expired
        // refreshTokenCounter won't be active, i.e. ID == ""
        // but when user explicitly log out, refreshTokenCounter will be active
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
