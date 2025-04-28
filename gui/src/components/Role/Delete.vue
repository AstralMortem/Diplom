<template>
  <ItemDeleteModal url="/api/v1/roles/{role_id}" :path="{role_id:$props.role.role_id}" :title="'Видалити роль ' + $props.role.name" resource="roles" @deleted="$emit('deleted')">
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити роль <span class="text-error-500">{{ $props.role.name }}</span>?</p>
      <p class="font-semibold">Це може превезти до неможливості авторизації для деяких користувачів.</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

defineProps({
  role: {
    type: {} as PropType<components["schemas"]["RoleRead"]>,
    required:true
  }
})
</script>

<style>

</style>