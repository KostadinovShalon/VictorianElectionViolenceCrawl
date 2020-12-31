<template>
  <v-container class="align-start justify-start">
    <div class="text-h3 ma-5">Advanced Search</div>
    <advanced-filters @updateAdvancedSearches="updateAdvancedSearches" ref="filters"></advanced-filters>
    <search-box
          v-on:ocr-changed="opts.ocr = $event"
          v-on:count-changed="updateCountingMode"
          v-on:search="processInfo"
          v-on:split-changed="opts.split = $event"
        ></search-box>
    <!------------- Crawling Dialog ----------------------------------------->
    <crawling-dialog
      v-bind:dialog="dialog"
      v-bind:crawling="scrapping"
      v-bind:finished="finished"
      v-bind:withOCR="opts.ocr"
      v-bind:currentProgress="currentProgress"
      v-on:cancel="cancelDialog = true"
      v-on:ok="dialog = false">

      <template v-slot:past-downloads>
        <advanced-crawled-data
          v-for="(item, index) in search_progress_done" v-bind:key="item.keyword"
          v-bind:searchTerms="getSearchTerms(index)"
          v-bind:downloadedArticles="search_progress.downloaded_articles[index]"
          v-bind:totalArticles="search_progress.total_articles[index]">
        </advanced-crawled-data>
      </template>

      <template v-slot:current-crawling-text>
        <h3><b>Crawling: </b></h3>
        <span v-for="(value, key) in getSearchTerms(search_progress.search_index)" v-bind:key="key">
            <b>{{key}}: </b> {{value}} <br>
        </span>
      </template>

      <template v-slot:crawling-bar-text>
        <strong>
          Downloading: 
          {{search_progress.downloaded_articles[search_progress.search_index]}} 
          of 
          {{search_progress.total_articles[search_progress.search_index]}} 
          articles
        </strong>
      </template>
    
    </crawling-dialog>
    <!------------- ---------------------------------------------------------->
    
    <!--COUNTING DIALOG ------------------------------------------------------>
    <counting-dialog
      v-bind:dialog="countingDialog"
      v-bind:finished="finishedCounting"
      v-bind:counting="counting"
      v-on:cancel="finishedCounting = true"
      v-on:ok="countingDialog = false">
      <v-card-text class="text--primary pa-5" v-for="(item, index) in counting_done" v-bind:key="item.keyword">
        <v-row  class="px-5" style="text-align: left">
        <v-col class="pr-15">

          <span v-for="(value, key) in getSearchTerms(index, true)" v-bind:key="key">
                <b>{{key}}: </b> {{value}} <br>
            </span>
            <b>Total articles:  </b> {{countingResult.total_articles[index]}}
        </v-col>
        </v-row>
      </v-card-text>
    </counting-dialog>
    <!------------------------------------------------------------------------>

    <!---- Cancel Dialog ----------------------------------------------------->
    <proceed-dialog
     title="Cancel Search?"
     message="Are you sure you want to cancel the current search?"
     v-bind:show="cancelDialog"
     v-on:cancel="cancelDialog = false"
     v-on:ok="stopSearch"></proceed-dialog>
    <!------------------------------------------------------------------------>
    <!---- NO DB Dialog ----------------------------------------------------->
    <no-database-dialog></no-database-dialog>
    <!----------------------------------------------------------------------->
  </v-container>
</template>

<script>
import SearchBox from '../components/SearchBox.vue';
import AdvancedFilters from '../components/AdvancedFilters.vue';
import NoDatabaseDialog from '../components/NoDatabaseDialog.vue';
import axios from 'axios';
import CrawlingDialog from '../components/CrawlingDialog.vue';
import AdvancedCrawledData from '../components/AdvancedCrawledData.vue';
import CountingDialog from '../components/CountingDialog.vue';
import ProceedDialog from '../components/ProceedDialog.vue';
export default {
  name: 'AdvancedSearch',
  components:{
    SearchBox,
    AdvancedFilters,
    NoDatabaseDialog,
    CrawlingDialog,
    AdvancedCrawledData,
    CountingDialog,
    ProceedDialog
  },
  data() {
    return{
      cancelDialog: false,
      pollInterval: null,
      finished: false,
      dialog: false,
      scrapping: false,//this is to show the modal dialog
      searches: [],
      counting: false,
      countingDialog: false,
      finishedCounting: false,
      //this sets the default state of each checkbox in searchbox.vue
      countingResult: {
        search_terms: [],
        total_articles: []
      },
      opts: {
        ocr: false,
        count: false,
        split: null
      },
      search_progress: {
        search_terms: [],
        search_index: 0
      }
    };
  },
  computed: {
    search_progress_done() {
      if(this.finished){
        return this.search_progress.search_terms
      }
      var done = []
      var i;
      for(i = 0; i<this.search_progress.search_index; i++){
        done.push(this.search_progress.search_terms[i])
      }
      return done
    },
    counting_done() {
      if(this.finishedCounting){
        return this.countingResult.search_terms
      }
      var done = []
      var i;
      for(i = 0; i<this.countingResult.total_articles.length; i++){
        done.push(this.countingResult.search_terms[i])
      }
      return done
    },
    currentProgress(){
      if(this.search_progress.search_terms.length == 0 
      && this.search_progress.search_index == 0){
        return 0
      }
      var i = this.search_progress.search_index
      return Math.floor(this.search_progress.downloaded_articles[i] *100 / this.search_progress.total_articles[i])
    },
    commonurl(){
        return this.$store.state.commonurl
    }
  },
  methods: {
    getSearchTerms(index, count=false){
      var st = null
      if(!count){
        st = this.search_progress.search_terms[index]
      } else {
        st = this.countingResult.search_terms[index]
      }
      var validST = {}
      if(st.searchAllWords != null){
        validST["Search All Words"] = st.searchAllWords
      }
      if(st.searchSomeWords != null){
        validST["Search Some Words"] = st.searchSomeWords
      }
      if(st.useExactPhrase != null){
        validST["Exact Phrase"] = st.useExactPhrase
      }
      if(st.publicationPlace != null){
        validST["Publication Place"] = st.publicationPlace
      }
      if(st.excludeWords != null){
        validST["Exclude Words"] = st.excludeWords
      }
      if(st.exactSearch){
        validST["Exact search"] = st.exactSearch
      }
      if(st.newspaperTitle != null){
        validST["Newspaper Title"] = st.newspaperTitle
      }
      if(st.articleType != null){
        validST["Article Type"] = st.articleType
      }
      if(st.fromDate != null){
        validST["From Date"] = st.fromDate
      }
      if(st.toDate != null){
        validST["To Date"] = st.toDate
      }
      if(st.fromDateAddedToSystem != null){
        validST["From Added Date"] = st.fromDateAddedToSystem
      }
      if(st.toDateAddedToSystem != null){
        validST["To Added Date"] = st.toDateAddedToSystem
      }
      if(st.tags != null){
        validST["Tags"] = st.tags
      }
      if(st.sortResultsBy != null){
        validST["Sort Results By"] = st.sortResultsBy
      }
      if(st.frontPageArticlesOnly){
        validST["Front Page Articles Only"] = st.frontPageArticlesOnly
      }
      return validST
    },
    updateAdvancedSearches(value){
      this.searches = value
    },
    updateCountingMode(value){
      this.opts.count = value
      if(value){
        this.opts.ocr = false
      }
    },

    //------------------------------ WEB ----------------------------------//
    processInfo() {
      this.$refs.filters.validate()
      var isValid = true
      var j;
      for(j=0;j<this.$refs.filters.valids.length;j++){
        if(!this.$refs.filters.valids[j]){
          isValid = false
          break
        }
      }
      if(isValid){
        var i;
        for(i=0;i<this.searches.length;i++){
          console.log(this.searches[i])
          if(typeof this.searches[i].newspaperTitle === 'undefined'){
            this.searches[i]["newspaperTitle"] = null
          }
          if(typeof this.searches[i].publicationPlace === 'undefined'){
            this.searches[i]["publicationPlace"] = null
          }
          if(this.searches[i].articleType !== null && this.searches[i].articleType.length == 0){
            this.searches[i]["articleType"] = null
          }
        }

        var searches = JSON.parse(JSON.stringify(this.searches))
        console.log(searches);

        var searchBody = {
            mode: "advanced",
            terms: searches,
            ocr: this.opts.ocr
        };
        if(this.opts.split !== null && this.opts.split !== "None"){
          searchBody["split"] = this.opts.split.toLowerCase()
        }

        this.submit(searchBody, this.opts.count)
        if(!this.opts.count){
          this.pollInterval = setInterval(() => {this.checkStatus()}, 200)
        } else {
          this.pollInterval = setInterval(() => {this.checkCountStatus()}, 200)
        }
      }
    },
    submit(searchBody, count=false){
        if(!count){
          this.finished = false
          this.search_progress = {
            search_terms: [],
            search_index: 0
          }
          axios.post(this.$store.state.commonurl + "search", searchBody)
              .then(response => {
                if(response.status == 200){
                  this.search_progress = response.data
                  this.scrapping = response.data.scrapping
                  this.dialog = response.data.scrapping
                }
              })
        } else {
          this.finishedCounting = false
          axios.post(this.$store.state.commonurl + "search/count", searchBody)
              .then(response => {
                if(response.status == 200){
                  this.countingResult = response.data
                  this.counting = response.data.scrapping
                  this.countingDialog = response.data.scrapping
                }
              })
        }
    },
    stopSearch(){
      this.cancelDialog = false
      axios.post(this.$store.state.commonurl + "search/stop")
    },
    checkStatus(){
      axios.get(this.$store.state.commonurl + "search").then(response => {
        var wasScrapping = this.scrapping
        var currentScrapping = false
        if(response.status == 200){
          this.search_progress = response.data
          currentScrapping = response.data.scrapping
        } else {
          this.search_progress = null
        }

        if(wasScrapping && !currentScrapping){
          this.finished = true
        }
        this.scrapping = currentScrapping

        this.dialog = this.scrapping || this.finished

        if(!this.scrapping){
          clearInterval(this.pollInterval)
        }
      })
    },
    checkCountStatus(){
      axios.get(this.$store.state.commonurl + "search/count").then(response => {
        var wasCounting = this.counting
        var currentCounting = false
        if(response.status == 200){
          console.log(response.data)
          this.countingResult = response.data
          currentCounting = response.data.counting
        } else {
          this.countingResult = null
        }

        if(wasCounting && !currentCounting){
          this.finishedCounting = true
        }
        this.counting = currentCounting

        this.countingDialog = this.counting || this.finishedCounting

        if(!this.counting){
          clearInterval(this.pollInterval)
        }
      })
    }
  },
  mounted: function(){
    axios.get(this.$store.state.commonurl + "search")
    .then((response) => {
      this.search_progress = response.data
      this.scrapping = response.data.scrapping
      this.dialog = response.data.scrapping
    })
    this.pollInterval = setInterval(() => {this.checkStatus()}, 200)
   }
};
</script>