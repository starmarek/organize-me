<template>
    <div class="centered">
        <form @submit.prevent="login">
            <div class="columns">
                <div class="column box" style="margin-bottom: 5vh">
                    <b-field label="Username">
                        <b-input v-model="username"></b-input>
                    </b-field>
                    <b-field label="Password">
                        <b-input password-reveal v-model="password"></b-input>
                    </b-field>
                    <div class="has-text-centered">
                        <b-button expanded native-type="submit" type="is-warning">
                            Login
                        </b-button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
        ...mapActions("auth", ["getTokenPair"]),
        login() {
            this.getTokenPair({
                username: this.username,
                password: this.password,
            });
        },
    },
    computed: {
        ...mapGetters("auth", [
            "accessToken",
            "refreshToken",
            "accessTokenDecoded",
            "refreshTokenDecoded",
        ]),
    },
};
</script>

<style>
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 95vh;
    background-color: rgb(238, 235, 235);
}
</style>
