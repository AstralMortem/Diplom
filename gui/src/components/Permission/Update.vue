<template>
  <ItemUpdateModal :title="'Оновити дозвіл ' + name" url="/api/v1/permissions/{permission_id}" resource="permissions" :path="{role_id:permission.permission_id}" :item="$props.permission" schema="PermissionUpdate" @updated="updated">
    <template #form="{formState}">
      <UFormField label="Ресурс">
        <UInput v-model="formState.resource" class="w-full"/>
      </UFormField>
      <UFormField label="Дія">
        <UInputMenu v-model="formState.action" class="w-full" :items="actions" create-item @create="onCreate"/>
      </UFormField>
    </template>
  </ItemUpdateModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
const emit = defineEmits(['updated'])

const actions = ref(['create', 'update', 'retrieve', 'delete'])

const onCreate = (item:string) => {
  actions.value.push(item)
}
const updated = (row: components["schemas"]["PermissionRead"]) => {
  emit('updated', row)
}

const props = defineProps({
  permission: {
    type: {} as PropType<components["schemas"]["PermissionRead"]>,
    required: true
  }
})

const name = computed(()=> `${props.permission.resource}:${props.permission.action}`)

</script>

<style>

</style>