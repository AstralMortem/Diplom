<template>
  <ItemAddModal title="Додати відділення" url="/api/v1/departments/" schema="PermissionCreate" :button="{label:'Додати відділення'}" resource="departments" @added="added">
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
  </ItemAddModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';


const emit = defineEmits(['added'])
const added = (row: components["schemas"]["DepartmentRead"]) => {
  emit('added', row)
}
</script>

<style>

</style>