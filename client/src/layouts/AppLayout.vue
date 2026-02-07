<script setup lang="ts">

import githubLogo from "@/assets/github.svg";
import Header from "@/components/Header.vue";

</script>

<template>
  <div id="site-body">
    <Header/>

    <div id="site-content">
      <RouterView/>
    </div>

    <footer>
      <div id="site-footer">
        <a id="github-link" href="https://github.com/makeopensource/MakeOfficeHours">
          <img :src="githubLogo" alt="github-logo" height="32">
          GitHub
        </a>
      </div>
    </footer>
  </div>
</template>

<style scoped>


#github-link {
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