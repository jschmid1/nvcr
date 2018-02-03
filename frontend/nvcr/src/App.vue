
<template>
  <div id="app">
    <Login></Login>
    <Header></Header>
    <Table></Table>
  </div>
</template>

<script>

import Header from './components/Header'
import Table from './components/Table'
import Login from './components/Login'

export default {
  name: 'app',
  components: {
    Header,
    Table,
    Login
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
