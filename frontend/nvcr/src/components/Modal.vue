

<template>
<transition name="modal">
  <div class="modal is-active">
    <div class="modal-background"></div>
    <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Modal title</p>
    </header>

      <div class="modal-content">
        <form>

          <p v-if="errors.length">
            <b>Please correct the following error(s):</b>
            <ul>
              <li v-for="error in errors">{{ error }}</li>
            </ul>
          </p>

        <label class='label' for="price">Price</label>
        <input class='input' type="number" v-model="selected_values.price" placeholder="$$">
        <br>

        <div class="select">
            <label class='label' for="market">Market</label>
            <select v-model="selected_values.selected_market">
                <option value="" disabled selected>Select market</option>
                <option v-for="market in markets" v-bind:value="market.name">
                    {{ market.name }}
                </option>
            </select>

            </select>

        </div>

        <br>
        <br>
        <br>

        <ul class="members">
            <li v-for="member in users">
                <input type="checkbox" :value="member" :id="member.name" v-model="selected_values.selected_members">
                <label :for="member.name"> {{ member.name }} <img :src="member.avatar"> </label>
            </li>
        </ul>

        <label class='label' for="date">Date</label>
        <input v-model='selected_values.date' type="date" name="date">
        <br>

        <div class="field">
            <label class="label">Description</label>
            <div class="control">
                <textarea
                   v-model='selected_values.description'
                   v-validate="selected_values.description"
                   data-rules="'required|min:3'"
                   class="textarea"
                   placeholder="Dinner, Lunch..">
                 </textarea>
                 <p class="help is-danger" v-show="errors.has('description')">
                  {{ errors.first('description') }}
                </p>
            </div>
        </div>
        </form>
      </div>

        <footer class="modal-card-foot">
          <button
             :disabled="errors.any()"
             type="submit"
             class="btn btn-primary"
             data-dismiss="modal"
             @click="submitAndClose()">
            Submit
          </button>
          <button type="button" class="btn btn-outline-info" @click="close()"> Close </button>
          </button>
       </footer>
      </div>
    </div>
  </div>
</transition>
</template>

<script>


import axios from 'axios'
import { getAccessToken, isLoggedIn } from '../auth';


export default {
    name: 'modal',
    data () {
      return {
        form: {
          description: ''
        },
        selected_values: {
          selected_members: [],
          selected_market: "",
          description: "",
          price: '',
          date: "",
          owner_id: "",
        },
        markets: [],
        name: '',
        users: [],
      }
    },
    methods: {
      close() {
        this.$emit('close');
      },
      submitAndClose() {
         this.new_bill(this.selected_values)
      },
      openModal() {
         this.showModal = true;
      },
      closeModal() {
         this.showModal = false;
      },
      populate_market() {
        axios.get(`http://localhost:5000/api/markets`)
          .then(response => {
            this.markets = response.data.markets
          })
          .catch(e => {
            this.errors.push(e)
          })
      },
      populate_users() {
        axios.get(`http://localhost:5000/api/users`)
          .then(response => {
            this.users = response.data.users
          })
          .catch(e => {
            this.errors.push(e)
          })
      },
      populate_self() {
        this.selected_values.owner_id = getAccessToken()
      },
      new_bill(payload) {

         axios.post(`http://localhost:5000/api/bills/new`, payload, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(function (response) {
              console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        })
  },
    },
    created () {
      this.populate_market();
      this.populate_users();
      this.populate_self();
    }
  };
</script>



<style lang="scss">
  @import "../../node_modules/bulma/bulma.sass";

.wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.myclass {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.level {
  padding: 0 20%;
  margin: 15px 0 0 !important;
}

.columns {
  margin: 0;
}

.column {
  padding: 0 20%;
}

.section {
  padding: 3rem 0;
}

table {
  border: 2px solid #42b983;
  border-radius: 3px;
  background-color: #fff;
}

th {
  background-color: #42b983;
  color: rgba(255,255,255,0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

td {
  background-color: #f9f9f9;
}

th, td {
  min-width: 120px;
  padding: 10px 20px;
}

th.active {
  color: #fff;
}

th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}

.members {
    margin: 0 -5px 30px;
}

.members li {
    display: inline-block;
    width: 25%;
    padding: 0 5px;
}

.members li label img {
    width: 100%;
}

input[type=checkbox] {
    display:none;
}
input[type=checkbox] + label {
    background-repeat: no-repeat;
    display: block;
    width: 100%;
    filter: grayscale(100%);
    padding: 0;
    transition: transform 0.25s ease, -webkit-filter 0.5s ease, color 0.5s ease;
}
input[type=checkbox]:checked + label {
    filter: grayscale(0%);
    transform: translateY(20px);
    display: inline-block;
    padding: 0;
    color: red;
}
.user-modal-container * {
  box-sizing: border-box;
}

.user-modal-container {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  visibility: hidden;
  cursor: pointer;
  overflow-y: auto;
  z-index: 3;
  font-family: 'Lato', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif';
  font-size: 14px;
  background-color: rgba(17, 17, 17, .9);
  -webkit-transition: all 0.25s linear;
  -moz-transition: all 0.25s linear;
  -o-transition: all 0.25s linear;
  -ms-transition: all 0.25s linear;
  transition: all 0.25s linear;
}

.user-modal-container.active {
  opacity: 1;
  visibility: visible;
}

.user-modal-container .user-modal {
  position: relative;
  margin: 50px auto;
  width: 90%;
  max-width: 500px;
  background-color: #f6f6f6;
  cursor: initial;
}

.user-modal-container .form-login,
.user-modal-container .form-register,
.user-modal-container .form-password {
  padding: 75px 25px 25px;
  display: none;
}

.user-modal-container .form-login.active,
.user-modal-container .form-register.active,
.user-modal-container .form-password.active {
  display: block;
}

.user-modal-container ul.form-switcher {
  margin: 0;
  padding: 0;
}

.user-modal-container ul.form-switcher li {
  list-style: none;
  display: inline-block;
  width: 50%;
  float: left;
  margin: 0;
}

.user-modal-container ul.form-switcher li a {
  width: 100%;
  display: block;
  height: 50px;
  line-height: 50px;
  color: #666666;
  background-color: #dddddd;
  text-align: center;
}

.user-modal-container ul.form-switcher li a.active {
  color: #000000;
  background-color: #f6f6f6;
}

.user-modal-container input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #eeeeee;
}

.user-modal-container input[type="submit"] {
  color: #f6f6f6;
  border: 0;
  margin-bottom: 0;
  background-color: #3fb67b;
  cursor: pointer;
}

.user-modal-container input[type="submit"]:hover {
  background-color: #3aa771;
}

.user-modal-container input[type="submit"]:active {
  background-color: #379d6b;
}

.user-modal-container .links {
  text-align: center;
  padding-top: 25px;
}

.user-modal-container .links a {
  color: #3fb67b;
}

.user-modal-container input[type="submit"].disabled {
  background-color: #98d6b7;
}

</style>
