<template>
  <ItemUpdateModal :title="'Оновити  запис за' + data" resource="medical_records" url="/api/v1/med-records/{record_id}" :path="{record_id: $props.record.record_id}" :item="$props.record" schema="MedRecordUpdate" @updated="updated">
    <template #form="{formState}">
      <UFormField label="Пацієнт" name="patient_id">
          <PatientPicker v-model="formState.patient_id" class="w-full"/>
      </UFormField>
      <UFormField label="Відділення" name="department_id">
          <DepartmentPicker v-model="formState.department_id" class="w-full"/>
      </UFormField>
      <UFormField label="Дата прийому" name="examination_date">
          <UIDateTimePicker v-model="formState.examination_date" class="w-full"/>
      </UFormField>
    </template>
  </ItemUpdateModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
const emit = defineEmits(['updated'])

const updated = (row: components["schemas"]["MedRecordDetailRead"]) => {
  emit('updated', row)
}

const props = defineProps({
  record: {
    type: {} as PropType<components["schemas"]["MedRecordRead"]>,
    required: true
  }
})

const data = computed(()=> new Date(props.record.examination_date).toLocaleString('uk-UA', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }))

</script>

<style>

</style>