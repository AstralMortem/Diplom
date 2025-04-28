<template>
  <UModal v-model:open="open" :title="title">
    <slot v-if="authStore.hasAccess('update', $props.resource)" name="open">
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
          <UButton variant="subtle" class="cursor-pointer" color="warning" label="Закрити" @click="cleanForm"/>
        </div>
      </slot>
    </template>
  </UModal>

</template>

<script lang="ts" setup generic="P extends keyof paths, S extends keyof components['schemas']">
import type { components, paths } from '#open-fetch-schemas/backend';
import type { ButtonProps } from '@nuxt/ui';
import type { PropType } from 'vue';

const defaultButton = {
  class: 'rounded-full cursor-pointer',
  variant: 'outline',
  color: 'warning',
  leadingIcon: 'i-heroicons-pencil-square'
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
  item: {
    type: {} as PropType<components["schemas"][S]> ,
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
const authStore = useAuthStore()
const emit = defineEmits(['updated', 'closed'])

const formState = ref<components["schemas"][S]>(JSON.parse(JSON.stringify(props.item)))
const open = defineModel<boolean>('open', {default: false})
watch(open, (newVal) =>{
  if(!newVal){
    emit('closed')
  }
})


const changedData = computed(() => {
  const changes = {};
  for (const key in formState.value) {
    if (formState.value[key] !== props.item[key]) {
      changes[key] = formState.value[key];
    }
  }
  return changes
});


const cleanForm = () => {
  formState.value = JSON.parse(JSON.stringify(props.item)) as components["schemas"][S]
  open.value = false
}

const formRef = useTemplateRef<HTMLFormElement>('formRef')

const {$backend} = useNuxtApp()

const submitForm = async () => {
  if(Object.keys(changedData.value).length > 0){
    try{
      const response = await $backend(props.url as P, {
        method: 'PATCH',
        path: props.path,
        query: props.query,
        body: changedData.value,
        
        cache: 'no-cache',
      })
      emit('updated', response)
      cleanForm()
    }catch(error){
      backendError(error)
    }
  }
  
}

</script>

<style>

</style>