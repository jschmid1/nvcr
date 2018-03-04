
<template>
  <div id="app">
    <Login v-if="!isLoggedIn()"></Login>
    <Header v-if="isLoggedIn()"></Header>
    <Table v-if="isLoggedIn()"></Table>
  </div>
</template>
<script>

import Header from './components/Header'
import Table from './components/Table'
import Login from './components/Login'
import { isLoggedIn, login, logout } from './auth';

export default {
  name: 'app',
  data () {
    return {
      test: 'test',
    }
  },
  components: {
    Header,
    Table,
    Login,
  },
  methods: {
    handleLogin() {
      login();
    },
    handleLogout() {
      logout();
    },
    isLoggedIn() {
      return isLoggedIn();
    },
  },
}
</script>

<style lang="scss">
  @import "../node_modules/bootstrap/scss/bootstrap.scss";
</style>
