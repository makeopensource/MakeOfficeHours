<script setup lang="ts">

import {useRouter} from "vue-router";
import {ref} from "vue";

const dev: boolean = import.meta.env.DEV

const router = useRouter()

const autolabLink = ref<HTMLAnchorElement>();

</script>

<template>
  <div id="login-buttons">
    <a ref="autolabLink" href="/api/authorize" hidden>Login with Autolab</a>
    <button class="login-button" id="autolab-login" @click="autolabLink?.click()">Login with Autolab</button>

    <button v-if="dev" class="login-button" id="dev-login" @click="router.push('/dev-login')">Dev Login</button>
  </div>

</template>