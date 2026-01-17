<script setup lang="ts">

import {ref} from "vue";

const error = ref<string>("");
const boxOpacity = ref<number>(1);

let opacityTimer: NodeJS.Timeout | null = null;
let endTimer: NodeJS.Timeout | null = null;

const fading = ref<string>("");
const msgType = ref<string>("");

const setError = (newError: string) => {
  error.value = newError;
  msgType.value = "error"
  fading.value = "";
  boxOpacity.value = 1;
  if (opacityTimer) {
    clearTimeout(opacityTimer);
  }
  if (endTimer) {
    clearTimeout(endTimer)
  }
  opacityTimer = setTimeout(() => { fading.value = "fading"; boxOpacity.value = 0 }, 2000);
  endTimer = setTimeout(() => { error.value = ""; boxOpacity.value = 1; fading.value = "" }, 5000)
}

const setMessage = (message: string) => {
  error.value = message;
  msgType.value = ""
  fading.value = "";
  boxOpacity.value = 1;
  if (opacityTimer) {
    clearTimeout(opacityTimer);
  }
  if (endTimer) {
    clearTimeout(endTimer)
  }
  opacityTimer = setTimeout(() => { fading.value = "fading"; boxOpacity.value = 0 }, 2000);
  endTimer = setTimeout(() => { error.value = ""; boxOpacity.value = 1; fading.value = "" }, 5000)

}

defineExpose({"setError": setError, "setMessage": setMessage})

</script>

<template>

  <div id="alert-container">
    <div id="alert" :class='[fading, msgType]' :style="{ opacity: boxOpacity }" ref="alertBox" v-show="error">{{ error }}</div>
  </div>

</template>

<style scoped>

#alert-container {
  position: absolute;
  top: 90%;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 4px;
}

#alert.error {
  background-color: var(--danger-color);
}

#alert {
  display: flex;
  flex-grow: 0;
  background-color: var(--accent-color);
  min-width: 20rem;
  min-height: 2rem;
  padding: 0.4rem 1rem;
  border-radius: 10px;
  justify-content: center;
  text-align: center;
  color: white;
  align-items: center;
  opacity: 1;
}

.fading {
    transition: opacity 5s;
}


</style>