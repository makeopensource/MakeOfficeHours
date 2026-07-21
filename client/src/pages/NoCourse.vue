<script setup lang="ts">

import {useRouter} from "vue-router";

const router = useRouter()

function signOut() {
  fetch("/api/signout", { method: "POST" }).then(res => {
    if (res.ok) {
      router.push("/")
    }
  })
}

</script>

<template>
  <div id="content">
    <img src="../assets/makeopenhorse.png" alt="Make Open Horse logo" class="big-logo">
    <p>Well, there is a horse here.</p>
    <p>There are no courses associated with your account.</p>
    <button class="no-grow" @click="signOut">Sign Out</button>
  </div>
</template>

<style scoped>

  #content {
    margin: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    gap: 8px;
  }

  .big-logo {
    margin: auto;
    max-height: 65vh;
  }

  button {
    margin: auto;
  }

</style>