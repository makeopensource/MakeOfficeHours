<script setup lang="ts">

import {ref} from "vue";

const dev: boolean = import.meta.env.DEV

const root: any = document.querySelector(":root")

if (root != null) {
  root.style.setProperty("--accent-color", dev ? "#A3195A" : "#0461cf")
  root.style.setProperty("--dark-accent-color", dev ? "#7C1344" : "#03499e")
  root.style.setProperty("--bg-color", "#FFFFFF")
  root.style.setProperty("--danger-color", dev ? "#A3195A" : "#0461cf")
}

</script>

<template>

  <RouterView/>

</template>

<style>

@import "assets/css/base.css";

</style>
