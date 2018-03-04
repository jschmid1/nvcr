<template>
  <div id="bills">
    <v-client-table :data="bills" :columns="columns" :options="options">

    </v-client-table>
  </div>
</template>
<script>

import axios from 'axios'

export default {
  name: 'table-component',
  data () {
    return {
      columns: ['id', 'owner', 'amount', 'market', 'participants'],
      errors: [],
      bills: [],
      options: {
        headings: {
          owner: 'Username',
          amount: 'Amount',
          market: 'Market',
          participants: 'Participants'
        },
        sortable: ['owner', 'amount'],
        filterable: ['owner', 'market']
     }
    }
  },
  created () {
    // dynamic user id
    axios.get(`http://localhost:5000/api/bills`)
      .then(response => {
        this.bills = response.data.bills
      })
      .catch(e => {
        this.errors.push(e)
      })
  }
}
</script>

<style scoped>

.VuePagination {
  text-align: center;
}

.vue-title {
  text-align: center;
  margin-bottom: 10px;
}

.vue-pagination-ad {
  text-align: center;
}


th:nth-child(3) {
  text-align:center;
}

#bills {
  text-align: center;
  width: 95%;
  margin: 0 auto;
}

</style>
