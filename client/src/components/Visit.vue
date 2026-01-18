<script setup lang="ts">

import {ref} from "vue";
import {send} from "vite";

const props = defineProps(["visit_info"])
const emit = defineEmits(["close"])

const dialogRef = ref<HTMLDialogElement>();
const showing = ref<boolean>(false);

const taNotesBox = ref<HTMLTextAreaElement>();
const taNotesText = ref("");

const show = () => {
  dialogRef.value?.showModal();
  showing.value = true;
}

const hide = () => {
  dialogRef.value?.close()
  showing.value = false;
  taNotesText.value = "";
  emit("close")
}

defineExpose({show: show, hide: hide})


function submitVisit(after?: () => void) {
  taNotesBox.value?.reportValidity();

  if (taNotesBox.value?.checkValidity()) {
    fetch("/api/end-visit", {
      method: "POST",
      body: JSON.stringify({"id": props?.visit_info["visitID"], "reason": taNotesText.value}),
      headers: {"Content-Type": "application/json"}
    }).then(res => {
      if (res.ok && after) {
        after();
      } else if (res.ok) {
        hide();
      }
    })
  }
}

const sendToFront = () => {
  fetch("/api/enqueue-override-front", {
    method: "POST",
    body: JSON.stringify({ "identifier": props.visit_info["username"] }),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      hide();
    }
  })
}

const sendToBack = () => {
  fetch("/api/enqueue-ta-override", {
    method: "POST",
    body: JSON.stringify({"identifier": props.visit_info["username"]}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      hide();
    }
  })
}


</script>

<template>
  <dialog @keydown.esc.prevent="" @close="$emit('close')" v-show="showing" ref="dialogRef" id="visit" class="modal">

    <div id="student-info">
      <h2 id="visit-student-name">{{ visit_info["preferred_name"] }}</h2>
      <h3 id="visit-student-email">{{ visit_info["username"] }}@buffalo.edu</h3>
      <button disabled>View Autolab Submission</button>
      <br/>
      <label for="student-visit-reason">Visit Reason</label>
      <textarea class="visit-reason-textbox" id="student-visit-reason" disabled>{{ visit_info["visit_reason"] !== null ? visit_info["visit_reason"] : "None provided."}}</textarea>
    </div>

    <div id="visit-controls">
      <label for="ta-visit-notes">Visit Notes</label>
      <textarea ref="taNotesBox" v-model="taNotesText" id="ta-visit-notes" placeholder="How did the visit go?"
                required></textarea>
      <button @click="() => submitVisit()" id="end-visit">End Visit</button>
      <button @click="() => submitVisit(sendToFront)" id="end-visit-return-front">End and Return to Front</button>
      <button @click="() => submitVisit(sendToBack)" id="end-visit-return-back">End and Return to Back</button>
    </div>


  </dialog>
</template>

<style scoped>
@import "../assets/css/visit.css";
</style>