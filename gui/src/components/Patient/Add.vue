<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
const patientStore = usePatientStore()


const formState = ref<components["schemas"]["PatientCreate"]>({})

const createPatient = async (e: any) => {
    const response = await patientStore.createPatient(e.data)
    if(response){
        clean()
        navigateTo('/patients/' + response.patient_id)
    }
    
}

const clean = () => {
    show.value = false
    formState.value = {} as components["schemas"]["PatientCreate"]
}

const show = ref(false)
const form = useTemplateRef<HTMLFormElement>('form')




</script>


<template>

    <UModal v-model:open="show" title="Додати пацієнта">
        <UButton label="Add Patient" color="primary" icon="i-heroicons-plus-20-solid"/>
        <template #body>
            <UForm :state="formState" @submit.prevent="createPatient" class="space-y-4" ref="form">
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
                        <FormGender v-model="formState.gender" />
                    </UFormField>
                    <UFormField name="birth_data" label="Дата народження">
                        <DatePicker v-model="formState.birth_data" />
                    </UFormField>
                </div>

                <UFormField name="address" label="Адреса">
                    <UTextarea v-model="formState.address" placeholder="Address" class="w-full"/>
                </UFormField>
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