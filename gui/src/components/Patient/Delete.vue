<template>
  <ItemDeleteModal url="/api/v1/patients/{patient_id}" :path="{patient_id:$props.patient.patient_id}" resource="patients" :title="'Видалити пацієнта ' + name" @deleted="$emit('deleted')">
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити пацієнта <span class="text-error-500">{{ name }}</span>?</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

const props = defineProps({
  patient: {
    type: {} as PropType<components["schemas"]["PatientRead"]>,
    required:true
  }
})

const name = computed(()=> `${props.patient.last_name} ${props.patient.first_name} ${props.patient.middle_name}`)

</script>

<style>

</style>