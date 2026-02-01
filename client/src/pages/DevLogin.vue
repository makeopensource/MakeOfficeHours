<script setup lang="ts">

import {ref} from "vue";
import {useRouter} from "vue-router";

const message = ref("");

const router = useRouter()

function submitWithoutRedirect(form: HTMLFormElement | undefined) {
  if (form === undefined) {
    return
  }

  const data = new FormData(form)
  fetch(form.action, {
    method: form.method,
    body: data
  }).then((res) => {
    return res.json()
  }).then(data => {
    message.value = data["message"]
  })
}

const enrollForm = ref<HTMLFormElement>();
const registerForm = ref<HTMLFormElement>();
const loginForm = ref<HTMLFormElement>();

const submitEnroll = () => {
  submitWithoutRedirect(enrollForm.value)
}

const submitRegister = () => {
  submitWithoutRedirect(registerForm.value)
}

const submitLogin = () => {
  submitWithoutRedirect(loginForm.value)
}

</script>

<template>
  <div id="forms">
    <div class="dev-form" id="enroll">
      <h2>Force Enroll</h2>
      <form @submit.prevent="submitEnroll" ref="enrollForm" action="/api/force-enroll" method="post"
            enctype="application/x-www-form-urlencoded">
        <label for="ubit">UBITName</label>
        <input name="ubit" type="text" id="ubit">
        <br/>
        <label for="pn">Person Number</label>
        <input name="pn" type="text" id="pn">
        <br/>
        <label for="role">Role</label>
        <select name="role" id="role">
          <option value="student">Student</option>
          <option value="ta">TA</option>
          <option value="instructor">Instructor</option>
          <option value="admin">Admin</option>
        </select>
        <br/>
        <button type="submit">Enroll</button>
      </form>
    </div>
    <div class="dev-form" id="register">
      <h2>Register</h2>

      <form action="/api/signup" method="post" ref="registerForm" @submit.prevent="submitRegister"
            enctype="application/x-www-form-urlencoded">
        <label for="ubit">UBITName</label>
        <input name="ubit" type="text" id="ubit">
        <br/>
        <label for="password">Password</label>
        <input name="password" type="password" id="password">
        <br/>
        <button type="submit">Register</button>
      </form>
    </div>
    <div class="dev-form" id="login">
      <h2>Login</h2>
      <form action="/api/login" method="post" ref="loginForm" @submit.prevent="submitLogin"
            enctype="application/x-www-form-urlencoded">
        <label for="ubit">UBITName</label>
        <input name="ubit" type="text" id="ubit">
        <br/>
        <label for="password">Password</label>
        <input name="password" type="password" id="password">
        <br/>
        <button type="submit">Login</button>
      </form>
    </div>
    <p id="message">{{ message }}</p>
    <button @click="router.push('/queue')">Go to Queue</button>
  </div>
</template>

<style scoped>
@import "../assets/css/dev-login.css";
</style>