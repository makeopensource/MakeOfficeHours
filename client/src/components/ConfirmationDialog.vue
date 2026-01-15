<script setup lang="ts">
import {ref} from "vue";

const dialog = ref<HTMLDialogElement>()
let showing = ref(false)

const emit = defineEmits(["open", "close"])


const show = () => {
  showing.value = true
  dialog.value?.showModal()
  emit("open")
}

const hide = () => {
  dialog.value?.close()
  showing.value = false
  emit("close")
}

defineExpose({show: show, hide: hide})


</script>

<template>

  <dialog @close="hide" v-show="showing" ref="dialog">
    <slot></slot>
  </dialog>

</template>

<style scoped>

dialog {
  margin: auto;
  padding: 64px;
  border: 2px solid #B9B9B9;
  border-radius: 10px;
  flex-direction: column;
  gap: 8px;
  display: flex;
}

</style>