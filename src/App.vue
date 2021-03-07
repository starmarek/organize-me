<template>
    <div class="app content">
        <Navbar />
        <router-view />
    </div>
</template>

<script>
import Navbar from "@/components/layout/Navbar.vue";
export default {
    name: "App",
    components: {
        Navbar,
    },
};
</script>

<style lang="scss">
// CUSTOM
body {
    height: 100vh;
}

// BULMA
@import "~bulma/sass/utilities/_all";

$primary: #227c9d;
$primary-invert: findColorInvert($primary);
$secondary: #ffcb77;
$secondary-invert: findColorInvert($secondary);

$colors: (
    "white": (
        $white,
        $black,
    ),
    "black": (
        $black,
        $white,
    ),
    "light": (
        $light,
        $light-invert,
    ),
    "dark": (
        $dark,
        $dark-invert,
    ),
    "primary": (
        $primary,
        $primary-invert,
    ),
    "secondary": (
        $secondary,
        $secondary-invert,
    ),
    "info": (
        $info,
        $info-invert,
    ),
    "success": (
        $success,
        $success-invert,
    ),
    "warning": (
        $warning,
        $warning-invert,
    ),
    "danger": (
        $danger,
        $danger-invert,
    ),
);

$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
