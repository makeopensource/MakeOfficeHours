<script setup lang="ts">
import StudentQueue from "@/pages/StudentQueue.vue";
import {ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import InstructorQueue from "@/pages/InstructorQueue.vue";

const router = useRouter()
const route = useRoute()

let student = ref(true);
let ready = ref(false)


const course: string | undefined = route.params.course?.toString()

if (course != null) {
  localStorage.setItem("last-course", course)
}

fetch(`/api/course/${course}`).then(res => {
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