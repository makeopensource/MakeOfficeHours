<script setup lang="ts">

import {useRouter} from "vue-router";
import nowhere from "@/assets/nowhere.png";

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
    <img :src="nowhere" alt="Horse behind a tree" class="big-logo">
    <br/>
    <p>There are no courses associated with your account.</p>
    <p>You need to be in a course to use this site.</p>
    <br/>
    <button class="no-grow" @click="signOut">Sign Out</button>
  </div>
</template>

<style scoped>

  #content {
    color: black;
    margin: 16px auto auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    gap: 8px;
    padding: 16px 64px;
    max-width: fit-content;
  }

  .big-logo {
    margin: auto;
    max-height: 65vh;
  }

  button {
    margin: auto;
  }

</style>