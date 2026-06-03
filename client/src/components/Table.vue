<script setup lang="ts">

import TableEntry from "@/components/TableEntry.vue";
import {ref} from "vue";

const props = defineProps(["headings", "table_data"]);



</script>

<template>
  <div id="enrollment-container">
        <table id="enrollment-table">
          <thead>
            <tr>
              <th v-for="heading in headings">{{ heading }}</th>
            </tr>
          </thead>
          <tbody>
            <slot></slot>
          </tbody>
        </table>
      </div>
</template>

<style scoped>

th {
  padding: 8px;
}

#enrollment-container {
  justify-content: center;
}

#enrollment-table, tr, th, td {
  border: 2px solid #D9D9D9;
  border-collapse: collapse;
}

#enrollment-table {
  min-width: 75%;
  margin: auto;
  font-size: 1rem;
}

#actions {
    display: flex;
    gap: 4px;
    margin: 4px;
    justify-content: center;
}


</style>