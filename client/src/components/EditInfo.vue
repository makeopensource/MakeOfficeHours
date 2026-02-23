<script setup lang="ts">

import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import {nextTick, ref} from "vue";

const props = defineProps(["default_name", "is_instructor"]);
const emit = defineEmits(["name-change"])

const dialog = ref<typeof ConfirmationDialog>();

const entry = ref<string>(props?.default_name);

function resetEntry() {
  entry.value = props?.default_name;
}

function submitNameChange() {
  fetch("/api/update-name", {
    method: "PATCH",
    body: JSON.stringify({"name": entry.value}),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      dialog.value?.hide()
      emit("name-change", entry.value)
    }
  })
}

const nameInput = ref<HTMLInputElement>();

defineExpose({"show": () => dialog.value?.show(), "hide": () => dialog.value?.hide()})


</script>

<template>

  <ConfirmationDialog @open="() => {resetEntry; nextTick(() => {nameInput?.focus()})}" @enter="submitNameChange" ref="dialog">
    <h3>Edit Info</h3>
    <p v-if="is_instructor">Your preferred name will be visible to students using the site.</p>
    <p v-else>Your preferred name will be your identifier on the queue and will be visible to TAs.</p>

    <br/>

    <label for="preferred-name">Preferred Name</label>
    <input id="preferred-name" v-model="entry" ref="nameInput">

    <button @click="submitNameChange" class="important">Change Preferred Name</button>
    <button @click="dialog?.hide()">Close</button>
  </ConfirmationDialog>

</template>

<style scoped>

</style>