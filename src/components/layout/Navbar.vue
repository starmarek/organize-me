<template>
    <b-navbar class="is-primary">
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                ORGANIZE-ME
                <i class="fa fa-hospital-o" aria-hidden="true" />
            </b-navbar-item>
        </template>
        <template slot="start">
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
                    <b-button @click="logout" v-else type="is-light">Logout</b-button>
                </div>
            </b-navbar-item>
        </template>
        <router-link :to="{ name: 'home' }">Home</router-link>
    </b-navbar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
    name: "Navbar",
    computed: {
        ...mapGetters("auth", ["isAuthenticated"]),
    },
    methods: {
        ...mapActions("auth", ["endAuthSession"]),
        logout() {
            this.endAuthSession();
            if (this.$route.path != "/") {
                this.$router.push("/");
            }
        },
    },
};
</script>
<style>
.navbar {
    height: 5vh;
}
</style>
