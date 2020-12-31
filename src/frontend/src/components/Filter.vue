<template>
  <section class="pa-3">
    <v-container>
      <v-form
      ref="form"
      v-model="valid">
        <v-row>
          <v-col xs="5" md="5">
            <div class="px-7">
              <v-text-field
                label="Keyword"
                required
                v-model="search.keyword"
                @input="() => onSetSearch(index, search)"
                :rules="keywordRules"
              ></v-text-field>
            </div>
          </v-col>
          <v-col xs="3" md="3">
            <div class="pr-7">
              <v-menu
                ref="menuFromDate"
                v-model="menuFromDate"
                :close-on-content-click="false"
                :return-value.sync="search.start_date"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="search.start_date"
                    label="From Date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    @input="() => onSetSearch(index, search)"
                    v-on="on"
                    :rules="fromdateRules"
                    required
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="search.start_date"
                  no-title
                  scrollable
                  :picker-date.sync="pickerDate"
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    text
                    color="primary"
                    @click="menuFromDate = false"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="selectFromDate"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </div>
          </v-col>
          <v-col xs="3" md="3">
            <v-menu
                ref="menuToDate"
                v-model="menuToDate"
                :close-on-content-click="false"
                :return-value.sync="search.end_date"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="search.end_date"
                    label="To Date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    @input="() => onSetSearch(index, search)"
                    v-on="on"
                    :rules="toDateRules"
                    required
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="search.end_date"
                  no-title
                  scrollable
                  :min="search.start_date"
                  :picker-date.sync="pickerToDate"
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    text
                    color="primary"
                    @click="menuToDate = false"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.menuToDate.save(search.end_date)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
          </v-col>
          <v-col xs="1" md="1" lg="1">
            <div class="pr-7 pt-5">
              <v-btn
                v-if="canBeRemoved"
                text
                icon
                color="error"
                @click="() => onDelete(index)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
  </section>
</template>




<script>
export default {
  name: 'FilterItem',
  data(){
    return{
      valid: true,
      menuFromDate: false,
      menuToDate: false,
      pickerDate: null,
      pickerToDate: null,

      keywordRules: [
        v => !!v || 'A keyword is required'
      ],
      fromdateRules: [
        v => !!v || 'A starting date is required'
      ],
      toDateRules: [
        v => !!v || 'A end date is required',
        v => v >= this.search.start_date || 'End date must be later thatn start date'
      ],
    }
  },
  props: {
    onSetSearch: {
      type: Function,
      required: true
    },
    onDelete: Function,
    canBeRemoved: Boolean,
    index: {
      type: Number,
      required: true,
    },
    searchOriginal: Object,
  },
  computed: {
    search() {
      return this.searchOriginal;
    },
  },
  methods:{
    selectFromDate(){
      this.$refs.menuFromDate.save(this.search.start_date)
      if(this.search.start_date > this.search.end_date){
        this.search.end_date = this.search.start_date
      }
    },
    validate () {
        this.$refs.form.validate()
      },
  },
  mounted: function(){
    this.pickerDate = '1900-01'
    this.pickerToDate = '1900-01'
  }
};
</script>

<style scoped></style>