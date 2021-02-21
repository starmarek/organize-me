<template>
    <b-navbar class="is-primary">
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                ORGANIZE-ME
                <i class="fa fa-hospital-o" aria-hidden="true" />
            </b-navbar-item>
        </template>
        <template slot="start">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">Home</b-navbar-item>
            <b-navbar-item tag="router-link" :to="{ path: '/messages' }"
                >Messages</b-navbar-item
            >
            <b-navbar-item tag="router-link" :to="{ path: '/users' }"
                >Users</b-navbar-item
            >
        </template>

        <template slot="end">
            <b-navbar-item tag="div">
                <div class="buttons">
                    <b-button
                        v-if="!isAuthenticated"
                        tag="router-link"
                        to="/login"
                        type="is-light"
                        >Sign in</b-button
                    >
                    <b-button @click="logout" v-if="isAuthenticated" type="is-light"
                        >Logout</b-button
                    >
                </div>
            </b-navbar-item>
        </template>
        <router-link :to="{ name: 'home' }">Home</router-link>
    </b-navbar>
</template>

<script>
import { mapMutations, mapGetters } from "vuex";

export default {
    name: "Navbar",
    computed: {
        ...mapGetters("auth", ["isAuthenticated"]),
    },
    methods: {
        ...mapMutations("auth", ["removeTokens"]),
        logout() {
            this.removeTokens();
            this.$router.push("/");
        },
    },
};
</script>
<style>
.navbar {
    height: 5vh;
}
</style>
