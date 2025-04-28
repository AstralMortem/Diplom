<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend';

const props = defineProps({
    transcription:{
        type: {} as PropType<components["schemas"]["TranscriptionRead"]>,
        required: true
    }
})
</script>

<template>
    <ItemDeleteModal title="Видалити транскрипцію" resource="transcriptions" url="/api/v1/med-records/{record_id}/transcriptions/{transcription_id}" :path="{record_id:$props.transcription.record_id, transcription_id: $props.transcription.transcription_id}" @deleted="navigateTo('/records/' + $props.transcription.record_id)">
        <template #body>
            <p>Ви впевнені що хочете видалити транскрипцію за <span class="text-error-500">{{ $props.transcription.created_at }} </span></p>
        </template>
    </ItemDeleteModal>
</template>