<script setup lang="ts">

import githubLogo from "@/assets/github.svg";
import mohJoke from "@/assets/makeopenhorse.png";
import Header from "@/components/common/Header.vue";
import {ref} from "vue";

const admin = ref<boolean>(false);

fetch("/api/me").then(res => {
  if (res.ok) {
    return res.json()
  }
}).then(json => {
  admin.value = json["site_role"] === "admin"
})

</script>

<template>
  <div id="site-body">
    <Header/>

    <div id="site-content">
      <RouterView/>
    </div>

    <footer>
      <div id="site-footer">
        <a class="picture-link" href="https://github.com/makeopensource/MakeOfficeHours">
          <img :src="githubLogo" alt="github-logo" height="32">
          GitHub
        </a>
        <a class="picture-link" v-if="admin" href="/admin">
          <img :src="mohJoke" alt="MakeOpenHorse Logo" height="32">
          Admin Page
        </a>
      </div>
    </footer>
  </div>
</template>

<style scoped>


.picture-link {
  display: flex;
  align-items: center;
  gap: 8px;
}

a {
  text-decoration: none;
  color: black;
  font-size: 1.0rem;
}

#site-body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#site-content {
  flex: 1;
}


footer {
  margin: 16px 8%;
}

#site-footer {
  padding: 16px;
  display: flex;
  gap: 32px;
  align-items: center;
  border-top: 1px solid #d9d9d9;
  border-bottom: 1px solid #d9d9d9;
}

hr {
  border: 1px solid #d9d9d9
}

</style>