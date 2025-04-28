<script setup lang="ts">
const router = useRouter()

const backButton = useBackButton()

const isSideBarOpen = defineModel<boolean>("sideBar", {default: false})

</script>


<template>
    <header class="bg-gray-300 dark:bg-gray-800 text-white p-4 flex items-center justify-between w-full rounded-lg">
        <div class="flex justify-start items-center gap-2">
            <UButton v-if="backButton" variant="outline"  class="rounded-full" leading-icon="i-heroicons-arrow-left" label="Назад" @click="router.back()"/>
            <UButton class="md:hidden" label="Open" @click="isSideBarOpen = !isSideBarOpen"/>
            <!-- <NavSearch/> -->
        </div>
        <div class="flex justify-end items-center gap-2">
            <UIColorMode/>
            <NavUserMenu />
        </div>
    </header>
</template>
