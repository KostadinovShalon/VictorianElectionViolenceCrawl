<template>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="700"
    >
      <v-card>
        <v-app-bar color="primary" dark>
          <v-card-title class="headline" v-if="crawling">
          Crawling <span v-if="withOCR"> (With OCR) </span>
          </v-card-title>

          <v-card-title class="headline" v-if="finished">
          Crawling Completed<span v-if="withOCR"> (With OCR) </span>
          </v-card-title>
        </v-app-bar>

        <slot name="past-downloads"></slot>

        <v-divider class="mx-5 mb-5" v-if="crawling"></v-divider>

        <v-card-text class="text--primary px-5" v-if="crawling">
          <v-row class="px-5" style="text-align: left">
            <v-col class="pr-15">
              <slot name="current-crawling-text"></slot>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-text class="px-5" v-if="crawling">
          <v-progress-linear
          color="primary"
          height="25"
          slot="progress"
          v-model="currentProgress"
          striped
          rounded
          >
          <slot name="crawling-bar-text"></slot>
          </v-progress-linear>
        </v-card-text>

        <v-card-actions v-if="!finished">
          <v-spacer></v-spacer>
          <v-btn
            class="py-3"
            elevation="5"
            color="error"
            @click="$emit('cancel')"
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
            @click="$emit('ok')"
            outlined
          >
          <strong>
            Ok
          </strong>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
  name: 'CrawlingDialog',
  props:{
      dialog: Boolean,
      withOCR: Boolean,
      crawling: Boolean,
      finished: Boolean,
      currentProgress: Number
  }
}
</script>