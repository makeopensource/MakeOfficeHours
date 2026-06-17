<script setup lang="ts">

import {ref, watch} from "vue";
import Table from "@/components/Table.vue";
import TableEntry from "@/components/TableEntry.vue";

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
    visitor.value = undefined
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

const headings = ['Enqueue Time', 'Visit Start Time', 'Visit End Time', 'Student Username', 'Student First Name', 'Student Last Name', 'TA Username', 'TA First Name', 'TA Last Name', '']

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
            visit["student_name"],
            visit["student_surname"],
            visit["ta_ubit"],
            visit["ta_name"],
            visit["ta_surname"],
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

const visitor: {[key: string]: any} = ref<object>();

watch(id, getName)

async function getName() {
  if (id.value !== undefined) {
    fetch(`/api/user/${id.value}`).then(res => {
      return res.json()
    }).then(json => {
      visitor.value = json
    })
  } else {
    visitor.value = undefined
  }
}

function exportVisits() {
  let csv = "Enqueue Time,Visit Start Time,Visit End Time,Student Username,Student First Name,Student Last Name,TA Username,TA First Name,TA Last Name,Student Visit Reason,TA Visit Notes\n";
  for (let visit of visits.value) {
    let info = ""
    for (let i = 0; i < visit.length - 1; i++) {
      info += visit[i] != null ? `${visit[i]},` : ','
    }
    info += visit[visit.length-1] != null ? `${visit[visit.length-1]}\n` : '\n'
    csv += info
  }
  const link = document.createElement("a")
  const file = new Blob([csv], {type: "text/csv"})
  link.href = URL.createObjectURL(file)
  link.download = "visits" + `${id.value !== undefined ? `-${visitor.value["ubit"]}` : ''}` + ".csv"
  link.click()
  URL.revokeObjectURL(link.href)
}

</script>

<template>

  <dialog @close="$emit('close')" v-show="showing" ref="dialogRef" id="visit-tbl-dialog" class="modal">

    <h2>{{ visitor != undefined ? `${visitor["preferred_name"]}'s ` : '' }}Visits</h2>

    <div id="inputs">
      <div id="input-l">
        <input type="checkbox" id="filter-blank" v-model="hideWeird" @change="filterWeirds">
        <label for="filter-blank">Hide Removals and Incomplete Visits</label>
      </div>
      <div id="buttons">
        <button @click="exportVisits" v-if="visits.length > 0">Export to CSV</button>
        <button @click="hide">Close</button>
      </div>
    </div>
    <br/>

    <div v-if="visits.length === 0" class="ominous-text">But nobody came.<br/></div>
    <div v-if="visits.length === 0" class="ominous-text">(No visits for this user)</div>

    <Table id="visits-tbl" v-if="visits.length > 0" :headings="headings" :table_data="visits">
      <TableEntry v-for="visit in visits" :data="visit.slice(0, 9)">
        <td><button @click="emit('show-visit', visit)" class="view-btn">View</button></td>
      </TableEntry>
    </Table>
  </dialog>
</template>

<style scoped>

#visit-tbl-dialog {
  max-width: 80vw;
}

.ominous-text {
  margin-bottom: 12px;
}

#visits-tbl {
  overflow-x: scroll
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