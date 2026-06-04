<script setup lang="ts">

defineProps(["headings"]);

</script>

<template>
  <div class="tbl-container">
        <table class="tbl-table">
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

.tbl-container {
  justify-content: center;
}

.tbl-table, tr, th, td {
  border: 2px solid #D9D9D9;
  border-collapse: collapse;
}

.tbl-table {
  min-width: 85%;
  margin: auto;
  font-size: 1rem;
}

</style>