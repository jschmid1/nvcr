import axios from 'axios'
import decode from 'jwt-decode';
const ID_TOKEN_KEY = 'id_token';
const ACCESS_TOKEN_KEY = 'access_token';
import Router from 'vue-router';

const API_URL = 'http://localhost:5000/api'
const LOGIN_URL = API_URL + '/login/'
const SIGNUP_URL = API_URL + 'register/'

var router = new Router({
   mode: 'history',
});

export function login(creds) {
       axios.post(`http://localhost:5000/api/login`, creds, {
          headers: {
              'Content-Type': 'application/json',
          }
      })
      .then(function (response) {
            console.log(response.data);
            localStorage.setItem(ACCESS_TOKEN_KEY, response.data.id_token);
            localStorage.setItem(ID_TOKEN_KEY, response.data.auth_token);
            router.go('/');

      })
      .catch(function (error) {
        console.log('token: NOPE');
        console.log(error);
      })
}

export function logout() {
  clearIdToken();
  clearAccessToken();
  router.go('/');
}

export function requireAuth(to, from, next) {
  if (!isLoggedIn()) {
    next({
      path: '/',
      query: { redirect: to.fullPath }
    });
  } else {
    next();
  }
}

export function getIdToken() {
  let tkn = localStorage.getItem(ID_TOKEN_KEY);
  return tkn
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

function clearIdToken() {
  localStorage.removeItem(ID_TOKEN_KEY);
}

function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

// Helper function that will allow us to extract the access_token and id_token
function getParameterByName(name) {
  let match = RegExp('[#&]' + name + '=([^&]*)').exec(window.location.hash);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

// Get and store access_token in local storage
export function setAccessToken() {
  let accessToken = getParameterByName('access_token');
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
}

// Get and store id_token in local storage
export function setIdToken() {
  let idToken = getParameterByName('id_token');
  localStorage.setItem(ID_TOKEN_KEY, idToken);
}

export function isLoggedIn() {
  const idToken = getIdToken();
  console.log("IDTOKEN: "+getIdToken())
  return !!idToken && !isTokenExpired(idToken);
}

function getTokenExpirationDate(encodedToken) {
  const token = decode(encodedToken);
  if (!token.exp) { return null; }

  const date = new Date(0);
  date.setUTCSeconds(token.exp);

  return date;
}

function isTokenExpired(token) {
  const expirationDate = getTokenExpirationDate(token);
  return expirationDate < new Date();
}
