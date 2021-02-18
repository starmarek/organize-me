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
                    <a class="button is-secondary">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">Log in</a>
                </div>
            </b-navbar-item>
        </template>
        <router-link :to="{ name: 'home' }">Home</router-link>
    </b-navbar>
</template>

<script>
export default {
    name: "Navbar",
};
</script>
