<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
const doctorStore = useDoctorStore()


const formState = ref<components["schemas"]["DoctorCreate"]>({
    password: Math.random().toString(36).slice(-8),
})

const createDoctor = async (e: any) => {
    const response = await doctorStore.createDoctor(e.data)
    if(response){
        clean()
        navigateTo('/doctors/' + response.doctor_id)
    }
}

const clean = () => {
    show.value = false
    formState.value = {
        password: Math.random().toString(36).slice(-8)
    } as components["schemas"]["DoctorCreate"]
}

const show = ref(false)
const form = useTemplateRef<HTMLFormElement>('form')




</script>


<template>

    <UModal v-model:open="show" title="Додати пацієнта">
        <UButton label="Add Doctor" color="primary" icon="i-heroicons-plus-20-solid"/>
        <template #body>
            <UForm :state="formState" @submit.prevent="createDoctor" class="space-y-4" ref="form">
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
                        <FormGender v-model="formState.gender" />
                    </UFormField>
                    <UFormField name="birth_data" label="Дата народження">
                        <DatePicker v-model="formState.birth_data" />
                    </UFormField>
                </div>
                <div class="flex items-center gap-2">
                    <UFormField name="specialization" label="Спеціалізація">
                        <UInput v-model="formState.specialization" placeholder="Specialization"/>
                    </UFormField>
                    <UFormField name="department_id" label="Відділ">
                        <FormDepartments v-model="formState.department_id"/>
                    </UFormField>
                    <UFormField name="role_id" label="Роль">
                        <FormRoles v-model="formState.role_id" />
                    </UFormField>
                </div>

            </UForm>
        </template>
        <template #footer>
            <div class="flex items-center gap-2">
                <UButton label="Save" color="primary" @click="form?.submit()"/>
                <UButton label="Cancel" color="neutral" variant="outline" @click="clean"/>
            </div>
        </template>
    </UModal>
</template>