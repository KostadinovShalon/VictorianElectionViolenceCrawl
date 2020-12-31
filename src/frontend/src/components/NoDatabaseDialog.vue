<template>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="400"
    >
      <v-card dark color="#ffffff">
        <v-card-title class="headline red">
          No Database Configuration
        </v-card-title>
        <v-card-text class="mt-5 black--text">Database is not configured (neither remote or local). No actions are allowed until database configuration.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            href="/"
          >
            Dashboard
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            href="/database-conn"
          >
            Config DB
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';
export default {
  name: 'NoDatabaseDialog',
  data(){
      return{
          dialog: false
      }
  },
  computed: {

    commonurl(){
            return this.$store.state.commonurl
        }
  },
  methods: {
      getDBConfiguration(){
        axios.get(this.commonurl + "setup/db")
        .then((response) => {
            var details = response.data
            const local = details.local
            if(local){
                this.dialog = details.data_dir === null
            } else {
                this.dialog = details.password === null || details.user === null || details.host === null
            }
        })
    },
  },
  mounted (){
      this.getDBConfiguration()
  }
};
</script>