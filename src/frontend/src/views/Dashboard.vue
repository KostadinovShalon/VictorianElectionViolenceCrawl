<template>
 <v-container class="align-center px-15 pb-10">
     <v-row>
         <v-col lg="9">
            <div class="text-h4 mt-10">Statistics</div>
            <v-row class="mt-5">
                <v-col sm="4" md="4" lg="4">
                    <dashboard-statistic
                        name="Total Searches"
                        v-bind:value="dashboard.searches_count">
                    </dashboard-statistic>
                </v-col>

                <v-col sm="4" md="4" lg="4">
                    <dashboard-statistic
                        name="Total Candidates"
                        v-bind:value="dashboard.candidates_count">
                    </dashboard-statistic>
                </v-col>

                <v-col sm="4" md="4" lg="4">
                    <dashboard-statistic
                        name="Total Portal Documents"
                        v-bind:value="dashboard.portal_count">
                    </dashboard-statistic>
                </v-col>
            </v-row>
            <div class="text-h4 mt-10">Last Searches</div>
            <v-data-table
                :headers="headers.last_searches"
                :items="dashboard.last_searches"
                :item-key="dashboard.last_searches.id"
                :loading="loading_last_searches"
                hide-default-footer
                class="elevation-3 pa-5 align-center mt-5">
            </v-data-table>
            <div class="text-h4 mt-10">Last Candidate Documents</div>
            <v-data-table
                :headers="headers.last_candidates"
                :items="dashboard.last_candidates"
                :item-key="dashboard.last_candidates.id"
                :loading="loading_last_candidates"
                hide-default-footer
                class="elevation-3 pa-5 align-center mt-5">
            </v-data-table>
            <div class="text-h4 mt-10">Last Portal Documents</div>
            <v-data-table
                :headers="headers.last_portal"
                :items="dashboard.last_portal"
                :item-key="dashboard.last_portal.id"
                :loading="loading_last_portal"
                hide-default-footer
                class="elevation-3 pa-5 align-center mt-5">
            </v-data-table>
         </v-col>
         <v-col lg="3">
             <system-variables-card></system-variables-card>
         </v-col>
     </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import DashboardStatistic from '../components/DashboardStatistic.vue';
import SystemVariablesCard from '../components/SystemVariablesCard.vue';
export default {
    components: {
        DashboardStatistic,
        SystemVariablesCard
    },
    name: 'Dashboard',
    data() {
        return{
            title: "Dashboard",
            loading_last_searches: false,
            loading_last_candidates: false,
            loading_last_portal: false,
            dashboard: {
                searches_count: 0,
                candidates_count: 0,
                portal_count: 0,
                last_searches: [],
                last_candidates: [],
                last_portal: []
            },
            headers:{ 
                last_searches: [
                        { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px"},
                        { text: 'Keyword', value: 'keyword', fixed: true, width: "256px"},
                        { text: 'From Date', value: 'start_date', width: "120px"},
                        { text: 'To Date', value: 'end_date', width: "120px"},
                        { text: 'Archive', value: 'archive'},
                        { text: 'Advanced Terms', value: 'advancedTerms', sortable: false},
                        { text: 'Time', value: 'timestamp'},
                    ],
                last_candidates: [
                    { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px"},
                    { text: 'Title', value: 'title'},
                    { text: 'Newspaper', value: 'publication_title'},
                    { text: 'Publication Location', value: 'publication_location'},
                    { text: 'Publication Date', value: 'publication_date'},
                    { text: 'Status', value: 'status', sortable: false},
                ],
                last_portal: [
                    { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px"},
                    { text: 'Title', value: 'title'},
                    { text: 'Newspaper', value: 'publication_title'},
                    { text: 'Publication Location', value: 'publication_location'},
                    { text: 'Publication Date', value: 'publication_date'},
                    { text: 'Type', value: 'type'},
                    { text: 'Word Count', value: 'word_count'},
                ]
            },
        };
    },
    computed: {
        commonurl(){
            return this.$store.state.commonurl
        }
    },
    methods: {
        getDataFromApi() {
            this.loading_last_searches = true
            this.loading_last_candidates = true
            this.loading_last_portal = true
            axios.get(this.commonurl + "dashboard").then(response =>{
                if(response.status == 200){
                    this.dashboard = response.data
                }
            })
            .catch(() => {})
            .then(() =>{
                this.loading_last_searches = false
                this.loading_last_candidates = false
                this.loading_last_portal = false
            })
        }
    },
    mounted(){
        this.getDataFromApi()
    }
}
</script>