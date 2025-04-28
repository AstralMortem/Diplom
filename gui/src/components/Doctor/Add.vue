<template>
  <ItemAddModal title="Додати лікаря" url="/api/v1/doctors/" schema="DoctorCreate" :button="{label:'Додати лікаря'}" resource="doctors" @added="added">
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
        <UFormField name="password" label="Пароль">
            <UInput v-model="formState.password" placeholder="Password"/>
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
  </ItemAddModal>
</template>

<script lang="ts" setup>
import { UIGenderPicker } from '#components';
import type { components } from '#open-fetch-schemas/backend';


const emit = defineEmits(['added'])
const added = (row: components["schemas"]["DoctorDetailRead"]) => {
  emit('added', row)
  navigateTo('/doctors/' + row.doctor_id)
}



</script>

<style>

</style>