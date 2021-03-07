import { api } from "@/services/api";

export default {
    fetchTokens(credentials) {
        return api.post("token/", credentials).then((response) => response.data);
    },
    fetchRefreshedAccessToken(refreshToken) {
        return api
            .post("token/refresh/", {
                refresh: refreshToken,
                headers: { Authorization: null },
            })
            .then((response) => response.data);
    },
    logoutUser(refreshToken) {
        return api
            .post("logout/", {
                refresh: refreshToken,
            })
            .then((response) => response.data);
    },
};
