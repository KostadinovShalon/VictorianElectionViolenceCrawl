<template>
    <v-container class="align-center">
      <v-row justify="center mt-10">
        <v-col s="12" sm="8" md="5" lg="5">
          <v-card class="elevation-7 px-10">
            <v-card-title class="pt-10 pr-10 pl-10 pb-5 text-h4">Database Connection</v-card-title>
            <v-switch v-model="localSwitch" label="Local"></v-switch>
            <v-card-text>

              <v-form ref="form" v-model="valid">
                <v-row class=" px-3" v-if="!localSwitch">
                    <v-flex xs6>
                      <v-text-field
                      class="pr-3 pb-5"
                      prepend-icon="mdi-database"
                      label="Host"
                      required
                      :rules="hostRules"
                      v-model="host"
                      ></v-text-field>
                  </v-flex>

                  <v-flex xs6>
                      <v-text-field
                      class="pl-3 pb-5"
                      prepend-icon="mdi-serial-port"
                      label="Port"
                      type="number"
                      v-model="port"
                      required
                      ></v-text-field>
                  </v-flex>
                </v-row>

                <v-text-field  v-if="!localSwitch"
                  class="pb-5"
                  prepend-icon="person"
                  name="user"
                  label="User"
                  type="email "
                  :rules="userRules"
                  v-model="user"
                  required
                >
                </v-text-field>

                <v-text-field v-if="!localSwitch"
                  class="pb-5"
                  prepend-icon="lock"
                  name="password"
                  label="Password"
                  type="password"
                  required
                  v-model="password"
                  :rules="passwordRules"
                >
                </v-text-field>

                <v-card-text v-else>
                  <v-row class="px-3">
                    <v-col xs="6">
                      <v-text-field
                      class="pr-3 pb-5"
                      prepend-icon="mdi-folder"
                      label="Absolute Path"
                      required
                      :rules="pathRules"
                      v-model="path"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-card-text>

              </v-form>
            </v-card-text>
            <v-card-actions class="justify-center pb-10">
              <v-btn
                class="px-16"
                color="primary"
                :disabled="!valid"
                @click="proceedDialog = true"
                >Ok</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <proceed-dialog
      title="Database Update"
      message="Do you want to update the database connection?"
      v-bind:show="proceedDialog"
      v-on:cancel="proceedDialog = false"
      v-on:ok="submit"></proceed-dialog>
     <success-dialog
      title="Database Update"
      message="Database connection updated"
      v-bind:show="successDialog"
      v-on:ok="successDialog = false"></success-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
import ProceedDialog from '../components/ProceedDialog.vue';
import SuccessDialog from '../components/SuccessDialog.vue';
export default {
    name: 'DatabaseConn',
    components: {
      ProceedDialog,
        SuccessDialog
    },
    data() {
        return{
          localSwitch: false,
          proceedDialog: false,
            successDialog: false,
            valid: false,
            user: '',
            password: '',
            host: '',
            port: 3600,
            path: null,
            hostRules: [
              v => (this.localSwitch || !!v) || 'Host is required'
            ],
            userRules: [
              v => this.localSwitch || !!v || 'User is required'
            ],
            passwordRules: [
                v => this.localSwitch || !!v || 'Password is required'
            ],
            pathRules: [
              v => !this.localSwitch || !!v || 'Path is required'
            ]
        };
    },
    methods: {
      processResponse: function(response){
              var details = response.data
                if(details != null){
                  this.localSwitch = details.local
                  this.user = details.user
                  this.password = details.password
                  this.host = details.host
                  this.path = details.data_dir
                }
      },
      submit(){
        this.$refs.form.validate()
        if(this.valid){
          this.proceedDialog = false
          var submitData = {
              user: this.user, 
              password: this.password,
              host: this.host,
              local: this.localSwitch, 
              data_dir: this.path
            }
          axios.post("http://127.0.0.1:5000/setup/db", submitData)
              .then((response) => {
                this.successDialog = true
                this.processResponse(response)})
        }
      }
    },
    mounted: function(){
      axios.get("http://127.0.0.1:5000/setup/db")
      .then((response) => {
        this.processResponse(response)
      })
    }
};
</script>