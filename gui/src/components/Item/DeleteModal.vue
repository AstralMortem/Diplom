<template>
  <UModal v-model:open="open" :title="title">
    <slot v-if="authStore.hasAccess('delete', $props.resource)"  name="open">
      <UButton v-bind="{...defaultButton, ...props.button}"/>
    </slot>

    <template #body>
      <slot name="body">
        <p v-if="typeof props.descriptions === 'string'">{{ props.descriptions }}</p>
        <component :is="props.descriptions" v-else-if="props.descriptions === 'object'" />
      </slot>
    </template>

    <template #footer>
      <slot name="footer">
        <div class="flex flex-row justify-start items-center gap-2">
          <UButton  label="Видалити" class="cursor-pointer" color="error" @click="submitDelete"/>
          <UButton variant="subtle" class="cursor-pointer" color="warning" label="Закрити" @click="open = false"/>
        </div>
      </slot>
    </template>
  </UModal>

</template>

<script lang="ts" setup generic="P extends Extract<keyof paths, string>">
import type { paths } from '#open-fetch-schemas/backend';
import type { ButtonProps } from '@nuxt/ui';
import type { PropType } from 'vue';

const defaultButton = {
  leadingIcon: 'i-heroicons-trash',
  variant: 'outline',
  color: 'error',
  class: 'cursor-pointer rounded-full'
} as ButtonProps

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  descriptions: {
    type: String || {} as VNode,
    default: undefined
  },
  button: {
    type: {} as PropType<ButtonProps>,
    default: {}
  },
  url: {
    type: String as unknown as PropType<P>,
    required: true
  },
  query: {
    type: {} as PropType<object>,
    default: {}
  },
  path: {
    type: {} as PropType<object>,
    default: {}
  },
  resource: {
    type: String,
    default: undefined
  }
})

const emit = defineEmits(['deleted', 'closed'])

const open = defineModel<boolean>('open', {default: false})

watch(open, (newVal) =>{
  if(!newVal){
    emit('closed')
  }
})

const authStore = useAuthStore()
const {$backend} = useNuxtApp()

const submitDelete = async () => {
  try{
    const response = await $backend(props.url as P, {
      method: 'DELETE',
      path: props.path,
      query: props.query,
      
      cache: 'no-cache',
    })
    emit('deleted', response)
    open.value = false
  }catch(error){
    backendError(error)
  }
}

</script>

<style>

</style>