<template>
  <ItemUpdateModal :title="'Оновити відділення ' + $props.department.name" url="/api/v1/departments/{department_id}" resource="departments" :path="{department_id:department.department_id}" :item="$props.department" schema="DepartmentUpdate" @updated="updated">
    <template #form="{formState}">
      <UFormField label="Назва">
        <UInput v-model="formState.name" class="w-full"/>
      </UFormField>
      <UFormField label="Опис">
        <UTextarea v-model="formState.description" class="w-full"/>
      </UFormField>
      <UFormField label="Контактний телефон">
        <UInput v-model="formState.contact_phone" class="w-full"/>
      </UFormField>
    </template>
  </ItemUpdateModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
const emit = defineEmits(['updated'])

const updated = (row: components["schemas"]["DepartmentDetailRead"]) => {
  emit('updated', row)
}

defineProps({
  department: {
    type: {} as PropType<components["schemas"]["DepartmentRead"]>,
    required: true
  }
})


</script>

<style>

</style>