<template>
  <UModal v-model:open="open" :title="title">
    <slot v-if="authStore.hasAccess('create', $props.resource)" name="open">
      <UButton v-bind="{...defaultButton, ...props.button}"/>
    </slot>

    <template #body>
      <slot name="body">
        <UForm ref="formRef" class="space-y-4" :state="formState" @submit.prevent="submitForm">
          <slot name="form" :form-state="formState"/>
        </UForm>
      </slot>
    </template>

    <template #footer>
      <slot name="footer">
        <div class="flex flex-row justify-start items-center gap-2">
          <UButton  label="Зберегти" class="cursor-pointer" @click="formRef?.submit()"/>
          <UButton variant="subtle"  class="cursor-pointer" color="warning" label="Закрити" @click="cleanForm"/>
        </div>
      </slot>
    </template>
  </UModal>

</template>

<script lang="ts" setup generic="P extends Extract<keyof paths, string>, S extends keyof components['schemas']">
import type { components, paths } from '#open-fetch-schemas/backend';
import type { ButtonProps } from '@nuxt/ui';
import type { PropType } from 'vue';

const defaultButton = {
  label: 'Add Item',
  leadingIcon: 'i-heroicons-plus',
  class: 'cursor-pointer'
} as ButtonProps

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  button: {
    type: {} as PropType<ButtonProps>,
    default: {}
  },
  url: {
    type: String as unknown as PropType<P>,
    required: true
  },
  schema: {
    type: String as unknown as PropType<S>,
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

const emit = defineEmits(['added', 'closed'])

const formState = ref<components["schemas"][S]>({})
const open = defineModel<boolean>('open', {default: false})
watch(open, (newVal) =>{
  if(!newVal){
    emit('closed')
  }
})

const authStore = useAuthStore()

const cleanForm = () => {
  formState.value = {} as components["schemas"][S]
  open.value = false
}

const formRef = useTemplateRef<HTMLFormElement>('formRef')

const {$backend} = useNuxtApp()

const submitForm = async () => {
  try{
    const response = await $backend(props.url as P, {
      method: 'POST',
      path: props.path,
      query: props.query,
      body: formState.value,
      cache: 'no-cache',
    })
    emit('added', response)
    cleanForm()
  }catch(error){
    backendError(error)
  }
}

</script>

<style>

</style>