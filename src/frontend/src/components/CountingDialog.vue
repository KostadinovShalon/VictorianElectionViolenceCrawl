<template>
<v-dialog
    v-model="dialog"
    persistent
    max-width="600">
    <v-card>
        <v-app-bar color="primary" dark>
            <v-card-title class="headline" v-if="counting">
            Counting
            </v-card-title>
            <v-card-title class="headline" v-if="finished">
            Counting completed
            </v-card-title>
        </v-app-bar>
        <slot></slot>

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
        <v-card-actions v-else>
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
    name: "CountingDialog",
    props: {
        dialog: Boolean,
        counting: Boolean,
        finished: Boolean
    }
}
</script>