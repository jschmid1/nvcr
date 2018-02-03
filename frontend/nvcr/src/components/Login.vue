<template>
  <div class="col-sm-4 col-sm-offset-4">
    <h2>Log In</h2>
    <p>Log in to your account to get some great quotes.</p>
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

export default {
  name: 'login-component',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      logged_in: false
    }
  },
  methods: {
    submit() {
      console.log(this.credentials)
      let send_data = JSON.stringify({
          password: this.password,
          email: this.email
      })

      axios.post(`http://localhost:5000/api/login`, send_data, {
          headers: {
              'Content-Type': 'application/json',
          }
      }
      ).then(function (response) {
            console.log(response.data);
            localStorage.token = response.data.auth_token
            this.logged_in = true;
      })
      .catch(function (error) {
        console.log('token: NOPE');
        console.log(error);
      })
      // test login
      axios.get('http://localhost:5000/api/secret', {
        headers: {'Authorization': 'Token ' + localStorage.token }
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log('token: ' + this.token);
        console.log(error);
      });
    }
  }

}
</script>
