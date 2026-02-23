<script setup lang="ts">

const props = defineProps(['user_id', 'username', 'pn', 'preferred_name',
                            'last_name', 'course_role'])

</script>

<template>
          <tr>
            <td contenteditable="true" @input="() => { console.log(username) }">{{ username }}</td>
            <td>{{ pn }}</td>
            <td>{{ preferred_name }}</td>
            <td>{{ last_name }}</td>
            <td>{{ course_role }}</td>
            <td>{{ user_id }}</td>
            <td>
              <div id="actions">
                <button @click="$emit('remove', )"
                        :disabled="course_role === 'admin'">Remove</button>
              </div>
            </td>
          </tr>
</template>

<style scoped>
  #actions {
    display: flex;
    gap: 4px;
    justify-content: center;
  }

  tr, th, td {
    border: 2px solid #D9D9D9;
    border-collapse: collapse;
  }

  td {
    padding: 8px;
  }

  tr:nth-child(odd) {
    background-color: #FAFAFA;
  }


</style>