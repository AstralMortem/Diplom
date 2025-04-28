<template>
  <ItemAddModal title="Додати медичний запис" url="/api/v1/med-records/" schema="MedRecordCreate" resource="medical_records" :button="{label:'Додати мед запис'}" @added="added">
    <template #form="{formState}">
      <UFormField label="Пацієнт" name="patient_id">
          <PatientPicker v-model="formState.patient_id" class="w-full"/>
      </UFormField>
      <UFormField label="Лікар" name="doctor_id">
        <DoctorPicker v-model="formState.doctor_id" class="w-full"/>
      </UFormField>
      <UFormField label="Відділення" name="department_id">
          <DepartmentPicker v-model="formState.department_id" class="w-full"/>
      </UFormField>
      <UFormField label="Дата прийому" name="examination_date">
          <UIDateTimePicker v-model="formState.examination_date" class="w-full"/>          
      </UFormField>
    </template>
  </ItemAddModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';


const emit = defineEmits(['added'])
const added = (row: components["schemas"]["MedRecordDetailRead"]) => {
  emit('added', row)
  navigateTo('/records/' + row.record_id)
}



</script>

<style>

</style>