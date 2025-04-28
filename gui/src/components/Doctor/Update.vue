<template>
    <ItemUpdateModal :title="'Оновити лікаря ' + name" url="/api/v1/doctors/{doctor_id}" :path="{doctor_id: $props.doctor.doctor_id}" resource="doctors" :item="$props.doctor" schema="DoctorUpdate" @updated="updated">
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
      <div class="flex items-center gap-2">
        <UFormField name="specialization" label="Спеціалізація">
            <UInput v-model="formState.specialization" placeholder="Specialization"/>
        </UFormField>
        <UFormField name="department_id" label="Відділ">
            <DepartmentPicker v-model="formState.department_id"/>
        </UFormField>
        <UFormField name="role_id" label="Роль">
            <RolePicker v-model="formState.role_id" />
        </UFormField>
      </div>
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
    doctor: {
      type: {} as PropType<components["schemas"]["DoctorRead"]>,
      required: true
    }
  })
  
  const name = computed(()=> `${props.doctor.last_name} ${props.doctor.first_name} ${props.doctor.middle_name}`)
  
  </script>
  
  <style>
  
  </style>