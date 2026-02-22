<script setup lang="ts">

import QueueControlEntry from "@/components/QueueControlEntry.vue";

defineProps(["name", "ubit", "id"])
defineEmits(["call-student", "remove-student", "move-to-end"])

</script>


<template>

  <QueueControlEntry>
    <template #info>{{name}} ({{ubit}})</template>
    <template #buttons>
        <button @click="$emit('call-student', id)">Start Visit</button>
        <button @click="$emit('remove-student', id)">Remove</button>
        <button @click="$emit('move-to-end', id)">Move to End</button>
    </template>
    <template #dropdown-buttons>
        <button @click="$emit('call-student', id);">Call</button>
        <button @click="$emit('remove-student', id);">Remove</button>
        <button @click="$emit('move-to-end', id);">Move to End</button>
    </template>
  </QueueControlEntry>



</template>

<style scoped>

</style>