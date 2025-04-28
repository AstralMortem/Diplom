<template>
    <ItemUpdateModal :title="'Оновити пацієнта ' + name" url="/api/v1/patients/{patient_id}" resource="patients" :path="{patient_id: $props.patient.patient_id}" :item="$props.patient" schema="PatientUpdate" @updated="updated">
      <template #form="{formState}">
        <div class="flex items-center gap-2">
          <UFormField name="last_name" label="Прізвище">
              <UInput v-model="formState.last_name" placeholder="Last Name"/>
          </UFormField>
          <UFormField name="first_name" label="Ім'я">
              <UInput v-model="formState.first_name" placeholder="First Name"/>
          </UFormField>
          <UFormField name="middle_name" label="По Батькові">
              <UInput v-model="formState.middle_name" placeholder="Middle Name"/>
          </UFormField>
      </div>
      <div class="flex items-center gap-2">
          <UFormField name="phone_number" label="Телефон">
              <UInput v-model="formState.phone_number" placeholder="Phone Number"/>
          </UFormField>
          <UFormField name="email" label="Email">
              <UInput v-model="formState.email" placeholder="Email"/>
          </UFormField>
      </div>
      <div class="flex items-center gap-2">
          <UFormField name="gender" label="Стать">
              <UIGenderPicker v-model="formState.gender" />
          </UFormField>
          <UFormField name="birth_data" label="Дата народження">
              <UIDatePicker v-model="formState.birth_data" />
          </UFormField>
      </div>

      <UFormField name="address" label="Адреса">
          <UTextarea v-model="formState.address" placeholder="Address" class="w-full"/>
      </UFormField>

      </template>
    </ItemUpdateModal>
  </template>
  
  <script lang="ts" setup>
  import type { components } from '#open-fetch-schemas/backend';
  const emit = defineEmits(['updated'])
  
  const updated = (row: components["schemas"]["DepartmentDetailRead"]) => {
    emit('updated', row)
  }
  
  const props = defineProps({
    patient: {
      type: {} as PropType<components["schemas"]["PatientRead"]>,
      required: true
    }
  })
  
  const name = computed(()=> `${props.patient.last_name} ${props.patient.first_name} ${props.patient.middle_name}`)
  
  </script>
  
  <style>
  
  </style>