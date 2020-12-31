<template>
  <div class="hello">
    <div>
        <h1>{{ msg }}</h1>
      <div v-for='result in basic_results' :key='result.id'>
        <h3>Post id: {{result.id}}</h3>
        <h3>Post Title:  {{result.title}}</h3>
        <h3>Post Body: {{result.body}}</h3>
        <h3>Post userId: {{result.userId}}</h3>
        <v-divider></v-divider>
      </div>
      <h2>Essential Links</h2>
    </div>

    <div>
      
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  name: 'myStore',
  data () {
    return {
      msg: 'Welcome to my Vuex Store'
    }
  },
  computed: mapState ([
    'basic_results'
  ]),
  mounted() {
    this.$store.dispatch('loadBasicResults');
  }
}
</script>

