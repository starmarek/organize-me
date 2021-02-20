<template>
    <div class="centered">
        <form @submit.prevent="login">
            <div class="columns">
                <div class="column box">
                    <b-field label="Username">
                        <b-input v-model="username"> </b-input>
                    </b-field>

                    <b-field label="Password">
                        <b-input v-model="password"> </b-input>
                    </b-field>
                    <div class="has-text-centered">
                        <b-button expanded type="is-warning">Login</b-button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
        login() {},
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
