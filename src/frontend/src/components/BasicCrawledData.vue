<template>
  <v-card-text class="text--primary pa-5">
    <v-row  class="px-5" style="text-align: left">
    <v-col class="pr-15">
        <b>Crawled </b> '{{item.keyword}}' from {{item.start_date}} to {{item.end_date}} <br> 
        <b>Total articles:  </b> {{downloadedArticles}} of {{totalArticles}}
    </v-col>
    </v-row>
</v-card-text>
</template>

<script>
export default {
    name: "BasicCrawledData",
    props: {
        item: Object,
        downloadedArticles: Number,
        totalArticles: Number
    }
}
</script>