<template>
    <nav class="navbar navbar-default">
    <div class="navbar-header">
      <router-link to="/" class="navbar-brand"> NVCR for {{ username }} </router-link>
    </div>
    <ul class="nav navbar-nav navbar-right">
      <li>
        <button class="btn btn-danger log" v-show="isLoggedIn()" @click="handleLogout()">Log out </button>
        <button class="btn btn-info log" v-show="!isLoggedIn()" @click="handleLogin()">Log In</button>

        <button type="button" class="btn btn-primary" @click="openModal()">Create Bill</button>
        <modal v-if="showModal" @close="showModal = false">
        </modal>
      </li>
    </ul>
  </nav>
</template>

<script>

import axios from 'axios'
import { isLoggedIn, login, logout } from '../auth';
import Modal from './Modal'

export default {
  name: 'header-component',
  components: {
    Modal,
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
    openModal() {
       this.showModal = true;
    },
  },
  data () {
    return {
      username: 'Anonymous',
      errors: [],
      showModal: false,
      logged_in: isLoggedIn()
    }
  },
  created () {
    // dynamic user id
    axios.get(`http://localhost:5000/api/users/1`)
      .then(response => {
        this.username = response.data.user
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
