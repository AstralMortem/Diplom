<template>
  <UCard>
    <UForm :state="formState" class="space-y-4" @submit.prevent="login">
      <UFormField label="Email / Телефон">
        <UInput v-model="formState.username"/>
      </UFormField>
      <UFormField label="Пароль">
        <UInput v-model="formState.password" type="password"/>
      </UFormField>
      <UButton label="Увійти" type="submit"/>
    </UForm>
  </UCard>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';

definePageMeta({
  layout: 'auth'
})

const authStore = useAuthStore()

const formState = ref<components["schemas"]["Body_AuthController_login_api_v1_auth_login_post"]>({})
const login = async () => {
  await authStore.login(formState.value.username, formState.value.password)
  if(authStore.isAuthenticated){
    navigateTo('/')
  }
}

</script>

<style>

</style>