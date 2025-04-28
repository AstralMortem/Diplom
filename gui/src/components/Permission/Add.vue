<template>
  <ItemAddModal title="Додати дозвіл" url="/api/v1/permissions/" schema="PermissionCreate" :button="{label:'Додати дозвіл'}" resource="permissions" @added="added">
    <template #form="{formState}">
      <UFormField label="Ресурс">
        <UInput v-model="formState.resource" class="w-full"/>
      </UFormField>
      <UFormField label="Дія">
        <UInputMenu v-model="formState.action" class="w-full" :items="actions" create-item @create="onCreate"/>
      </UFormField>
    </template>
  </ItemAddModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';

const actions = ref(['create', 'update', 'retrieve', 'delete'])

const onCreate = (item:string) => {
  actions.value.push(item)
}

const emit = defineEmits(['added'])
const added = (row: components["schemas"]["PermissionRead"]) => {
  emit('added', row)
}
</script>

<style>

</style>