<script setup lang="ts">

import {ref} from "vue";

defineProps(["name", "ubit", "id"])
defineEmits(["call-student"])

</script>


<template>
  <div class="queue-entry">
    <div class="queue-entry-info">{{ name }} ({{ ubit }})</div>
    <div class="queue-entry-buttons">
      <button @click="$emit('call-student', id)">Call</button>
      <button>Remove</button>
      <button>Move to End</button>
    </div>
  </div>

</template>

<style scoped>

.queue-entry {
  display: flex;
  border-bottom: 2px solid #D9D9D9;
  border-top: 0;
  align-items: center;
  padding: 16px;
  background-color: #F5F5F5;
}

.queue-entry-info {
  font-weight: bold;
}

.queue-entry-buttons {
  margin-left: auto;
  display: flex;
  gap: 4px;
}

</style>