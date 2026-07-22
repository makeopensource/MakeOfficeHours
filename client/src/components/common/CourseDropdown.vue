<script setup lang="ts">

import {nextTick, ref, watch} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();
const emit = defineEmits(["change"])
const props = defineProps(["current", "courses"])
const coursesDropdownShowing = ref<boolean>(false);

const currentString = ref<string>()

watch(() => props.current, (val) => {
  if (val !== undefined) {
    currentString.value = `${props.current["course_name"]} (${props.current["course_sem"]})`
  }
})

function switchCourse(to: any) {
  window.location.href = `/${to["course_url"]}/queue`
  // emit("change", to)
  // props.current.value = to
  // currentString.value = `${to["course_name"]} (${to["course_sem"]}})`
}

</script>

<template>
<div id="dropdown" v-if="current !== undefined && courses.length > 1">
      <div class="dropdown-inside" @click="coursesDropdownShowing = !coursesDropdownShowing">
        {{ currentString }}
        <div :class="coursesDropdownShowing ? 'on' : ''" class="dropdown-arrow">&#9658;</div>
      </div>
      <div class="dropdown-content" v-if="coursesDropdownShowing">
        <div class="dropdown-link" v-for="course in courses" @click="() => switchCourse(course)">{{ course["course_name"] }} ({{ course["course_sem"] }})</div>
      </div>
</div>
</template>

<style scoped>

#dropdown {
  max-width: fit-content;
  margin-left: auto;
}

.dropdown-arrow {
  margin-left: auto;
  color: #818181;
  transition: transform 100ms ease;
}

.on {
  transform: rotate(90deg)
}

.dropdown-inside {
  cursor: pointer;
  outline: 2px solid #D9D9D9;
  display: flex;
  margin-left: auto;
  padding: 16px;
  align-items: center;
  gap: 8px;
}

.dropdown-content {
  position: absolute;
  margin-top: 2px;
  padding: 4px 16px;
  outline: 2px solid #D9D9D9;
  background-color: var(--bg-color);
  box-shadow: 2px 2px 2px lightgrey;
}

.dropdown-link {
  padding: 16px 8px;
  cursor: pointer;
}

.dropdown-link:hover {
  background-color: #f5f5f5;
}


</style>