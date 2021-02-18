<template>
  <div class="users-creation">
    <h1>Stwórz użytkownika</h1>
    <form @submit.prevent="processForm">
      <div class="columns">
        <div class="column is-one-third">
          <b-field label="Imię">
            <b-input v-model="firstname" />
          </b-field>
        </div>
        <div class="column is-one-third">
          <b-field label="Nazwisko">
            <b-input v-model="surname" />
          </b-field>
        </div>
      </div>

      <div class="columns">
        <div class="column is-two-thirds">
          <b-field label="E-mail">
            <b-input type="email" v-model="email" />
          </b-field>
        </div>
      </div>

      <b-field label="Preferowana zmiana nocna">
        <div class="block">
          <b-checkbox native-value="Dziena" v-model="preferredShift.day">Dzienna</b-checkbox>
          <b-checkbox native-value="Nocna" v-model="preferredShift.night">Nocna</b-checkbox>
        </div>
      </b-field>

      <b-field label="Preferowana wolna niedziela i święta">
        <b-checkbox native-value="true" v-model="freeHolidays">Tak</b-checkbox>
      </b-field>

      <b-field label="Typ etatu">
        <div class="block">
          <b-radio name="name" native-value="1/2" v-model="timeJob">1/2</b-radio>
          <b-radio name="name" native-value="3/5" v-model="timeJob">3/5</b-radio>
          <b-radio name="name" native-value="1" v-model="timeJob">Pełny</b-radio>
        </div>
      </b-field>

      <br />

      <div class="field is-grouped">
        <p class="control">
          <button class="button is-secondary" type="submit">Dodaj</button>
        </p>
        <p class="control">
          <a class="button is-light">Anuluj</a>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "UsersCreation",
  data() {
    return {
      firstname: "",
      surname: "",
      email: "",
      preferredShift: {
        day: false,
        night: false,
      },
      freeHolidays: false,
      timeJob: 1,
    };
  },
  computed: {
    console: () => console,
  },
  methods: {
    processForm: function () {
      console.log({
        firstname: this.firstname,
        email: this.email,
        preferredShift: this.preferredShift,
        freeHolidays: this.freeHolidays,
        timeJob: this.timeJob,
      });
    },
  },
};
</script>
