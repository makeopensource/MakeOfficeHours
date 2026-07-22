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
    if (data["course_role"] !== "student") {
      console.log("not a student")
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


  <StudentQueue v-if="student && ready">
    <CourseDropdown id="course-dropdown" @change="changeCourse" :current="currentCourse" :courses="myCourses"/>
  </StudentQueue>
  <InstructorQueue v-else-if="!student && ready">
    <CourseDropdown id="course-dropdown" @change="changeCourse" :current="currentCourse" :courses="myCourses"/>
  </InstructorQueue>


</template>

<style scoped>

#course-dropdown {
  position: relative;
  margin-left: auto;
  margin-right: 32px;
  max-width: fit-content;
}

</style>