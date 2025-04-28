<template>
  <ItemDeleteModal url="/api/v1/doctors/{doctor_id}" :path="{doctor_id:$props.doctor.doctor_id}" :title="'Видалити лікаря ' + name" resource="doctors" @deleted="$emit('deleted')" >
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити лікаря <span class="text-error-500">{{ name }}</span>?</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

const props = defineProps({
  doctor: {
    type: {} as PropType<components["schemas"]["DoctorRead"]>,
    required:true
  }
})

const name = computed(()=> `${props.doctor.last_name} ${props.doctor.first_name} ${props.doctor.middle_name}`)

</script>

<style>

</style>