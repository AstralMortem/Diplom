<script setup lang="ts">
definePageMeta({
    layout: 'auth'
})

const authStore = useAuthStore()


const state = ref({
    username: undefined,
    password: undefined,
})

const login = async (e: any) => {
    await authStore.login(e.data.username, e.data.password)
    if(authStore.isAuthenticated){
        navigateTo('/')
    }
}

</script>

<template>
    <UCard>
        <template #header>
            <div class="flex flex-col gap-2 items-center justify-center">
                <h3 class="text-lg font-semibold">Log into Account</h3>
            </div>
            
        </template>
        <UForm :state="state" @submit.prevent="login" class="space-y-4">
        <UFormField  label="Email/Phone" name="username">
            <UInput v-model="state.username" placeholder="johndoe@gmail.com"  class="w-full"/>
        </UFormField >
        <UFormField  label="Password" name="password">
            <UInput v-model="state.password" placeholder="********" type="password" class="w-full"/>
            <template #help>
                <ULink class="text-2xs hover:underline cursor-pointer hover:text-primary-500">Forgot Password?</ULink>
            </template>
        </UFormField >
        <UButton type="submit" label="Login" block/>
    </UForm>
    </UCard>
    
</template>


