import axios from "axios";
import Cookies from "js-cookie";

const api = axios.create({
    baseURL: "/api",
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
    },
});

export { api };
