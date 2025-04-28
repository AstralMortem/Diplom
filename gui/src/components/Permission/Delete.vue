<template>
  <ItemDeleteModal url="/api/v1/permissions/{permission_id}" :path="{permission_id:$props.permission.permission_id}" resource="permissions" :title="'Видалити дозвіл ' + name" @deleted="$emit('deleted')">
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити дозвіл <span class="text-error-500">{{ name }}</span>?</p>
      <p class="font-semibold">Це може превезти до неможливості деяких дій в системі для деяких користувачів.</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

const props = defineProps({
  permission: {
    type: {} as PropType<components["schemas"]["PermissionRead"]>,
    required:true
  }
})

const name = computed(()=> `${props.permission.resource}:${props.permission.action}`)

</script>

<style>

</style>