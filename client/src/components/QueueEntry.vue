<script setup lang="ts">

import {ref} from "vue";

defineProps(["name", "ubit", "id"])
defineEmits(["call-student", "remove-student", "move-to-end"])

const dropdownVisible = ref<boolean>(false);

</script>


<template>
  <div class="queue-entry-container">
      <div @click='dropdownVisible = !dropdownVisible' class="queue-entry">
      <div class="queue-entry-info">{{ name }} ({{ ubit }})</div>
      <div class="queue-entry-buttons">
        <button @click="$emit('call-student', id)">Call</button>
        <button @click="$emit('remove-student', id)">Remove</button>
        <button @click="$emit('move-to-end', id)">Move to End</button>
      </div>
      <div :class="dropdownVisible ? 'open' : '' " class="queue-dropdown-toggle">&#9658;</div>
    </div>
    <div ref="dropdown" :class="dropdownVisible ? 'visible' : ''" class="queue-entry-dropdown">
      <div class="dropdown-buttons">
        <button @click="$emit('call-student', id); dropdownVisible = false">Call</button>
        <button @click="$emit('remove-student', id); dropdownVisible = false">Remove</button>
        <button @click="$emit('move-to-end', id); dropdownVisible = false">Move to End</button>
      </div>
    </div>
  </div>


</template>

<style scoped>

.queue-entry {
  display: flex;
  border-bottom: 2px solid #D9D9D9;
  border-top: 0;
  justify-content: flex-start;
  align-items: center;
  padding: 16px;
  background-color: #F5F5F5;
}

.queue-entry-container {
  display: flex;
  flex-direction: column;
}

.queue-entry-info {
  font-weight: bold;
}

@media screen and (min-width: 992px) {

  .queue-entry-buttons {
    margin-left: auto;
    display: flex;
    gap: 4px;
  }

  .queue-entry-dropdown {
    display: none;
  }

  .queue-dropdown-toggle {
    display: none;
  }
}

@media screen and (max-width: 991px) {
  .queue-entry-buttons {
    display: none;
  }

  .queue-entry {
    border-bottom: 0;
  }

  .dropdown-buttons {
    margin: 8px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .queue-entry-dropdown {
    display: flex;
    overflow: hidden;
    flex-direction: column;
    justify-content: center;
    padding: 0 8px;
    gap: 4px;
    border-bottom: 2px solid #D9D9D9;
    transition: max-height ease 250ms;
    max-height: 0;
  }

  .queue-entry-dropdown.visible {
    max-height: 10rem;
  }

  .queue-dropdown-toggle {
    margin-left: auto;
    color: #818181;
    transition: transform 100ms ease;
  }

  .queue-dropdown-toggle.open {
    transform: rotate(90deg);
  }
}



</style>