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

const me = ref<any>({});
const manager = ref<boolean>(false);

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json();
}).then(data => {
  if (data["course_role"] === "student") {
    router.push("/queue")
  }
  if (data["course_role"] !== "ta") {
    manager.value = true;
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
    "preferred_name": `${visit[4]} ${visit[5]}`,
    "username": visit[3],
    "visit_reason": visit[9],
    "visit_result": visit[10]
  }
  visitRef.value?.show()
}

function deleteUser(user: string) {
  fetch(`/api/user/${user}`, { method: "DELETE"}).then(res => {
      if (!res.ok) {
        alertBox.value?.setError("Failed to remove user")
      } else {
        getRoster()
      }
    }
  )
}

const clearDialog = ref<typeof ConfirmationDialog>();

function clearStudents() {
  fetch("/api/clear-enrollments", { method: "DELETE"} ).then(res => {
    if (!res.ok) {
      alertBox.value?.setError("Failed to clear roster.")
    } else {
      getRoster();
    }
  })
}

function updateRole(user: string, role: string) {
  fetch(`/api/user/${user}/role`, {
    method: "PATCH",
    body: JSON.stringify({"role": role}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (!res.ok) {
      res.json().then((json) => {
        alertBox.value?.setError(`Failed to change role: ${json["message"]}`)
        getRoster()
      })

    }
  })
}

function rolePrettyName(role: string) {
  switch (role) {
    case "student": return "Student"
    case "ta": return "TA"
    case "instructor": return "Instructor"
    case "admin": return "Admin"
    default: return "IDK"
  }
}

</script>

<template>

  <Visit ref="visitRef" :visit_info="visitInfo" :read_only="true"/>

  <ConfirmationDialog ref="clearDialog">
    <p>
      This will delete all students from the course. Reversing this action will be difficult.
    </p>
    <button class="danger" @click="clearStudents">Delete the students!</button>
    <button @click="clearDialog?.hide()">Close</button>

  </ConfirmationDialog>

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
      <option value="ta" v-if="manager">TA</option>
      <option value="instructor" v-if="manager">Instructor</option>
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

  <VisitTable id="visit-tbl" ref="visitTable" @show-visit="showOldVisit" />


  <div id="manage-course">
      <h2>Manage Course</h2>
      <button id="return-btn" @click="router.push('/queue')">Return to Queue</button>
      <br/>
      <div class="manage-buttons">
        <button v-if="manager" @click='visitTable?.show()'>View All Visits</button>
        <button @click="hardwareDialog?.show()">Authorize Swipe</button>
        <button @click="enrollDialog?.show()">Add User to Roster</button>
        <button @click="uploadCSVDialog?.show()">Enroll from CSV</button>
        <button v-if="manager" @click="clearDialog?.show()" class="danger">Remove all Students</button>
      </div>
    <Table id="users-tbl" :headings="['User ID', 'Username', 'Preferred Name', 'Last Name', 'Person Number', 'Role', 'Actions']">

      <TableEntry v-for="user in users" :data="user.slice(0, 5)">
        <td>
          <select v-if="user[0] != me['user_id']" v-model="user[5]" @change="() => updateRole(user[0], user[5])">
            <option value="student" v-if="user[5] != 'admin'">Student</option>
            <option value="ta" v-if="user[5] != 'admin'">TA</option>
            <option value="instructor" v-if="user[5] != 'admin'">Instructor</option>
            <option value="admin" v-if="user[5] == 'admin'">Admin</option>
          </select>
          <span v-else>{{rolePrettyName(user[5])}}</span>
        </td>
        <td id="actions">
              <button v-if="me['course_role'] !== 'ta' || me['user_id'] == user[0]" @click="visitTable?.show(user[0])">Visits</button>
              <button @click="() => deleteUser(user[0])" v-if="me['user_id'] != user[0] && (user[5] == 'student' || (me['course_role'] != 'ta' && user[5] != 'admin'))" class="danger">Remove</button>
        </td>
      </TableEntry>
    </Table>

  </div>


</template>

<style scoped>

@media screen and (max-width: 991px) {

  h2 {
    text-align: center;
  }

  .manage-buttons {
    flex-direction: column;
  }

  #return-btn {
    margin: auto;
    display: flex;
  }

  #users-tbl {
    overflow-x: scroll;
  }
}

#actions {
  display: flex;
  gap: 4px;
  justify-content: center;
  border: none;
  padding: 4px;
}

tr, th, td {
    border: 2px solid #D9D9D9;
    border-collapse: collapse;
  }

td {
  padding: 8px;
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