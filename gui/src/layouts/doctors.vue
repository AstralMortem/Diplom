
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
            <div class="w-full h-full flex-1 flex flex-row py-2 px-3">
                <div class="w-full h-full pr-2">
                    <slot/>
                </div>
                
                <DoctorList />
            </div>
        </div>
    </div>
</template>