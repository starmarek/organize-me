<template>

  <div id="app">
    <div id="header">
      <h1>Organize-me <i class="fa fa-hospital-o" aria-hidden="true"/></h1>
      <h4>Szybkie i wygodnie ustalanie grafiku!</h4>
    </div>

    <div id="section">
        <div id="nav">
          <ul>
            <li><router-link :to="{ name: 'home' }">Home</router-link></li>
            <li><router-link :to="{ name: 'messages' }">Django Rest</router-link></li>
          </ul>
        </div>

      <div id="main">
        <router-view/>
      </div>
    </div>

    <div id="footer">
      <p>Footer</p>
    </div>

  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
@import "styles/main.css";
</style>
