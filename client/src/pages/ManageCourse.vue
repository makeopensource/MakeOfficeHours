<script setup lang="ts">

import {useRouter} from "vue-router";
import {ref} from "vue";
import EnrollmentEntry from "@/components/EnrollmentEntry.vue";
import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import Alert from "@/components/Alert.vue";

const router = useRouter()

const me = ref<Object>();

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json();
}).then(data => {
  if (data["course_role"] !== "instructor" && data["course_role"] !== "admin") {
    router.push("/queue")
  }
  me.value = data;
})

const users = ref();

const getRoster = () => fetch("/api/get-roster").then(res => {
  if (!res.ok) {
    router.push("/queue")
  }
  return res.json();
}).then(json => {
  users.value = json["roster"]
});

getRoster()

const enrollDialog = ref<typeof ConfirmationDialog>();

const uploadCSVDialog = ref<typeof ConfirmationDialog>();

const alertBox = ref<typeof Alert>();

const csvFile = ref();

const setCSVFile = (event: any) => csvFile.value = event.target?.files[0]


function uploadCSV() {
  const data = new FormData()
  data.append('roster', csvFile.value)
  fetch("/api/upload-roster", {
    method: "POST",
    body: data
  }).then(res => {
    if (!res.ok) {
      return res.json().then(json => {
        throw new Error(json["message"])
      })
    }
    getRoster();
    uploadCSVDialog.value?.hide();
    alertBox.value?.setMessage("Successfully enrolled")
  }).catch(e => {
    alertBox.value?.setError(e.message);
  })
}

const userToEnroll = ref(
    {
      "first_name": "",
      "last_name": "",
      "ubit": "",
      "person_num": "",
      "course_role": ""
    }
);

function enrollUser() {
  fetch("/api/enroll", {
    method: "POST",
    body: JSON.stringify({
      "ubit": userToEnroll.value?.ubit,
      "pn": userToEnroll.value?.person_num,
      "preferred_name": userToEnroll.value?.first_name,
      "last_name": userToEnroll.value?.last_name,
      "role": userToEnroll.value?.course_role
    }),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (!res.ok) {
      return res.json().then(json => {
        throw new Error(json["message"])
      })
    }
    enrollDialog.value?.hide();
    alertBox.value?.setMessage("Enrolled new user");
    getRoster()
  }).catch(e => {
    alertBox.value?.setError(e.message);
  })
}

</script>

<template>

  <ConfirmationDialog ref="enrollDialog">
    <h2>Enroll User</h2>
    <label for="first_name">First Name</label>
    <input id="first_name" type="text" v-model="userToEnroll.first_name">
    <label for="last_name">Last Name</label>
    <input id="last_name" type="text" v-model="userToEnroll.last_name">
    <label for="ubit">UBIT</label>
    <input id="ubit" type="text" v-model="userToEnroll.ubit">
    <label for="person_number">Person Number</label>
    <input id="person_number" type="text" v-model="userToEnroll.person_num">
    <label for="course_role">Role</label>
    <select id="course_role" v-model="userToEnroll.course_role">
      <option value="student">Student</option>
      <option value="ta">TA</option>
      <option value="instructor">Instructor</option>
    </select>
    <br/>
    <button @click="enrollUser" class="important">Submit</button>
    <button @click="enrollDialog?.hide()">Close</button>
  </ConfirmationDialog>

  <Alert ref="alertBox"/>

  <ConfirmationDialog ref="uploadCSVDialog">
    <h2>Upload Roster</h2>
    <label for="roster_cs3,v">Roster</label>
    <p>Formatted "ubit,pn,first_name,last_name,role"</p>
    <input @change="setCSVFile" name="roster" type="file" accept="text/csv">
    <button @click="uploadCSV" class="important">Submit</button>
    <button @click="uploadCSVDialog?.hide()">Close</button>
  </ConfirmationDialog>



  <div id="manage-course">
      <h2>Manage Course</h2>
      <button @click="router.push('/queue')">Return to Queue</button>
      <br/>
      <div class="manage-buttons">
        <button @click="enrollDialog?.show()">Add User to Roster</button>
        <button @click="uploadCSVDialog?.show()">Enroll from CSV</button>
        <button @click="alertBox?.setError('Not implemented')" class="danger">Clear all Enrollments</button>
      </div>
      <div id="enrollment-container">
        <table id="enrollment-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Person Number</th>
              <th>Preferred Name</th>
              <th>Last Name</th>
              <th>Role</th>
              <th>User ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <EnrollmentEntry v-for="user in users"
                             :user_id="user['user_id']"
                             :preferred_name="user['preferred_name']"
                             :last_name="user['last_name']"
                             :pn="user['person_num']"
                             :username="user['ubit']"
                             :course_role="user['course_role']"
            />
          </tbody>
        </table>
      </div>
  </div>




</template>

<style scoped>

#enrollment-container {
  justify-content: center;
  overflow-x: scroll;
}

#enrollment-table, tr, th, td {
  border: 2px solid #D9D9D9;
  border-collapse: collapse;
}

#enrollment-table {
  width: 100%;
  font-size: 1rem;
}

#manage-course {
  margin: 32px 8%;
}

.manage-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-bottom: 16px;
}

br {
  margin-bottom: 24px;
}

th {
  padding: 8px;
}

</style>