<template>
  <v-dialog
      v-model="show"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline white--text green">
          {{title}}
        </v-card-title>
        <v-card-text class="mt-5">{{message}}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="$emit('ok')"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: "SuccessDialog",
    props: {
        title: String,
        message: String,
        show: Boolean
    },
}
</script>