<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';

const props = defineProps({
    patient: {
        type: {} as PropType<components["schemas"]["PatientRead"]>,
        required: true
    }
})

const formState = ref<components["schemas"]["PatientUpdate"]>(JSON.parse(JSON.stringify(props.patient)))
const patientStore = usePatientStore()

const changedData = computed(() => {
  const changes = {};
  for (const key in formState.value) {
    if (formState.value[key] !== props.patient[key]) {
      changes[key] = formState.value[key];
    }
  }
  return changes
});

const updatePatient = async (e: any) => {
    
    if(Object.keys(changedData.value).length > 0){
        if(await patientStore.updatePatient(props.patient.patient_id, changedData.value)){
            show.value = false
            emit('updated')
        }
    }
    
}

const form = useTemplateRef<HTMLFormElement>('form')
const show = ref(false)
const emit = defineEmits(['updated'])

</script>


<template>
<UModal v-model:open="show" :title="`Редагувати пацієнта ${props.patient.first_name} ${props.patient.last_name} ${props.patient.middle_name}`">
    <UButton class="rounded-full hover:cursor-pointer" variant="outline" color="warning" icon="i-heroicons-pencil-square" />
    <template #body>
        <UForm ref="form" :state="formState" @submit.prevent="updatePatient" class="space-y-4">
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
                <UButton label="Cancel" color="neutral" variant="outline" @click="show = false"/>
            </div>
        </template>
</UModal>
</template>