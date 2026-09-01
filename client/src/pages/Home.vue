<script setup lang="ts">

import {useRouter} from "vue-router";
import {ref} from "vue";

const dev: boolean = import.meta.env.DEV

const router = useRouter()

const autolabLink = ref<HTMLAnchorElement>();

const myCourses = ref<any>([]);

function findDestination() {
  let destination = ""
  const stored = localStorage.getItem("last-course")

  if (myCourses.value.length === 0) {
    router.push("/nowhere")
  }

  if (stored != null) {
    fetch(`/api/course/${stored}`).then(res => {
      if (res.ok) {
        res.json().then(json => { if (json["course_role"] != null) router.push(`/${stored}/queue`) })
      }
    })
  }

  destination = myCourses.value[0]["course_url"]
  localStorage.setItem("last-course", destination)
  router.push(`/${destination}/queue`)
}

fetch("/api/me").then(res => {
  if (res.ok) {
    res.json().then(json => myCourses.value = json["enrollments"]).then(() => findDestination())
  }
})

</script>

<template>
  <div id="login-buttons">
    <a ref="autolabLink" href="/api/authorize" hidden>Login with Autolab</a>
    <button class="login-button" id="autolab-login" @click="autolabLink?.click()">Login with Autolab</button>

    <button v-if="dev" class="login-button" id="dev-login" @click="router.push('/dev-login')">Dev Login</button>
  </div>

</template>