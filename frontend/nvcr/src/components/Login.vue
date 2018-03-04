<template>
  <div class="col-sm-4 col-sm-offset-4">
    <h2>Log In</h2>
    <div class="alert alert-danger" v-if="error">
      <p>{{ error }}</p>
    </div>
    <div class="form-group">
      <input
        type="text"
        class="form-control"
        placeholder="Enter your email"
        v-model="email"
      >
    </div>
    <div class="form-group">
      <input
        type="password"
        class="form-control"
        placeholder="Enter your password"
        v-model="password"
      >
    </div>
    <button class="btn btn-primary" @click="submit()">Access</button>
  </div>
</template>

<script>

import axios from 'axios'
import { isLoggedIn, login, logout } from '../auth';

export default {
  name: 'login-component',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      logged_in: isLoggedIn()
    }
  },
  methods: {
    submit() {
      console.log(this.credentials)
      let send_data = JSON.stringify({
          password: this.password,
          email: this.email
      })
      login(send_data)
    },
    handleLogin() {
      login();
    },
    handleLogout() {
      logout();
    },
    isLoggedIn() {
      return isLoggedIn();
    },
  }

}
</script>
