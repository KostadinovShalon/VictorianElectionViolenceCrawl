<template>
  <v-card-text class="text--primary pa-5">
    <v-row  class="px-5" style="text-align: left">
    <v-col class="pr-15">
        <b>Crawled </b><br>
        <span v-for="(value, key) in searchTerms" v-bind:key="key">
            <b>{{key}}: </b> {{value}} <br>
        </span>
        <b>Total articles:  </b> {{downloadedArticles}} of {{totalArticles}}
    </v-col>
    </v-row>
</v-card-text>
</template>

<script>
export default {
    name: "AdvancedCrawlerData",
    props: {
        searchTerms: Object,
        downloadedArticles: Number,
        totalArticles: Number
    }
}
</script>