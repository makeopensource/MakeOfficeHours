<script setup lang="ts">

import QueueControlEntry from "@/components/QueueControlEntry.vue";

defineProps(["name", "ubit", "id"])
defineEmits(["enqueue-student", "remove-student"])

</script>

<template>

  <QueueControlEntry>
    <template #info>{{ name }} ({{ ubit }})</template>
    <template #buttons>
      <button @click="$emit('enqueue-student', id)">Add to Queue</button>
      <button @click="$emit('remove-student', id)" class="danger">Deactivate</button>
    </template>
    <template #dropdown-buttons>
      <button @click="$emit('enqueue-student', id)">Add to Queue</button>
      <button @click="$emit('remove-student', id)" class="danger">Deactivate</button>
    </template>
  </QueueControlEntry>

</template>

<style scoped>

</style>