<template>
  <div class="header">
    <h1> Welcome {{ username }}</h1>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'header-component',
  data () {
    return {
      username: 'Anonymous',
      errors: []
    }
  },
  created () {
    // dynamic user id
    axios.get(`http://localhost:5000/api/user/1`)
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
