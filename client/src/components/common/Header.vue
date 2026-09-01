<script setup lang="ts">

import CourseDropdown from "@/components/common/CourseDropdown.vue";
import {ref, watch} from "vue";
import {useRoute} from "vue-router";

const route = useRoute();

const course = ref(route.params.course)
const myCourses = ref([]);
const currentCourse = ref();

const showCourse = ref<boolean>(false)

function fetchCourse() {
  fetch(`/api/course/${course.value}`).then(res => {
  if (res.ok) {
      return res.json();
  }
  }).then(json => {
    currentCourse.value = json
  })
}


function setupHeader() {
  course.value = route.params.course
  if (course.value !== undefined) {
    fetchCourse();
    showCourse.value = true;
  } else {
    showCourse.value = false;
  }

  fetch("/api/me").then(res => res.json()).then(json => myCourses.value = json["enrollments"])
}

setupHeader();

watch(() => route.fullPath, () => setupHeader())

</script>

<template>
    <header id="site-header">
      <h1>Make Office Hours</h1>
      <CourseDropdown id="dropdown" v-if="showCourse" :current="currentCourse" :courses="myCourses"></CourseDropdown>
    </header>
</template>

<style scoped>

#site-header {
  display: flex;
  padding-left: 8%;
  padding-right: 8%;
}

@media screen and (max-width: 991px) {
  #site-header {
    flex-direction: column;
    padding: 8px;
  }

  #dropdown {
    margin: auto;
  }


}

</style>