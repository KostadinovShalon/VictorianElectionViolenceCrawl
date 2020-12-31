<template>
<v-container class="justifi-center align-start pa-0 ma-0">
    <div class="text-h3 ma-9">Searches</div>
    <v-data-table
        v-model="selected"
        :headers="headers"
        :items="search_results"
        :item-key="search_results.id"
        :options.sync="options"
        :server-items-length="totalSearches"
        :loading="loading"
        show-select
        class="elevation-0 align-center">
        <template v-slot:[`item.select`]="{ item }">
            <v-simple-checkbox
            v-model="item.select"
            ></v-simple-checkbox>
        </template>
    </v-data-table>
    <v-row class="mt-2 pa-3">
        <v-spacer></v-spacer>
        <v-btn
        :key="search_results.id"
        color="primary"
        @click="goToCandidates"
        >Get Candidates</v-btn>
    </v-row>
    <no-database-dialog></no-database-dialog>
</v-container>
</template>

<script>
import axios from 'axios';
import NoDatabaseDialog from '../components/NoDatabaseDialog.vue';
export default {
    name: 'SearchResults',
    components: {NoDatabaseDialog},
    data() {
        return{
            selected: [],
            totalSearches: 0,
            loading: true,
            options: {},
            headers: [
                { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px"},
                { text: 'Keyword', value: 'keyword', fixed: true, width: "256px"},
                { text: 'From Date', value: 'start_date', width: "120px"},
                { text: 'To Date', value: 'end_date', width: "120px"},
                { text: 'Archive', value: 'archive'},
                { text: 'Advanced Terms', value: 'advancedTerms', sortable: false},
                { text: 'Time', value: 'timestamp'},
                //{ text: 'State', value: 'state', sortable: false},
            ],
            search_results: []
                // {
                //     id: '1',
                //     keyword: 'Mexico',
                //     fromDate: '1900-01-01',
                //     toDate: '1900-01-05',
                //     archive: 'service a country w here the hotel inn is utterly unknown.',
                //     advancedTerms: 'pelos',
                //     time: '01:12',
                //     select: null
                // }
                // {"added_date_end":null,
                // "added_date_start":null,
                // "article_type":null,
                // "end_date":"1900-01-10",
                // "exact_phrase":null,
                // "exact_search":null,
                // "exclude_words":null,
                // "front_page":null,
                // "id":140,
                // "keyword":"UK",
                // "newspaper_title":null,
                // "publication_place":null,
                // "search_all_words":null,
                // "archive":"BNA",
                // "sort_by":null,
                // "start_date":"1900-01-01",
                // "tags":null,
                // "time":"2020-12-13 23:12:03"}
        };
    },
    methods: {
        goToCandidates() {
            const selectedIds = this.selected.map(s => s.id)
            this.$store.commit("set_selected_searches", selectedIds)
            this.$router.push('candidates')
        },
        getDataFromApi() {
            this.loading = true
            const { sortBy, sortDesc, page, itemsPerPage } = this.options
            var params = {
                page: page,
                limit: itemsPerPage
            }
            if(sortBy.length == 1){
                params["sortby"] = sortBy[0]
                if(sortDesc[0]){
                    params['desc'] = 1
                } else {
                    params['desc'] = 0
                }
            }
            
            axios.get(this.$store.state.commonurl + "search/results", {params: params}).then(response =>{
                if(response.status == 200){
                    console.log(response.data)
                    var sr = response.data.results
                    var i = 0
                    for(i = 0; i<sr.length; i++){
                        sr[i]["advancedTerms"] = ""
                    }
                    this.search_results = sr
                    this.totalSearches = response.data.total
                }
            })
            .catch(() => {})
            .then(this.loading = false)

        }
    },
    watch: {
      options: {
        handler () {
          this.getDataFromApi()
        },
        deep: true,
      },
    },
};
</script>