<script setup lang="ts">

import {useRouter} from "vue-router";
import {ref} from "vue";
import TableEntry from "@/components/TableEntry.vue";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import Alert from "@/components/common/Alert.vue";
import Table from "@/components/Table.vue";
import Visit from "@/components/instructor/Visit.vue";
import VisitTable from "@/components/instructor/VisitTable.vue";

const router = useRouter()

const me = ref<any>();

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json();
}).then(data => {
  if (data["course_role"] === "student") {
    router.push("/queue")
  }
  me.value = data;
  getCode();
})

const users = ref<Array<Array<any>>>([]);

const getRoster = () => fetch("/api/get-roster").then(res => {
  if (!res.ok) {
    router.push("/queue")
  }
  return res.json();
}).then(json => {
  users.value = []
  const roster: Array<any> = json["roster"]

  roster.sort((a, b) => { return a["ubit"].localeCompare(b["ubit"]) })

  roster.forEach((user) => {
    users.value.push([user["user_id"], user["ubit"], user["preferred_name"], user["last_name"], user["person_num"], user["course_role"]])
  })
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

let hardwareDialog = ref<typeof ConfirmationDialog>();

let hardwareCode = ref<string>();



const getCode = () => {
  fetch("/api/swipe-authorization").then(res => res.json()).then(json => {
    hardwareCode.value = json["code"]
  })
}

const resetAuth = () => {
  fetch("/api/reset-swipe-auth", {
    method: "DELETE"
  }).then(() => {
    getCode()
  })


}

const visitTable = ref<typeof VisitTable>();
const visitRef = ref<typeof Visit>();

const visitInfo = ref({});

function showOldVisit(visit: Array<any>) {
  visitInfo.value = {
    "preferred_name": visit[4],
    "username": visit[3],
    "visit_reason": visit[7],
    "visit_result": visit[8]
  }
  visitRef.value?.show()
}

</script>

<template>

  <Visit ref="visitRef" :visit_info="visitInfo" :read_only="true"/>

  <ConfirmationDialog ref="hardwareDialog">

    <label for="auth_code">Authorization Code</label>
    <input v-model="hardwareCode" id="auth_code" disabled>
    <button class="danger" @click="resetAuth">Reset Code</button>
    <button @click="hardwareDialog?.hide()">Close</button>

  </ConfirmationDialog>

  <ConfirmationDialog ref="enrollDialog" @enter="enrollUser">
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

  <ConfirmationDialog ref="uploadCSVDialog" @enter="uploadCSV">
    <h2>Upload Roster</h2>
    <label for="roster_cs3,v">Roster</label>
    <p>Formatted "ubit,pn,first_name,last_name,role"</p>
    <input @change="setCSVFile" name="roster" type="file" accept="text/csv">
    <button @click="uploadCSV" class="important">Submit</button>
    <button @click="uploadCSVDialog?.hide()">Close</button>
  </ConfirmationDialog>

  <VisitTable ref="visitTable" @show-visit="showOldVisit" />


  <div id="manage-course">
      <h2>Manage Course</h2>
      <button @click="router.push('/queue')">Return to Queue</button>
      <br/>
      <div class="manage-buttons">
        <button @click="hardwareDialog?.show()">Authorize Swipe</button>
        <button @click="enrollDialog?.show()">Add User to Roster</button>
        <button @click="uploadCSVDialog?.show()">Enroll from CSV</button>
        <button @click="alertBox?.setError('Not implemented')" class="danger">Clear all Enrollments</button>
      </div>
    <Table :headings="['User ID', 'Username', 'Preferred Name', 'Last Name', 'Person Number', 'Role', 'Actions']">

      <TableEntry v-for="user in users" :data="user">
        <td id="actions">
              <button v-if="me['course_role'] !== 'ta' || me['user_id'] == user[0]" @click="visitTable?.show(user[0])">Visits</button>
              <button v-if="me['user_id'] != user[0]" class="danger">Remove</button>
        </td>
      </TableEntry>
    </Table>

  </div>


</template>

<style scoped>

#actions {
    display: flex;
    gap: 4px;
    justify-content: center;
    border: none;
    padding: 4px;
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


</style>