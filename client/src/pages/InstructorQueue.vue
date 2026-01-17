<script setup lang="ts">

import QueueEntry from "@/components/QueueEntry.vue";
import {ref} from "vue";
import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import Visit from "@/components/Visit.vue";
import EditInfo from "@/components/EditInfo.vue";
import {useRouter} from "vue-router";

const students = ref([])

const router = useRouter()

const taName = ref<string>("");

const courseManager = ref<boolean>(false);

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json()
}).then(data => {
  taName.value = data["preferred_name"]
  courseManager.value = data["course_role"] == 'instructor' || data["course_role"] == 'admin'
})

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


const removeStudentDialog = ref<typeof ConfirmationDialog>();
let removeStudentId: number | undefined = undefined;
const removeStudentReason = ref("");

function showRemoveStudentDialog(id: number) {
  removeStudentId = id;
  removeStudentDialog.value?.show();
}

function removeStudent() {
  fetch("/api/remove-from-queue", {
    method: "POST",
    body: JSON.stringify({"reason": removeStudentReason.value, "user_id": removeStudentId}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      removeStudentDialog.value?.hide();
      removeStudentReason.value = "";
      removeStudentId = undefined;
      getQueue();
    }
  })
}

const editInfo = ref<typeof EditInfo>();

function getInProgressVisit() {
  fetch("/api/restore-visit").then(res => {
    if (!res.ok) {
      throw new Error("No in-progress visit found.")
    }
    return res.json()
  }).then(data => {
    visitInfo.value = data
    visitDialog.value?.show()
  }).catch(() => {})
}

getInProgressVisit()

function signOut() {
  fetch("/api/signout", { method: "POST" }).then(res => {
    if (res.ok) {
      router.push("/")
    }
  })
}

</script>

<template>

  <Visit ref="visitDialog" :visit_info="visitInfo" @close="getInProgressVisit"/>

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

  <ConfirmationDialog ref="removeStudentDialog">
      <p><strong>Are you sure?</strong> This student will permanently lose their position in the queue.</p>
      <br/>
      <label for="remove-student-reason">Reason</label>
      <textarea v-model="removeStudentReason" class="modal-big-text" id="remove-student-reason" placeholder="Why is this student being removed?" required></textarea>
      <div class="input-modal-container">
        <button @click="removeStudentDialog?.hide()" id="remove-student-cancel">No, keep this student in the queue.</button>
        <button @click="removeStudent" id="remove-student-confirm" class="danger">Yes, remove this student.</button>
      </div>
  </ConfirmationDialog>

  <EditInfo is_instructor="true" @name-change="(name) => { taName = name }" :default_name="taName" ref="editInfo"/>


  <div id="instructor-queue">
    <div class="queue-section">
      <h2 id="welcome-text">Hello, {{ taName }}!</h2>
      <h2 id="student-count-text">{{ students?.length }} student{{ students?.length !== 1 ? "s" : "" }} in the queue.</h2>
    </div>
    <div id="queue-buttons" class="queue-section">
      <div id="buttons-l">
        <button @click="editInfo?.show()">Edit My Info</button>
        <button>Clock In</button>
        <button id="signout" @click="signOut">Sign Out</button>
      </div>
      <div id="buttons-r">
        <button v-show="courseManager" id="manage-course-button">Manage Course</button>
        <button @click="forceEnqueueDialog?.show()" id="enqueue-dialog-button">Enqueue Student</button>
        <button @click="clearQueueDialog?.show()" id="clear-queue-dialog-button" class="danger">Clear Queue</button>
      </div>
    </div>
    <div id="queue-container" class="queue-section">
      <QueueEntry v-for="student in students" :name="student['preferred_name']" :ubit="student['ubit']"
                  :id="student['id']" @call-student="callStudent" @remove-student="showRemoveStudentDialog"/>
    </div>
  </div>
</template>

<style scoped>
@import "../assets/css/instructor-queue.css";
</style>