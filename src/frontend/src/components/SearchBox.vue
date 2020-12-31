<template>
<v-container>
    <v-spacer></v-spacer>
  <v-row align="center" justify="end" >
    <v-col lg="1" md="2" sm="3"  align-self="center">
      <v-select 
        label="Split"
        :items="splits"
        v-model="selectedSplit"
        @change="() => $emit('split-changed', selectedSplit)"
        >
        </v-select>
    </v-col>
    <v-col lg="1" md="2" sm="3">
      <v-checkbox
        v-on:change="$emit('ocr-changed', ocr)"
        :disabled="count || !bna_configured"
        v-model="ocr"
        label="OCR"
        ></v-checkbox>
    </v-col>
    <v-col lg="1" md="2" sm="3">
      <v-switch
        v-on:change="$emit('count-changed', count)"
        v-model="count"
        label="Count"
        ></v-switch>
    </v-col>
    <v-col lg="1" md="2" sm="3">
        <v-btn
        v-on:click="$emit('search')"
        color="primary"
        >Search</v-btn>
      </v-col>
  </v-row>
</v-container>
</template>

<script>
import axios from 'axios';
export default {
  name: 'SearchBox',
  data(){
    return {
      bna_configured: false,
      count: false,
      ocr: false,
      splits: ['None',  'Day', 'Week', 'Month', 'Year'],
      selectedSplit: null,
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
  },
  watch: {
    count: {
      handler: function(newVal) {
        if(newVal){
          this.ocr = false
        }
      }
    },
  },
  mounted(){
    this.getBNAConfiguration()
  }
};
</script>
