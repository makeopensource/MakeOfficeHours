<script setup lang="ts">

import {nextTick, ref, watch} from "vue";
import StudentQueue from "@/pages/StudentQueue.vue";
import Table from "@/components/Table.vue";
import TableEntry from "@/components/TableEntry.vue";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";

const props = defineProps(["id"])
const emit = defineEmits(["open", "close", "show-visit"])

const hideWeird = ref<any>(false);

const dialogRef = ref<HTMLDialogElement>();
const showing = ref<boolean>(false);

const unf = ref<Array<any>>([]);

const id = ref<number>();

const show = (user: number) => {
  dialogRef.value?.showModal();
  showing.value = true;
  emit("open")

  if (user === undefined) {
    visitor.value = ""
  }
  id.value = user;
  getVisits();
}

const hide = () => {
  dialogRef.value?.close()
  showing.value = false;
  emit("close")
}

defineExpose({show: show, hide: hide})

const visits = ref<Array<Array<any>>>([]);

const headings = ['Enqueue Time', 'Visit Start Time', 'Visit End Time', 'Student Username', 'Student Name', 'TA Username', 'TA Name', '']

const getVisits = () => fetch(`/api/visits${id.value !== undefined ? `/${id.value}` : ''}`).then(res => {
  return res.json();
}).then(json => {

  if (json["message"] !== undefined) {
    return;
  }

  const newVisits: Array<any> = []

  const vis: Array<any> = json["visits"]

  vis.sort((a, b) => { return -a["enqueue_time"].localeCompare(b["enqueue_time"]) })

  vis.forEach((visit) => {
    newVisits.push(
        [
            visit["enqueue_time"],
            visit["session_start"],
            visit["session_end"],
            visit["student_ubit"],
            `${visit["student_name"]} ${visit["student_surname"]}`,
            `${visit["ta_ubit"] != null ? `${visit["ta_ubit"]}` : '-'}`,
            `${visit['ta_ubit'] != null ? `${visit["ta_name"]} ${visit["ta_surname"]}` : '-'}`,
            visit["student_visit_reason"],
            visit["session_end_reason"]
        ]
    )
  })
  unf.value = newVisits
  visits.value = newVisits

  if (hideWeird.value) {
    filterWeirds();
  }

});

getVisits()

function filterWeirds() {
  if (hideWeird.value == true) {
    visits.value = unf.value.filter((val) => {
      let passed = true;
      for (let entry of val.slice(0, 7)) {
        if (entry === null || entry === '-') {
          passed = false;
        }
      }
      return passed;
    })
  } else {
    visits.value = unf.value
  }
}

function weirdTest() {
  const ar2: Array<any> = [...visits.value]

  ar2.sort((a, b) => { return a[0].localeCompare(b[0]) })

  visits.value = ar2;
}

const visitor = ref<string>("ASD!");

watch(id, getName)

async function getName() {
  if (id.value !== undefined) {
    fetch(`/api/user/${id.value}`).then(res => {
      return res.json()
    }).then(json => {
      visitor.value = `${json["preferred_name"]}'s `
    })
  }
  return ""
}

</script>

<template>

  <dialog @close="$emit('close')" v-show="showing" ref="dialogRef" id="visit" class="modal">

    <h2>{{ visitor }}Visits</h2>

    <div id="inputs">
      <div id="input-l">
        <input type="checkbox" id="filter-blank" v-model="hideWeird" @change="filterWeirds">
        <label for="filter-blank">Hide Self-Removals and Incomplete Visits</label>
      </div>
      <div id="buttons">
        <button @click="weirdTest" v-if="visits.length > 0">Export</button>
        <button @click="hide">Close</button>
      </div>
    </div>
    <br/>

    <div v-if="visits.length === 0" class="ominous-text">But nobody came.<br/></div>
    <div v-if="visits.length === 0" class="ominous-text">(No visits for this user)</div>

    <Table v-if="visits.length > 0" :headings="headings" :table_data="visits">
      <TableEntry v-for="visit in visits" :data="visit.slice(0, 7)">
        <td><button @click="emit('show-visit', visit)" class="view-btn">View</button></td>
      </TableEntry>
    </Table>
  </dialog>
</template>

<style scoped>

.ominous-text {
  margin-bottom: 12px;
}

#inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

#input-l {
  display: flex;
  align-items: center;
  gap: 4px;
}

#buttons {
  margin-left: auto;
  display: flex;
  gap: 4px;
}

dialog {
  max-height: 60%;
}

.view-btn {
  padding: 8px;
  margin: 4px;
}


</style>