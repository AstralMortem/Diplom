<script setup lang="ts">
const router = useRouter()


const isSideBarOpen = defineModel("sideBar", {default: false})
const backButton = useBackButton()

</script>


<template>
    <header class="bg-gray-800 text-white p-4 flex items-center justify-between w-full rounded-lg">
        <div class="flex justify-start items-center gap-2">
            <UButton v-if="backButton" @click="router.back()"  class="rounded-full" variant="outline" label="Назад" leading-icon="i-heroicons-arrow-left"/>
            <UButton @click="isSideBarOpen = !isSideBarOpen" class="md:hidden" label="Open"/>
            <NavSearch/>
        </div>
        <div class="flex justify-end items-center gap-2">
            <UIColorMode/>
            <UserMenu />
        </div>
    </header>
</template>
