<template>
    <v-container fluid>
        <v-row align="baseline">
            <v-col sm="9" md="10" lg="11">
                <filter-item
                v-for="(search, index) in search_terms"
                ref="filters"
                :key="index"
                :canBeRemoved="canBeRemoved(index)"
                :index="index"
                :onDelete="deleteSearch"
                :searchOriginal="search"
                :onSetSearch="setSearch">
                </filter-item>
            </v-col>
        <v-col sm="1" md="1" lg="1">
            <v-btn icon class="primary" dark text elevation="5" @click="addSearch"
            >
                <v-icon>mdi-plus</v-icon>
            </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import FilterItem from '../components/Filter.vue';

export default {
    name: 'Filters',
    components: {
        FilterItem,
    },
    data() {
        return {
            search_terms: [
                {
                    keyword: '',
                    start_date: '',
                    end_date: '',
                },
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
        addSearch() {
            this.search_terms.push({
                    keyword: '',
                    start_date: '',
                    end_date: '',
            });
            this.valids.push(true)
        },
        deleteSearch(index) {
            //console.log(index);
            this.search_terms.splice(index, 1);
            this.valids.splice(index, 1)
            //console.log(this.search_terms);
        },
        canBeRemoved(index) {
            return index !== 0;
        },
        setSearch(index, search) {
            this.search_terms[index] = search;
            this.$emit('updateSearches', this.search_terms)
        },
        setRemoteValue() {
            if(this.search_terms.length > 1) {
                this.search_terms[1].keyword = "Teclado";
            }
        },
    },
};
</script>