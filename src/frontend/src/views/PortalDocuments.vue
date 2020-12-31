<template>
<v-container class="justifi-center align-start pa-0 ma-0">
    <div class="text-h3 ma-9">Portal Documents</div>
    <v-data-table
        :headers="headers"
        :items="documents"
        :item-key="documents.id"
        :options.sync="options"
        :server-items-length="total"
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
                :disabledOCRButton="true"></expanded-document>
          </td>
        </template>
        <template v-slot:[`item.full_preview`]="{ item }">
          <preview-button
           v-bind:uri="item.pdf_uri"
           v-bind:link="getPDFUri(item)"
           v-on:reload="pdfDialog = true; pdfToUpdateId = item.id">
           </preview-button>
        </template>
        <template v-slot:[`item.cropped_preview`]="{ item }">
            <preview-button
            v-bind:uri="item.cropped_pdf_uri"
            v-bind:link="getCroppedPDFUri(item)"
            v-on:reload="pdfDialog = true; pdfToUpdateId = item.id">
            </preview-button>
        </template>
    </v-data-table>

    <!--Updating Files Dialog ------------------------------------------------------>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <v-card>
        <v-app-bar color="primary" dark>
          <v-card-title class="headline" v-if="updatingFinished">
              Updating Files (Document {{updatingDocumentId}}) (Finished)
          </v-card-title>
          <v-card-title class="headline" v-else>
            Updating Files (Document {{updatingDocumentId}})
          </v-card-title>
        </v-app-bar>
          <template>
            <v-card-text class="text--primary pa-5">
              <v-row  class="px-5">
                <div v-if="!updatingFinished">
                  <b>Status:</b> {{updatingStatus}}
                </div>
                <div v-else>
                    <h3>Finished</h3>
                </div>
              </v-row>
            </v-card-text>
          </template>
        <v-card-actions v-if="!updatingFinished">
          <v-spacer></v-spacer>
          <v-btn
            class="py-3"
            elevation="5"
            color="error"
            @click="stopUpdating"
            outlined
          >
          <strong>
            Cancel
          </strong>
          </v-btn>
        </v-card-actions>
        <v-card-actions v-if="updatingFinished">
          <v-spacer></v-spacer>
          <v-btn
            class="py-3"
            elevation="5"
            color="primary"
            @click="dialog = false"
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

    <!---- Update PDF Dialog ----------------------------------------------------->
    <proceed-dialog
      title="Reload PDF"
      message="The full and cropped article are going to be downloaded using your BNA account. Do you want to proceed?"
      v-bind:show="pdfDialog"
      v-on:cancel="pdfDialog = false"
      v-on:ok="updateFiles"></proceed-dialog>
    <!------------------------------------------------------------------------>
    <no-database-dialog></no-database-dialog>
</v-container>
</template>

<script>
import axios from 'axios';
import NoDatabaseDialog from '../components/NoDatabaseDialog.vue';
import ExpandedDocument from '../components/ExpandedDocument.vue';
import PreviewButton from '../components/PreviewButton.vue';
import ProceedDialog from '../components/ProceedDialog.vue'
export default {
    name: 'PortalDocuments',
    components: {NoDatabaseDialog, ExpandedDocument, PreviewButton, ProceedDialog},
    data() {
        return{
            pdfDialog: false,
            pdfToUpdateId: 0,
            dialog: false,
            updatingFinished: false,
            updatingDocumentId: 0,
            updatingStatus: null,
            updating: false,
            pollInterval: null,
            storage_configured: false,

            expanded: [],
            total: 0,
            loading: true,
            options: {},
            headers: [
                { text: 'Id', align: 'start', value: 'id', fixed: true, width: "100px"},
                { text: 'Title', value: 'title'},
                { text: 'Newspaper', value: 'publication_title'},
                { text: 'Publication Location', value: 'publication_location'},
                { text: 'Publication Date', value: 'publication_date'},
                { text: 'Full article', value: 'full_preview', sortable: false},
                { text: 'Cropped article', value: 'cropped_preview', sortable: false},
                { text: 'Type', value: 'type'},
                { text: 'Word Count', value: 'word_count'},
                { text: '', value: 'data-table-expand' },
            ],
            documents: [],
        }
    },
    computed: {
        commonurl(){
            return this.$store.state.commonurl
        },
    },
    methods: {
        getPDFUri(item){
          if(item.pdf_uri === null){
            return null
          }
          if(item.pdf_uri.startsWith('http')){
            return item.pdf_uri
          }
          return this.commonurl + "portal/local/full?id=" + item.id.toString()

        },
        getCroppedPDFUri(item){
          if(item.cropped_pdf_uri === null){
            return null
          }
          if(item.cropped_pdf_uri.startsWith('http')){
            return item.cropped_pdf_uri
          }
          return this.commonurl + "portal/local/cropped?id=" + item.id.toString()

        },
        stopUpdating(){
            axios.delete(this.commonurl + "portal/update/stop")
            this.dialog = false
            this.updating = false
            this.getDataFromApi()
        },
        updateFiles(){
            this.updatingDocumentId = this.pdfToUpdateId
            this.updatingFinished = false
            axios.put(this.commonurl + "portal/update", this.pdfToUpdateId, {headers: {'Content-Type': 'text/plain'}})
            this.pollInterval = setInterval(() => {this.checkStatus()}, 500)
            this.pdfDialog = false
        },
        checkStatus(){
            axios.get(this.$store.state.commonurl + "portal/update").then(response => {
                var wasUpdating = this.updating
                var currentUpdating = response.data.updating
                this.updatingStatus = response.data.status
                if(wasUpdating && !currentUpdating){
                    this.updatingFinished = true
                    this.getDataFromApi()
                }
                this.updating = currentUpdating

                this.dialog = this.updating || this.updatingFinished

                if(!this.updating && this.pollInterval !== null){
                    clearInterval(this.pollInterval)
                }
            })
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

            axios.get(this.commonurl + "portal", {params: params}).then(response =>{
                if(response.status == 200){
                    this.documents = response.data.documents
                    this.total = response.data.total
                    console.log(this.documents)
                }
            })
            .catch(() => {})
            .then(() => {this.loading = false})

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
       this.getDataFromApi()
       this.checkStatus()
       this.getServerConfiguration()
       this.pollInterval = setInterval(() => {this.checkStatus()}, 500)
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