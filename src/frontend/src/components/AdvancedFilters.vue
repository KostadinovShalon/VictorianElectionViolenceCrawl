<template>
<v-container fluid>
    <v-row align="baseline">
        <v-col sm="9" md="10" lg="11">
            <advanced-filter
            v-for="(advancedSearch, index) in advancedSearches"
            :key="index"
            :canBeRemoved="canBeRemoved(index)"
            ref="filters"
            :index="index"
            :onDelete="deleteAdvancedSearch"
            :advancedSearchOriginal="advancedSearch"
            :onSetSearch="setSearch"></advanced-filter>
        </v-col>
        <v-col sm="1" md="1" lg="1">
            <v-btn icon class="primary" dark text elevation="5" @click="addAdvancedSearch"
            >
                <v-icon>mdi-plus</v-icon>
            </v-btn>
        </v-col>
    </v-row>
</v-container>
</template>

<script>
import AdvancedFilter from '../components/AdvancedFilter.vue';
export default {
    name: 'AdvancedFilters',
    components: {
        AdvancedFilter,
    },
    data() {      
        return {
            advancedSearches: [
                {
                    searchAllWords: null,
                    searchSomeWords: null,
                    useExactPhrase: null,
                    publicationPlace: null,
                    excludeWords: null,
                    exactSearch: false,
                    newspaperTitle: null,
                    articleType: null,//Check this one (is a dropdown)
                    fromDate: null,
                    toDate: null,
                    fromDateAddedToSystem: null,
                    toDateAddedToSystem: null,
                    tags: null,
                    sortResultsBy: null,//Check this one (is a dropdown)
                    frontPageArticlesOnly: false
                }
            ],
            valids: [true]
        };
    },
    methods: {
        validate(){
            this.$refs.filters.forEach((f, idx) => {
                f.validate()
                this.valids[idx] = f.valid
            })
        },
        addAdvancedSearch() {
            this.advancedSearches.push({
                    searchAllWords: null,
                    searchSomeWords: null,
                    useExactPhrase: null,
                    publicationPlace: null,
                    excludeWords: null,
                    exactSearch: false,
                    newspaperTitle: null,
                    articleType: null,//Check this one (is a dropdown)
                    fromDate: null,
                    toDate: null,
                    fromDateAddedToSystem: null,
                    toDateAddedToSystem: null,
                    tags: null,
                    sortResultsBy: null,//Check this one (is a dropdown)
                    frontPageArticlesOnly: false
                });
            this.valids.push(true)
        },
        deleteAdvancedSearch(index) {
            //console.log(index);
            this.advancedSearches.splice(index, 1);
            this.valids.splice(index, 1)
            //console.log(this.advancedSearches);
        },
        canBeRemoved(index) {
            return index !== 0;
        },
        setSearch(index, advancedSearch) {
            this.advancedSearches[index] = advancedSearch;
            this.$emit('updateAdvancedSearches', this.advancedSearches)
        }
    }
};
</script>