<template>
 <v-container class="align-center">
    <v-row justify="center">
      <v-col xs="12" sm="8" md="5">
        <v-card class="elevation-7 px-10">
          <v-card-title class="pt-10 pr-10 pl-10 pb-5 text-h4">Storage Configuration</v-card-title>
          <v-alert type="info" :value="local">Database is set to local.</v-alert>
          <v-card-text >
            <v-form ref="form" v-model="valid" :disabled="local">
                  <v-row class=" px-3">
                  <v-flex xs6>
                    <v-text-field
                    class="pr-3 pb-5"
                    prepend-icon="mdi-database"
                    label="Host"
                    required
                    v-model="host"
                    ></v-text-field>
                </v-flex>
              </v-row>

              <v-text-field
                class="pb-5"
                prepend-icon="person"
                name="email"
                label="FTP User"
                type="email"
                v-model="user"
                required
              >
              </v-text-field>

              <v-text-field
                class="pb-5"
                prepend-icon="lock"
                name="password"
                label="Password"
                id="password"
                type="password"
                required
                v-model="password"
                :rules="passwordRules"
              >
              </v-text-field>
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
      title="Storage Update"
      message="Do you want to update the storage information?"
      v-bind:show="proceedDialog"
      v-on:cancel="proceedDialog = false"
      v-on:ok="submit"></proceed-dialog>
     <success-dialog
      title="Storage Update"
      message="Storage updated"
      v-bind:show="successDialog"
      v-on:ok="successDialog = false"></success-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
import ProceedDialog from '../components/ProceedDialog.vue';
import SuccessDialog from '../components/SuccessDialog.vue';
export default {
    name: 'ServerVariables',
    components: {
      ProceedDialog,
        SuccessDialog
    },
    data() {
        return{
          proceedDialog: false,
            successDialog: false,
            valid: false,
            user: '',
            password: '',
            host: '',
            local: false,
            passwordRules: [
                v => !!v || 'Password is required',
                v => v.length >= 6 || 'Password must be at least 6 characters'
            ]
        };
    },
    methods: {
      submit(){
        this.proceedDialog = false
        var submitData = {
          user: this.user, 
          password: this.password,
          host: this.host
          }
        axios.post("http://127.0.0.1:5000/setup/server", submitData)
          .then((response) => {
            var details = response.data
            if(details != null){
              this.successDialog = true
              this.user = details.user
              this.password = details.password
              this.host = details.host
              this.local = details.local
            }
          })
      }
    },
    mounted: function(){
      axios.get("http://127.0.0.1:5000/setup/server")
      .then((response) => {
        var details = response.data
        if(details != null){
          this.user = details.user
          this.password = details.password
          this.host = details.host
          this.local = details.local
        }
      })
    }
}
</script>