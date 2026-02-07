<script setup lang="ts">

import {ref} from "vue";
import {useRouter} from "vue-router";


const router = useRouter()

let code = ref<string>("");

let status = ref<string>("");

let setCode = () => {
  localStorage.setItem("auth-code", code.value)
  status.value = "Done!"
  router.push("/swipe")
}

</script>

<template>

  <div id="auth-cont">
      <label for="auth-code">Swipe Authorization Code</label>
      <br/>
      <input v-model="code" id="auth-code">
      <br/>
      <button @click="setCode" class="no-grow">Set Authorization Code</button>
      <br/>
      <p>{{ status }}</p>
  </div>


</template>

<style scoped>


#auth-cont {
  display: flex;
  justify-content: center;
  flex-direction: column;
  margin: 128px;
}

br {
  margin-top: 8px;
}

p {
  text-align: center;
}

</style>