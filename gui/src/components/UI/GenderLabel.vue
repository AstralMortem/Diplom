<script setup lang="ts">
defineProps({
    gender: {
        type: String as PropType<'male' | 'female'>,
        required: true
    }
})
</script>


<template>
    <UILabel label="Стать">
        <div class="flex items-center gap-2">
            <UIcon :name="gender === 'male' ? 'mdi-gender-male' : 'mdi-gender-female'" :class="gender === 'male' ? 'text-blue-500' : 'text-pink-500'" />
            <span>{{ gender === 'male' ? 'Чоловік' : 'Жінка' }}</span>
        </div>
        
    </UILabel>
    
</template>

<style scoped>

</style>