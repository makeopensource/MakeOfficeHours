<script setup lang="ts">
import {nextTick, ref} from "vue";

const dialog = ref<HTMLDialogElement>()
let showing = ref(false)

const emit = defineEmits(["open", "close", "enter"])

const props = defineProps({
  persistent: {
    default: false
  }
})


const show = () => {
  showing.value = true
  dialog.value?.showModal()
  emit("open")
  if (props.persistent) {
      nextTick(() => { dialog.value?.focus() })
  }
}

const hide = () => {
  dialog.value?.close()
  showing.value = false
  emit("close")
}

defineExpose({show: show, hide: hide})

function esc(e: Event) {
  if (props.persistent) {
    dialog.value?.focus()
    e.preventDefault()
  }
}


</script>

<template>

  <dialog @close="hide" v-show="showing" @keydown.esc.stop="esc" @keydown.enter="$emit('enter')" ref="dialog">
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

dialog:focus {
  outline: 0
}

@media screen and (max-width: 992px) {
    dialog {
        transform: scale(90%);
        padding: 6%;
    }
}

</style>