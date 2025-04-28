<template>
  <ItemUpdateModal :title="'Оновити роль ' + $props.role.name" url="/api/v1/roles/{role_id}" resource="roles" :path="{role_id:role.role_id}" :item="$props.role" schema="RoleUpdate" @updated="updated">
    <template #form="{formState}">
      <UFormField label="Назва" name="name">
        <UInput v-model="formState.name"/>
      </UFormField>
    </template>
  </ItemUpdateModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
const emit = defineEmits(['updated'])

const updated = (row: components["schemas"]["RoleRead"]) => {
  emit('updated', row)
}

defineProps({
  role: {
    type: {} as PropType<components["schemas"]["RoleRead"]>,
    required: true
  }
})

</script>

<style>

</style>