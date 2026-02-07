<script setup lang="ts">

import {ref} from "vue";
import {useRouter} from "vue-router";
import Header from "@/components/Header.vue";

let inputRef = ref<HTMLInputElement>();

let status = ref<string>("");

let queueLen = ref<number>(0);

const hostname = window.location.hostname;

const router = useRouter()

inputRef.value?.focus();

const swipeInput = () => {
  let input = inputRef.value
  let inputValue = inputRef.value?.value

  if (!inputValue) {
    inputValue = "";
  }

  if (input) {
    fetch("/api/enqueue-card-swipe", {
      method: "POST",
      body: JSON.stringify({"swipe_data": inputValue, "code": localStorage.getItem("auth-code")}),
      headers: {"Content-Type": "application/json"}
    }).then(res => {
      if (res.ok) {
        refreshQueueLen()
        status.value = `You're in the queue! Visit ${hostname} to track your position.`
        clearStatus();
      } else if (res.status == 400) {
        status.value = "Bad card read, please try again."
        clearStatus();
      } else if (res.status == 403) {
        status.value = "Unauthorized card swipe! Please alert course staff."
        clearStatus();
      }

      else if (res.status == 404) {
        status.value = "You are not in the roster! Please alert course staff."
        clearStatus();
      } else {
        status.value = "Something went very wrong! Please report this!"
      }
    });


    input.value = "";
  } else {
    console.log(inputValue.length);
  }
}

const clearStatus = () => {
  setTimeout(() => { status.value = "" }, 5000)
}

let pollTimeout = -1;

const refreshQueueLen = () => {
  fetch("/api/get-queue-size").then(res => {
    if (res.ok) {
      return res.json()
    }
  }).then(json => {
    queueLen.value = json["size"]
    pollTimeout = setTimeout(refreshQueueLen, 2000)
  })
}

refreshQueueLen()

// stop polling when leaving page
router.beforeEach((to, from, next) => {
  clearTimeout(pollTimeout);

  next();
})

if (localStorage.getItem("auth-code") === null) {
  router.push("/swipe-auth")
}

</script>

<template>

  <Header/>

  <div id="welcome">
    <h1>Welcome to Office Hours!</h1>
    <h2>Swipe your UB Card to join the queue.</h2>
    <h2>Visit {{ hostname }} for updates!</h2>
    <input id="swipe" type="text" ref="inputRef" autofocus @keydown.enter="swipeInput" @focusout="inputRef?.focus()">

    <div id="queue-len" class="circle pos">
      {{ queueLen }}
    </div>
    <h2>Queue Size</h2>


    <p>{{ status }}</p>
  </div>

</template>

<style scoped>

.circle {
  height: 256px;
  width: 256px;
}

#welcome {
  margin: 32px;
}

h1, h2, h3, p {
  text-align: center;
  margin: 16px;
}

#swipe {
  opacity: 0;
}

#queue-len {
  margin: auto;
  font-size: 128px;
}

br {
  margin-top: 32px;
}

footer {
  display: none;
}

</style>