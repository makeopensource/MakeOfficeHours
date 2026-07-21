<script setup lang="ts">

import {ref} from "vue";
import Alert from "@/components/common/Alert.vue";
import {useRouter} from "vue-router";

const router = useRouter()

const courses = ref([]);

const alert = ref<typeof Alert>();

fetch("/api/me")

const fetchCourses = () => fetch("/api/courses").then(res => {
  return res.json()
}).then(json => {
  courses.value = json["courses"]
})

fetchCourses()

const createCourseForm = ref<HTMLFormElement>();
const createUserForm = ref<HTMLFormElement>();
const createInstructorForm = ref<HTMLFormElement>();

const selectedURL = ref<string>();

function submitForm(form: HTMLFormElement | undefined) {
  if (form === undefined) {
    return;
  }

  const data: any = {}

  for (let i = 0; i < form.elements?.length; i++) {
    // i regret choosing you typescript
    const elem: any = form.elements[i]

    if (elem.type !== 'submit') {
      data[elem.name] = elem.value
    }
  }

  fetch(form.target, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {"Content-Type": "application/json"}
  }).then(res => {
    if (res.ok) {
      alert.value?.setMessage("Success")
      fetchCourses()
    } else {
      res.json().then(json => alert.value?.setError(json["message"]))
    }
  })
}

</script>

<template>

  <Alert ref="alert"/>

  <div id="page">
    <h1>Admin Page</h1>
    <div id="top-buttons">
      <button @click="router.push('/')">Let me out!</button>
    </div>
    <br/>

    <div id="main-cont">
      <div id="sidebar">
        <h3>Actions</h3>
        <a href="#create-class">Create a new course</a>
        <a href="#create-user">Create a user</a>
        <a href="#promote-paul">Promote instructor</a>
      </div>
        <div id="content">

<!--          CREATE COURSE FORM      -->
        <h2 id="create-class">Create a new course</h2>
        <form class="mini-form-container" ref="createCourseForm" target="/api/course">
          <div class="input-elem">
            <label for="name">Course Name</label>
            <p>(e.g. CSE 116: Computer Science II)</p>
            <input name="name" type="text">
          </div>
          <div class="input-elem">
            <label for="semester">Course Semester</label>
            <p>(e.g. f26)</p>
            <input name="semester" type="text">
          </div>
          <div class="input-elem">
            <label for="url">Course URL</label>
            <p>(e.g. cse116-f26)</p>
            <input name="url" type="text">
          </div>
          <div class="input-elem">
            <button type="submit" @click.prevent="() => submitForm(createCourseForm)">Create Course</button>
          </div>
        </form>

        <br/>

<!--          CREATE USER FORM -->
        <h2 id="create-user">Create a user</h2>
        <form class="mini-form-container" ref="createCourseForm" target="/api/user">
          <div class="input-elem">
            <label for="ubit">Username</label>
            <input name="ubit" type="text">
          </div>
          <div class="input-elem">
            <label for="pn">Person Number</label>
            <input name="pn" type="text">
          </div>
          <div class="input-elem">
            <label for="first_name">First Name</label>
            <input name="first_name" type="text">
          </div>
          <div class="input-elem">
            <label for="last_name">Last Name</label>
            <input name="last_name" type="text">
          </div>
          <div class="input-elem">
            <button type="submit" @click.prevent="() => submitForm(createCourseForm)">Create User</button>
          </div>
        </form>

        <br/>
<!--PROMOTE INSTRUCTOR FORM-->
        <h2 id="promote-paul">Promote Instructor</h2>
        <form class="mini-form-container" ref="createInstructorForm" :target="`/api/course/${selectedURL}/appoint`">
          <div class="input-elem">
            <label for="ubit">Instructor UBIT</label>
            <input name="ubit" type="text">
          </div>
          <div class="input-elem">
            <label>Course</label>
            <select v-model="selectedURL" @change="() => console.log(selectedURL)" type="submit">
              <option v-for="course in courses" :value="course['course_url']">{{ course['course_url'] }}</option>
            </select>
          </div>

          <div class="input-elem">
            <button type="submit" @click.prevent="() => submitForm(createInstructorForm)">Promote User</button>
          </div>
        </form>
      </div>
    </div>


  </div>


</template>

<style scoped>

@import "../assets/css/base.css";

label {
  font-weight: bold;
}

#main-cont {
  display: flex;
  gap: 32px;
}

#sidebar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

#content {
  flex: 1;
}

.mini-form-container {
  padding: 16px;
  outline: 1px solid #D9D9D9;
  border-radius: 16px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-elem {
  display: flex;
  gap: 8px;
  flex-direction: column;
  flex-grow: 0;
  width: fit-content;
}

#page {
  margin: 32px 128px;
}

#top-buttons {
  margin-top: 4px;
}


</style>