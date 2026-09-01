<script setup lang="ts">
import StudentQueue from "@/pages/StudentQueue.vue";
import {nextTick, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import InstructorQueue from "@/pages/InstructorQueue.vue";
import CourseDropdown from "@/components/common/CourseDropdown.vue";

const router = useRouter()
const route = useRoute()

let student = ref(true);
let ready = ref(false)


const course: string | undefined = route.params.course?.toString()

if (course != null) {
  localStorage.setItem("last-course", course)
}

const myCourses = ref([])

function setupQueue() {
  ready.value = false
  fetch(`/api/me`).then(res => {
  if (res.ok) {
    return res.json()
  }
    router.push("/")
  }).then(json => {
    myCourses.value = json["enrollments"]
  })

  fetch(`/api/course/${course}`).then(res => {
    if (!res.ok) {
      router.push("/")
    }
    return res.json()
  }).then(data => {
    if (data["course_role"] === null) {
      router.push("/")
    }
    if (data["course_role"] !== "student") {
      student.value = false;
    }
    ready.value = true
  })

  fetchCourse()
}



const currentCourse = ref();
function fetchCourse() {
  fetch(`/api/course/${course}`).then(res => {
  if (res.ok) {
      return res.json();
  } else {
    router.push("/")
  }
  }).then(json => {
    currentCourse.value = json
  })
}

function changeCourse(to: any) {
  window.location.href = `/${to["course_url"]}/queue`
}

setupQueue();

</script>

<template>


  <StudentQueue v-if="student && ready"></StudentQueue>
  <InstructorQueue v-else-if="!student && ready"></InstructorQueue>


</template>

<style scoped>

#course-dropdown {
  position: relative;
  max-width: fit-content;
  margin-bottom: 4px;
}

@media screen and (max-width: 991px) {
  #course-dropdown {
    margin: auto auto 16px;
  }
}

</style>