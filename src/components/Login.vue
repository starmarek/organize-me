<template>
    <div class="centered">
        <form @submit.prevent="login">
            <div class="columns">
                <div class="column box" style="margin-bottom: 5vh">
                    <b-field
                        :type="wrongCredentialsProvided ? 'is-danger' : ''"
                        :message="
                            wrongCredentialsProvided
                                ? 'The email or password is incorrect.'
                                : ''
                        "
                        label="Username"
                    >
                        <b-input v-model="username" required></b-input>
                    </b-field>
                    <b-field label="Password">
                        <b-input required password-reveal v-model="password"></b-input>
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
import { mapActions } from "vuex";
export default {
    name: "Login",
    data() {
        return {
            wrongCredentialsProvided: false,
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
            })
                .then(() => {
                    this.$router.push("/");
                    this.$buefy.notification.open({
                        duration: 8000,
                        message: `Successfull login!`,
                        position: "is-top-right",
                        type: "is-success",
                        hasIcon: true,
                    });
                })
                .catch((err) => {
                    if (err.response.status == 401) {
                        this.password = "";
                        this.wrongCredentialsProvided = true;
                    } else {
                        this.$buefy.notification.open({
                            duration: 8000,
                            message: `Request failed with status <b>${err.response.status}</b>. Please try again in a moment. Otherwise contact administrator.`,
                            position: "is-top-right",
                            type: "is-danger",
                            hasIcon: true,
                        });
                    }
                });
        },
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
