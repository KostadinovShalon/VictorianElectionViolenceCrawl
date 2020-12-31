<template>

<v-navigation-drawer
  :clipped="true"
  permanent
  class="green darken-1 font-weight-bold"
  enable-resize-watcher app
>
  
  <v-list
    dense
    nav
    dark
  >
    <v-list-item
      v-for="tab in tabs"
      :key="tab.id"
      :to="tab.route"
    >
      <v-list-item-icon v-if="tab.name!=='spacer'">
        <v-icon>{{ tab.icon }}</v-icon>
      </v-list-item-icon>

      <v-list-item-content v-if="tab.name!=='spacer'">
        <v-list-item-title v-text="tab.name"></v-list-item-title>
      </v-list-item-content>
      <v-divider v-else></v-divider>
    </v-list-item>
    <v-list-group no-action prepend-icon="mdi-cog" active-class="white--text">
        <template v-slot:activator>
          <v-list-item-title>Configuration</v-list-item-title>
        </template>
        <v-list-item :key="11" to="/bna-user" active-class="white--text"><v-list-item-title>BNA</v-list-item-title></v-list-item>
        <v-list-item :key="12" to="/database-conn" active-class="white--text"><v-list-item-title>Database</v-list-item-title></v-list-item>
        <v-list-item :key="13" to="/server-variables" active-class="white--text"><v-list-item-title>Storage</v-list-item-title></v-list-item>
    </v-list-group>
  </v-list>
</v-navigation-drawer>
</template>

<script>
export default {
  name: 'AppNavigation',
  data() {
    return {
      appTitle: 'Web Crawler',
      tabs: [
        { id: '0', name: 'Dashboard', route: '/', icon: 'mdi-view-dashboard'},
        { id: '1', name: 'spacer'},
        { id: '2', name: 'Basic Search', route: '/search', icon: "mdi-magnify"},
        { id: '3', name: 'Advanced Search', route: '/advanced-search', icon: "mdi-briefcase-search"},
        { id: '4', name: 'Search Results', route: '/search-results', icon: "mdi-text-box-search"},
        { id: '5', name: 'Search Count Results', route: '/search-count-results', icon: null},
        { id: '6', name: 'spacer'},
        { id: '7', name: 'Candidates', route: '/candidates', icon: "mdi-text-box-plus"},
        { id: '8', name: 'Portal Documents', route: '/portal', icon: "mdi-text-box-check"},
        { id: '9', name: 'spacer'}
      ]
    };
  }
};
</script>