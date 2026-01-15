<script setup lang="ts">

import QueueEntry from "@/components/QueueEntry.vue";
import {ref} from "vue";
import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import Visit from "@/components/Visit.vue";

const students = ref([])

function getQueue() {
  fetch("/api/get-queue").then(res => {
    return res.json()
  }).then(data => {
    students.value = data
  })
}

function poll() {
  getQueue();
  setTimeout(poll, 2000);
}

poll();

const forceEnqueueDialog = ref<typeof ConfirmationDialog>();
const forceEnqueueEntry = ref('');
const forceEnqueueErrorMessage = ref('');


function submitForceEnqueue() {
  fetch("/api/enqueue-ta-override", {
    method: "POST",
    body: JSON.stringify({"identifier": forceEnqueueEntry.value}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      forceEnqueueDialog.value?.hide();
      getQueue();
    }
    return res.json()
  }).then(data => {
    forceEnqueueErrorMessage.value = data["message"]
  })
}

function resetForceEnqueueDialog() {
  forceEnqueueEntry.value = "";
  forceEnqueueErrorMessage.value = "";
}

const visitInfo = ref({})
const visitDialog = ref<typeof Visit>();

function callStudent(id: number) {

  fetch("/api/help-a-student", {
    method: "POST",
    body: JSON.stringify({"id": id}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (!res.ok) {
      throw new Error("failed to dequeue student")
    }
    return res.json()
  }).then(data => {
    visitInfo.value = data;
    visitDialog.value?.show();
  })
}

const clearQueueDialog = ref<typeof ConfirmationDialog>();

function clearQueue() {
  fetch("/api/clear-queue", {
    method: "DELETE"
  }).then(res => {
    if (res.ok) {
      clearQueueDialog.value?.hide();
      getQueue();
    }
  })
}

</script>

<template>

  <Visit ref="visitDialog" :visit_info="visitInfo"/>

  <ConfirmationDialog @open="resetForceEnqueueDialog" ref="forceEnqueueDialog">
    <label for="force-enqueue">Student Identifier (UBITName or Person Number)</label><br/>
    <input v-model="forceEnqueueEntry" type="text" id="force-enqueue" class="flex" name="force-enqueue">

    <div class="input-modal-container">
      <button id="close-enqueue-dialog" @click="forceEnqueueDialog?.hide()" class="no-grow">Cancel</button>
      <button id="submit-force-enqueue" @click="submitForceEnqueue" class="no-grow important">Submit</button>
    </div>

    <p id="enqueue-error-message">{{ forceEnqueueErrorMessage }}</p>
  </ConfirmationDialog>

  <ConfirmationDialog ref="clearQueueDialog">
    <p><strong>Are you sure?</strong></p>
    <p>If you clear the queue, <strong>all students</strong> will permanently lose their position.</p>
    <div class="input-modal-container">
      <button @click="clearQueueDialog?.hide()" id="clear-queue-cancel">No, keep everyone's position in the queue.
      </button>
      <button @click="clearQueue" id="clear-queue-confirm" class="danger">Yes, clear the queue.</button>
    </div>
    <p id="clear-queue-error-message"></p>
  </ConfirmationDialog>
  <dialog id="force-enqueue-dialog" class="small-modal">


  </dialog>

  <dialog id="clear-queue-dialog" class="small-modal">

  </dialog>


  <div id="instructor-queue">
    <div class="queue-section">
      <h2 id="welcome-text">Hello, Jimmy!</h2>
      <h2 id="student-count-text">{{ students?.length }} students in the queue.</h2>
    </div>
    <div id="queue-buttons" class="queue-section">
      <div id="buttons-l">
        <button>Edit My Info</button>
        <button>Clock In</button>
      </div>
      <div id="buttons-r">
        <button id="manage-course-button">Manage Course</button>
        <button @click="forceEnqueueDialog?.show()" id="enqueue-dialog-button">Enqueue Student</button>
        <button @click="clearQueueDialog?.show()" id="clear-queue-dialog-button" class="danger">Clear Queue</button>
      </div>
    </div>
    <div id="queue-container" class="queue-section">
      <QueueEntry v-for="student in students" :name="student['preferred_name']" :ubit="student['ubit']"
                  :id="student['id']" @call-student="callStudent"/>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/css/instructor-queue.css";
</style>