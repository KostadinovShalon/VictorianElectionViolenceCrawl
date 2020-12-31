<template>
    <v-card class="mx-auto my-12" >
        <v-card-title><div class="text-h4">System variables</div></v-card-title>
        <v-card-title>
            <v-icon left color="green" v-if="bna_configured">mdi-check-circle</v-icon>
            <v-icon left color="orange" v-else>mdi-alert</v-icon>
            BNA
            <v-spacer></v-spacer>
            <v-btn icon href="/bna-user"><v-icon>mdi-cog</v-icon></v-btn>
        </v-card-title>
        <v-card-text v-if="!bna_configured">BNA user login details have not been configured. Crawling can be performed without OCR and files cannot be downloaded.</v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-title>
                <v-icon left color="green" v-if="db_configured">mdi-check-circle</v-icon>
            <v-icon left color="red" v-else>mdi-alert</v-icon>
            Database 
            <v-chip class="ms-2" color="blue" dark v-if="db_configured && local">Local</v-chip> 
            <v-chip class="ms-2" color="yellow" v-if="db_configured && !local">Remote</v-chip>
            <v-spacer></v-spacer>
            <v-btn icon href="/database-conn"><v-icon>mdi-cog</v-icon></v-btn>
        </v-card-title>
        <v-card-text v-if="!db_configured">Database is not configured (neither remote or local). No actions are allowed until database configuration.</v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-title>
            <v-icon left color="green" v-if="storage_configured">mdi-check-circle</v-icon>
            <v-icon left color="orange" v-else>mdi-alert</v-icon>
            Storage
            <v-spacer></v-spacer>
            <v-btn icon href="/server-variables"><v-icon>mdi-cog</v-icon></v-btn>
        </v-card-title>
        <v-card-text v-if="!storage_configured">Storage is not configured. Files will not be downloaded (previews can be generated if BNA account details are given)</v-card-text>
    </v-card>
</template>

<script>
import axios from 'axios';
export default {
    name: "SystemVariablesCard",
    data(){
        return {
            bna_configured: false,
            db_configured: false,
            storage_configured: false,
            local: false
        }
    },
    computed: {
        commonurl(){
            return this.$store.state.commonurl
        }
    },
    methods: {
        getBNAConfiguration(){
            axios.get(this.commonurl + "setup/bna")
            .then((response) => {
                var details = response.data
                this.bna_configured = details.password !== null && details.username !== null
            })
        },
        getDBConfiguration(){
            axios.get(this.commonurl + "setup/db")
            .then((response) => {
                var details = response.data
                this.local = details.local
                if(this.local){
                    this.db_configured = details.data_dir !== null
                } else {
                    this.db_configured = details.password !== null && details.user !== null && details.host !== null
                }
            })
        },
        getServerConfiguration(){
            axios.get(this.commonurl + "setup/server")
            .then((response) => {
                var details = response.data
                this.local = details.local
                if(this.local){
                    this.storage_configured = details.files_dir !== null
                } else {
                    this.storage_configured = details.password !== null && details.user !== null && details.host !== null
                }
            })
        }
    },
    mounted(){
        this.getBNAConfiguration()
        this.getDBConfiguration()
        this.getServerConfiguration()
    }
}
</script>

<style>

</style>