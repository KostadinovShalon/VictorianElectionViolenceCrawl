<template>
<v-container class="justifi-center align-start pa-0 ma-0">
    <div v-if="searchIndices == null" class="text-h3 ma-9">Candidate Documents</div>
    <div v-else class="text-h3 ma-9">Candidates <span class="text-h4">(From searches: 
                <span v-for="i in searchIndices.length" v-bind:key="i">
                    {{searchIndices[i-1]}}<span v-if="i < searchIndices.length">,</span> </span>)</span></div>
    <v-data-table
        :headers="candidatesHeaders"
        :items="candidates"
        :item-key="candidates.id"
        :options.sync="options"
        :server-items-length="totalCandidates"
        :loading="loading"
        :single-expand="false"
        :expanded.sync="expanded"
        show-expand
        class="elevation-0">
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length" class="pa-0">
              <expanded-document
              v-bind:description="item.description"
              v-bind:ocr="item.ocr"
              v-bind:disabledOCRButton="disable_update_ocr || !bna_configured"
              v-on:download-ocr="ocrToUpdateId = item.id;ocrDialog = true"></expanded-document>
          </td>
        </template>
        <template v-slot:[`item.preview`]="{ item }">
            <v-btn
            color="primary"
            v-model="item.preview"
            :disabled="!bna_configured"
            @click="previewDialog = true; previewId = item.id">
                <v-icon>mdi-link</v-icon>
            </v-btn>
        </template>
        <template v-slot:[`item.status`]="{ item }">
            <v-select
            v-model="item.status"
            :items="states"
            @change="changedCandidateStatus(item.id, item.status)"
            :disabled="!bna_configured || !storage_configured"
            ></v-select>
        </template>
    </v-data-table>
    <v-row class="mt-2 pa-3">
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="toPortalDialog = true" :disabled="documentsAffected == 0 || !bna_configured || !storage_configured">Process</v-btn>
    </v-row>


    <!--Processing Candidates Dialog ------------------------------------------------------>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="1000"
    >
      <v-card>
        <v-app-bar color="primary" dark>
          <v-card-title class="headline" v-if="finished">
              Candidates to Portal (Finished)
          </v-card-title>
          <v-card-title class="headline" v-else>
            Candidates to Portal
          </v-card-title>
        </v-app-bar>
          <template>
            <v-card-text class="text--primary pa-5">
              <v-row  class="px-5">
                <span class="pr-15">
                  Processing {{processProgress.index}} of {{processProgress.total}} candidates
                </span>
              </v-row>
            </v-card-text>

            <v-divider class="mx-5 mb-5"></v-divider>
            <v-card-text class="text--primary px-5">
              <v-row class="px-5">
                <div v-if="!finished">
                  <b>Status:</b> {{processProgress.status}}
                </div>
                <div v-else>
                    <h3>Finished</h3>
                </div>
              </v-row>
            </v-card-text>
            <v-flex class="pa-5" v-if="processing">
              <v-progress-linear
              color="primary"
              height="25"
              slot="progress"
              v-model="currentProgress"
              striped
              rounded
              >
              </v-progress-linear>
            </v-flex>
          </template>
        <v-card-actions v-if="!finished">
          <v-spacer></v-spacer>
          <v-btn
            class="py-3"
            elevation="5"
            color="error"
            @click="stopProcess"
            outlined
          >
          <strong>
            Cancel
          </strong>
          </v-btn>
        </v-card-actions>
        <v-card-actions v-if="finished">
          <v-spacer></v-spacer>
          <v-btn
            class="py-3"
            elevation="5"
            color="primary"
            @click="processAfterFinish"
            outlined
          >
          <strong>
            Ok
          </strong>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!------------------------------------------------------------------------>

    <!-- SNACK BAR ----------------------------------------------------------->
    <v-snackbar v-model="ocr_snackbar">
      {{ snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="primary"
          text
          v-bind="attrs"
          @click="ocr_snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <!------------------------------------------------------------------------>

    <!---- Preview Dialog ----------------------------------------------------->
    <proceed-dialog
      title="Get Preview"
      message="The preview will be downloaded using your BNA account. Do you want to proceed?"
      v-bind:show="previewDialog"
      v-on:cancel="previewDialog = false"
      v-on:ok="openPreview"></proceed-dialog>
    <!------------------------------------------------------------------------>

    <!---- OCR Dialog ----------------------------------------------------->
    <proceed-dialog
      title="Download OCR"
      message="The OCR be downloaded using your BNA account. Do you want to proceed?"
      v-bind:show="ocrDialog"
      v-on:cancel="ocrDialog = false"
      v-on:ok="updateOCR"></proceed-dialog>
    <!------------------------------------------------------------------------>

    <!---- To Portal Dialog ----------------------------------------------------->
    <proceed-dialog
      title="Candidates to Portal"
      v-bind:message="documentsAffected + ' candidate documents will be affected. Do you want to proceed?'"
      v-bind:show="toPortalDialog"
      v-on:cancel="toPortalDialog = false"
      v-on:ok="processCandidates"></proceed-dialog>
    <!------------------------------------------------------------------------>
    <no-database-dialog></no-database-dialog>
</v-container>
</template>

<script>
import axios from 'axios';
import NoDatabaseDialog from '../components/NoDatabaseDialog.vue';
import ExpandedDocument from '../components/ExpandedDocument';
import ProceedDialog from '../components/ProceedDialog';
export default {
    name: 'Candidates',
    components: {NoDatabaseDialog, ExpandedDocument, ProceedDialog},
    data() {
        return{
            bna_configured: false,
            storage_configured: false,
            ocrDialog: false,
            ocrToUpdateId: 0,
            toPortalDialog: false,
            previewId: null,
            previewDialog: false,
            expanded: [],
            fromSearches: [],
            totalCandidates: 0,
            loading: true,
            options: {},
            candidatesHeaders: [
                { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px" },
                { text: 'Title', value: 'title'},
                { text: 'Newspaper', value: 'publication_title'},
                { text: 'Publication Location', value: 'publication_location'},
                { text: 'Publication Date', value: 'publication_date'},
                { text: 'Preview', value: 'preview', sortable: false},
                { text: 'Status', value: 'status', sortable: false},
                { text: '', value: 'data-table-expand' },
            ],
            states: ['', '0', '1', '2', '3', '4', '5'],
            candidates: [],
            statusChanges: {},
            originalStatus: {},
            processProgress: {},
            finished: false,
            processing: false,
            dialog: false,
            pollInterval: null,
            ocr_snackbar: false,
            snackbar_text: "Problem updating OCR",
            disable_update_ocr: false,
            documentsAffected: 0
        }
    },
    computed: {
        commonurl(){
            return this.$store.state.commonurl
        },
        currentProgress(){
            return Math.floor(this.processProgress.index *100 / this.processProgress.total)
        },
        searchIndices(){
            var body = this.$store.state.selected_searches
            if(body.length == 0){
                body = null
            }
            return body
        }
    },
    methods: {
        openPreview(){
            window.open(this.commonurl + 'candidates/preview?id=' + this.previewId, '_blank')
            this.previewDialog = false
        },
        changedCandidateStatus(id, status){
            this.statusChanges[id] = status
            if(this.originalStatus[id] == status){  // Removing if returning to the original status
                delete this.statusChanges[id]
            }
            this.documentsAffected = Object.keys(this.statusChanges).length
        },
        processCandidates() {
            this.finished = false
            const body = Object.entries(this.statusChanges).map(entry =>{
                const [id, status] = entry
                return {id: parseInt(id), status: status}
            })
            axios.put(this.$store.state.commonurl + "candidates", body)
                .then(response => {
                    if(response.status == 200){
                        this.checkStatus()
                    }
                })
            this.pollInterval = setInterval(() => {this.checkStatus()}, 500)
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

            axios.post(this.commonurl + "candidates", this.searchIndices, {params: params}).then(response =>{  // DON'T REMOVE THE TRAILING SLASH
                if(response.status == 200){
                    console.log(response)
                    this.candidates = response.data.candidates
                    this.totalCandidates = response.data.total
                    if(this.candidates === null){
                      this.candidates = []
                    }
                    // Handling changes of status after changing a page
                    this.candidates.forEach(candidate => {
                        if(candidate["status"] !== null){
                            candidate["status"] = candidate["status"].toString()
                        }
                        this.originalStatus[candidate.id] = candidate.status
                        if(candidate.id in this.statusChanges){
                            if(candidate.status == this.statusChanges[candidate.id]){
                                delete this.statusChanges[candidate.id]  //  If status is the same as original, remove from status changes
                            } else {
                                candidate.status = this.statusChanges[candidate.id]  // Else, update GUI status value
                            }
                        }
                    })
                }
            })
            .catch(() => {})
            .then(() => {this.loading = false})

        },
        processAfterFinish(){
            this.dialog = false
            this.getDataFromApi()
        },
        checkStatus(){
            axios.get(this.$store.state.commonurl + "candidates").then(response => {
                var wasProcessing = this.processing
                var currentProcessing = false
                if(response.status == 200){
                    this.processProgress = response.data
                    currentProcessing = response.data.uploading
                } else {
                    this.processProgress = null
                }

                if(wasProcessing && !currentProcessing){
                    this.finished = true
                    this.statusChanges = {}
                }
                this.processing = currentProcessing

                this.dialog = this.processing || this.finished

                if(!this.processing){
                    clearInterval(this.pollInterval)
                }
            })
        },
        stopProcess(){
            axios.delete(this.$store.state.commonurl + "candidates/stop")
        },
        updateOCR(){
            this.disable_update_ocr = true
            axios.put(this.commonurl + "candidates/update-ocr", this.ocrToUpdateId, {headers: {'Content-Type': 'text/plain'}})
            .then(() => this.getDataFromApi())
            .catch(() => this.ocr_snackbar = true)
            .then(() => this.disable_update_ocr = false)
            this.ocrDialog = false
        },
        getBNAConfiguration(){
            axios.get(this.commonurl + "setup/bna")
            .then((response) => {
                var details = response.data
                this.bna_configured = details.password !== null && details.username !== null
            })
        },
        getServerConfiguration(){
            axios.get(this.commonurl + "setup/server")
            .then((response) => {
                var details = response.data
                var local = details.local
                if(local){
                    this.storage_configured = details.files_dir !== null
                } else {
                    this.storage_configured = details.password !== null && details.user !== null && details.host !== null
                }
            })
        }
    },
    mounted(){
        this.getServerConfiguration()
        this.getBNAConfiguration()
        axios.get(this.$store.state.commonurl + "candidates")
            .then((response) => {
                this.processProgress = response.data
                this.processing = response.data.uploading
                if(!this.processing){
                    this.getDataFromApi()
                }
                this.dialog = response.data.uploading
            })
        this.pollInterval = setInterval(() => {this.checkStatus()}, 500)
    },
    watch: {
      options: {
        handler () {
          if(!this.processing){
            this.getDataFromApi()
          }
        },
        deep: true,
      },
    },
};
</script>