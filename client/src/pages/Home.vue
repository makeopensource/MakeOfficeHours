<script setup lang="ts">

import {useRouter} from "vue-router";

const dev: boolean = import.meta.env.DEV

const router = useRouter()

</script>

<template>
  <div id="login-buttons">

    <button class="login-button" id="autolab-login">Login with Autolab</button>

    <button v-if="dev" class="login-button" id="dev-login" @click="router.push('/dev-login')">Dev Login</button>
  </div>

</template>