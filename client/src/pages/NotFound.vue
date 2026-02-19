<script setup lang="ts">

import {useRouter} from "vue-router";

const router = useRouter()

</script>

<template>
  <div id="content">
    <img src="../assets/makeopenhorse.png" alt="Make Open Horse logo" class="big-logo">
    <p>Couldn't find what you were looking for. (Unless it was this horse)</p>
    <button class="no-grow" @click="router.push('/')">Go Home</button>
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