<template>
    <v-container class="align-center">
    <v-layout justify-center>
      <v-flex xs12 sm8 md5>
        <v-row>
          <v-col>
            <v-card class="elevation-7 px-10">
              <v-spacer></v-spacer>
              <div class="pt-10 pr-10 pl-10 pb-5">
                <h2>BNA USER</h2>
              </div>

              <v-card-text >
                <v-form ref="form" v-model="valid" lazy-validation>

                  <v-text-field
                    class="pb-5"
                    prepend-icon="person"
                    name="email"
                    label="User"
                    type="email"
                    v-model="email"
                    :rules="emailRules"
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
      </v-flex>
    </v-layout>
    <proceed-dialog
      title="BNA Details"
      message="Do you want to update the BNA account details?"
      v-bind:show="proceedDialog"
      v-on:cancel="proceedDialog = false"
      v-on:ok="submit"></proceed-dialog>
     <success-dialog
      title="BNA details"
      message="Details updated"
      v-bind:show="successDialog"
      v-on:ok="successDialog = false"></success-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
import ProceedDialog from '../components/ProceedDialog.vue';
import SuccessDialog from '../components/SuccessDialog.vue';
export default {
    name: 'BNAUser',
    components: {
      ProceedDialog,
        SuccessDialog
    },
    data() {
         return{
            valid: false,
            proceedDialog: false,
            successDialog: false,
            email: '',
            password: '',
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+/.test(v) || 'E-mail must ve valid'
            ],
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
          user: this.email, 
          password: this.password
          }
        axios.post("http://127.0.0.1:5000/setup/bna", submitData)
          .then((response) => {
            var details = response.data
            if(details != null){
              this.email = details.username
              this.password = details.password
              this.successDialog = true
            }
          })
      }
    },
    mounted: function(){
      axios.get("http://127.0.0.1:5000/setup/bna")
      .then((response) => {
        var details = response.data
        if(details != null){
          this.email = details.username
          this.password = details.password
        }
      })
    }
};
</script>