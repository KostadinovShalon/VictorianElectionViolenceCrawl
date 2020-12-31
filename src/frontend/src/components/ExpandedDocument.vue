<template>
<v-card tile class="elevation-0 pa-2 grey lighten-5">
    <v-row class="px-5"><b>Description</b>: {{description}} <br></v-row>
    <v-row class="mt-2 px-5" align="center">
        <span><b>OCR</b>: {{ocr}} </span>
        <v-btn 
            text color="primary" 
            v-if="ocr === '' || ocr === null" 
            @click="$emit('download-ocr')" 
            :disabled="disabledOCRButton">Download OCR</v-btn>
    </v-row>
</v-card>
</template>

<script>
export default {
    name: "ExpandedDocument",
    props: {
        description: String,
        ocr: String,
        disabledOCRButton: Boolean
    }
}
</script>