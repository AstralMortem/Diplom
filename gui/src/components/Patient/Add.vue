<template>
  <ItemAddModal title="Додати пацієнта" url="/api/v1/patients/" schema="DoctorCreate" :button="{label:'Додати пацієнта'}" resource="patients" @added="added">
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
  </ItemAddModal>
</template>

<script lang="ts" setup>
import { UIGenderPicker } from '#components';
import type { components } from '#open-fetch-schemas/backend';


const emit = defineEmits(['added'])
const added = (row: components["schemas"]["PatientDetailRead"]) => {
  emit('added', row)
  navigateTo('/patients/' + row.patient_id)
}



</script>

<style>

</style>