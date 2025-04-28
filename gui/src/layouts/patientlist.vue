<template>
  <div class="h-screen w-screen flex">
        <NavSideBar v-model="isSideBarOpen"/>
        <div class="flex-1 flex flex-col">
            <div class="w-full h-max py-2 px-3">
                <NavTopBar v-model:side-bar="isSideBarOpen"/>
            </div>
            <div class="w-full h-full flex-1 flex flex-row py-2 px-3">
                <div class="w-full h-full pr-2">
                    <slot/>
                </div>
                <ItemList title="Пацієнти" url="/api/v1/patients/">
                    <template #item="{item}">
                        <PatientListItem :item="item"/>
                    </template>
                </ItemList>
            </div>
        </div> 
    </div>
</template>

<script lang="ts" setup>
const isSideBarOpen = ref<boolean>(true)
</script>

<style>

</style>