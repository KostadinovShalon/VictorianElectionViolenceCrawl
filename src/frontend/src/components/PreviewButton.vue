<template>
    <v-btn
    color="yellow"
    @click="$emit('reload')"
    v-if="uri === '' || uri === null"
    :disabled="!bna_configured">
        <v-icon>mdi-refresh</v-icon>
    </v-btn>
    <v-btn
    color="primary"
    v-model="url"
    :href="link"
    target="_blank"
    v-else>
        <v-icon>mdi-link</v-icon>
    </v-btn>
</template>

<script>
import axios from 'axios'
export default {
    name: "PreviewButton",
    data(){
        return {
            bna_configured: false
        }
    },
    computed: {
        commonurl(){
            return this.$store.state.commonurl
        },
    },
    methods:{
        getBNAConfiguration(){
            axios.get(this.commonurl + "setup/bna")
            .then((response) => {
                var details = response.data
                this.bna_configured = details.password !== null && details.username !== null
            })
        }
    },
    props: {
        uri: String,
        link: String
    }, 
    mounted(){
       this.getBNAConfiguration()
    }
}
</script>