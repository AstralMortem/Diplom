<script setup lang="ts">
const isSideBarOpen = ref(false);

</script>


<template>

    <div class="h-screen w-screen flex">
        <NavSideBar v-model="isSideBarOpen"/>
        <div class="flex-1 flex flex-col">
            <div class="w-full h-max py-2 px-3">
                <NavTopBar v-model:sideBar="isSideBarOpen"/>
            </div>
            <div class="w-full h-full flex-1 py-2 px-3">
                <slot />
            </div>
        </div>
    </div>
</template>