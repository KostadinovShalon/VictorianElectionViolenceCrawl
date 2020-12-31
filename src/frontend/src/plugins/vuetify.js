import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#22AB00',
        secondary: '#1B5E20',
        accent: '#EDEDED',
        error: '#D32F2F'
      }
    }
  }
});
