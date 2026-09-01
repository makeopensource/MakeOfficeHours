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
}

</script>

<template>
<div id="dropdown">
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
  height: 100%;
}

.dropdown-arrow {
  margin-left: auto;
  color: white;
  transition: transform 100ms ease;
}

.on {
  transform: rotate(90deg)
}

.dropdown-inside {
  cursor: pointer;
  display: flex;
  margin-left: auto;
  align-items: center;
  gap: 8px;
  height: 100%;
}

.dropdown-content {
  position: absolute;
  right: 0;
  margin-right: 8%;
  margin-top: 2px;
  padding: 4px 16px;
  color: black;
  text-align: left;
  background-color: var(--bg-color);
  box-shadow: 2px 2px 8px lightgrey;
}

@media screen and (max-width: 991px) {
  .dropdown-content {
    margin: auto;
    right: auto;
    padding: 4px;
  }

}

.dropdown-link {
  padding: 16px 8px;
  cursor: pointer;
}

.dropdown-link:hover {
  background-color: #f5f5f5;
}


</style>