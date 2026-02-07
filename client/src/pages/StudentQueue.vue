<script setup lang="ts">

import {ref} from "vue";
import {useRouter} from "vue-router";
import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import EditInfo from "@/components/EditInfo.vue";
import Alert from "@/components/Alert.vue";

const router = useRouter()

let enqueued = ref(false)

let studentName = ref("")
let studentPos = ref("N/A")
let queueLen = ref(0)

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json()
}).then(data => {
  studentName.value = `${data["preferred_name"]}`
})

let bannerClass = ref("bad")
let bannerText = ref("You are not in the queue!")

const leaveQueueDialog = ref<typeof ConfirmationDialog>();

function fetchPosition() {
  fetch("/api/get-my-position").then(
      res => {
        return res.json()
      }
  ).then(data => {
    queueLen.value = data["length"]
    if (data["position"] !== undefined) {
      studentPos.value = data["position"]
      bannerClass.value = ""
      bannerText.value = "You are in the queue!"
      enqueued.value = true
    } else {
      studentPos.value = "N/A"
      bannerClass.value = "bad"
      bannerText.value = "You are not in the queue!"
      enqueued.value = false
    }

  })
}

let pollTimeout = -1;

function poll() {
  fetchPosition();
  pollTimeout = setTimeout(poll, 2000);
}

poll()

// stop timeout when leaving queue so requests don't get spammed
router.beforeEach((to, from, next) => {
  clearTimeout(pollTimeout);

  next();
})

const selfDequeueReason = ref<HTMLTextAreaElement>();

function leaveQueue() {

  selfDequeueReason.value?.reportValidity()

  if (selfDequeueReason.value?.checkValidity()) {
    fetch("/api/remove-self-from-queue", {
      method: "POST",
      body: JSON.stringify({"reason": selfDequeueReason.value?.value}),
      headers: {"Content-Type": "application/json"}
    }).then((res) => {
      if (!res.ok) {
        throw new Error("failed to remove from queue")
      }
      leaveQueueDialog.value?.hide();
      fetchPosition();
    }).catch(e => {
      alertBox.value?.setError("Failed to remove from queue. Please tell your SA.")
    })
  }
}

const queueReason = ref<HTMLTextAreaElement>();

function updateReason() {

  fetch("/api/update-reason", {
    method: "PATCH",
    body: JSON.stringify({"reason": queueReason.value?.value}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      alertBox.value?.setMessage("Updated your visit reason. Thank you!")
    } else {
      alertBox.value?.setError("Failed to update visit reason. Please notify your SA.")
    }
  })

}

const preferredNameUpdate = ref<typeof ConfirmationDialog>();

function signOut() {
  fetch("/api/signout", { method: "POST" }).then(res => {
    if (res.ok) {
      router.push("/")
    }
  })
}

const alertBox = ref<typeof Alert>();

</script>

<template>

  <header id="queue-banner" :class="bannerClass">{{ bannerText }}</header>

  <ConfirmationDialog ref="leaveQueueDialog">
    <p><strong>Sorry to see you go!</strong> If you leave the queue now, you'll lose your position.</p>
    <p>To rejoin, you will have to swipe back in.</p>
    <br/>
    <div class="columns all-centered left-al">
      <label for="self-dequeue-reason">Why are you leaving the queue?</label>
      <textarea ref="selfDequeueReason" id="self-dequeue-reason" class="modal-big-text" required></textarea>
    </div>
    <div class="button-container">
      <button @click="leaveQueueDialog?.hide()" id="close-dequeue-dialog">Nevermind, return to queue.</button>
      <button @click="leaveQueue" id="submit-self-dequeue" class="important">End Visit</button>
    </div>
  </ConfirmationDialog>

  <EditInfo ref="preferredNameUpdate" :default_name="studentName" @name-change="(name) => { studentName = name }"/>

  <Alert ref="alertBox"/>

  <div id="queue">
    <div id="info" class="queue-section">
      <div id="user">
        <h2 id="student-name">{{ studentName }}</h2>
        <button id="edit" @click="preferredNameUpdate?.show()">Edit Info</button>
      </div>
    </div>
    <div id="position-info" class="queue-section">
      <div class="all-centered columns">
        <div id="my-position" class="circle pos">{{ studentPos }}</div>
        Your Position
      </div>
      <div class="all-centered columns">
        <div id="queue-length" class="circle pos">{{ queueLen }}</div>
        Queue Size
      </div>
    </div>
    <br/>
    <div class="queue-section columns all-centered">
      <div class="columns left-al">
        <label for="student-visit-reason">Visit Reason</label>
        <textarea ref="queueReason" :disabled="!enqueued" id="student-visit-reason"
                  placeholder="What brings you to office hours?"></textarea>
        <button @click="updateReason" :disabled="!enqueued" id="submit-updated-reason" class="right-al-item">Update
          Reason
        </button>
      </div>
    </div>
    <div class="queue-section columns all-centered">
      <button :disabled="!enqueued" @click="leaveQueueDialog?.show()" class="wide-button danger">Exit Queue</button>
      <button @click="signOut" class="wide-button">Sign Out {{ enqueued ? "(will not remove you from queue)" : "" }}</button>
    </div>
  </div>


</template>

<style scoped>
@import "../assets/css/student-queue.css";
</style>