<template>
    <v-card class="green lighten-4 elevation-5">
        <v-card-title class="justify-center">{{name}}</v-card-title>
        <v-card-text class="text-center text-h1">
            <animated-number
                :value="value"
                :round="1"
                :duration="300"
            />
        </v-card-text>
    </v-card>
</template>

<script>
import AnimatedNumber from "animated-number-vue";
export default {
    name: "DashboardStatistic",
    components: {
        AnimatedNumber
    },
    props: {
        name: String,
        value: Number
    }
}
</script>