<template>
  <v-dialog
      v-model="show"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          {{title}}
        </v-card-title>
        <v-card-text>{{message}}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="$emit('cancel')"
          >
            Cancel
          </v-btn>
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
    name: "ProceedDialog",
    props: {
        title: String,
        message: String,
        show: Boolean
    },
}
</script>