<template>
    <div class="hello">
        <h1>Strona startowa</h1>
        <button>Zaloguj</button>
        <p>
            Nie masz konta?
            <!-- It does nothing YET! -->
            <a class="register" href="register"> Zarejstruj się! </a>
        </p>
    </div>
</template>

<script>
export default {
    name: "Home",
    props: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
