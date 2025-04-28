<template>
  <ItemAddModal title="Додати роль" url="/api/v1/roles/" schema="RoleCreate" resource="roles" :button="{label:'Додати роль'}" @added="added">
    <template #form="{formState}">
      <UFormField label="Назва">
        <UInput v-model="formState.name" class="w-full"/>
      </UFormField>
    </template>
  </ItemAddModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';

const emit = defineEmits(['added'])
const added = (row: components["schemas"]["RoleRead"]) => {
  emit('added', row)
}
</script>

<style>

</style>