<script setup lang="ts">

import {nextTick, ref} from "vue";
import StudentQueue from "@/pages/StudentQueue.vue";
import Table from "@/components/Table.vue";
import TableEntry from "@/components/TableEntry.vue";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";

const props = defineProps(["id"])
const emit = defineEmits(["open", "close", "show-visit"])

const dialogRef = ref<HTMLDialogElement>();
const showing = ref<boolean>(false);

const id = ref<number>();

const show = (user: number) => {
  dialogRef.value?.showModal();
  showing.value = true;
  emit("open")
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
  visits.value = []
  return res.json();
}).then(json => {

  if (json["message"] !== undefined) {
    return;
  }

  const vis: Array<any> = json["visits"]

  vis.sort((a, b) => { return -a["enqueue_time"].localeCompare(b["enqueue_time"]) })

  vis.forEach((visit) => {
    visits.value.push(
        [
            visit["enqueue_time"],
            visit["session_start"],
            visit["session_end"],
            visit["student_ubit"],
            `${visit["student_name"]} ${visit["student_surname"]}`,
            visit["ta_ubit"],
            `${visit["ta_name"]} ${visit["ta_surname"]}`,
            visit["student_visit_reason"],
            visit["session_end_reason"]
        ]
    )
  })
});

getVisits()


</script>

<template>

  <dialog @close="$emit('close')" v-show="showing" ref="dialogRef" id="visit" class="modal">
    <div v-if="visits.length === 0" class="ominous-text">But nobody came.<br/></div>
    <div v-if="visits.length === 0" class="ominous-text">(No visits for this user)</div>

    <div id="buttons">
      <button @click="hide()" v-if="visits.length > 0">Export</button>
      <button @click="hide()">Close</button>
    </div>

    <br/>

    <Table v-if="visits.length > 0" :headings="headings" :table_data="visits">
      <TableEntry v-for="visit in visits" :data="visit.slice(0, 7)">
        <button @click="emit('show-visit', visit)" class="view-btn">View</button>
      </TableEntry>
    </Table>
  </dialog>
</template>

<style scoped>

.ominous-text {
  margin-bottom: 12px;
}

#buttons {
  justify-content: end;
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