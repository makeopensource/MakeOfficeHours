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
  padding: 3%;
  border: 2px solid #B9B9B9;
  border-radius: 10px;
  flex-direction: column;
  gap: 8px;
  display: flex;
}

@media screen and (max-width: 992px) {
    dialog {
        transform: scale(90%);
        padding: 6%;
    }
}

</style>