<script setup lang="ts">
import StudentQueue from "@/pages/StudentQueue.vue";
import {ref} from "vue";
import {useRouter} from "vue-router";
import InstructorQueue from "@/pages/InstructorQueue.vue";

const router = useRouter()

let student = ref(true);
let ready = ref(false)

fetch("/api/me").then(res => {
  if (!res.ok) {
    router.push("/")
  }
  return res.json()
}).then(data => {
  if (data["course_role"] !== "student") {
    student.value = false;
  }
  ready.value = true
})

</script>

<template>

  <StudentQueue v-if="student && ready"></StudentQueue>
  <InstructorQueue v-else-if="!student && ready"></InstructorQueue>


</template>

<style scoped>

</style>