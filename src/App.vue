<template>
  <v-app>
    <v-app-bar
      app
      dark
      color="teal darken-4"  
    >
    <a href="https://prra.dev">
    <v-img
          alt="PRRA Logo"
          class="shrink mr-2"
          contain
          src='https://res.cloudinary.com/prra/image/upload/c_scale,w_500/v1587654993/PRRA.site/logo.prra_sxtsgv.png'
          transition="scale-transition"
          width="157"
        />
      </a>
    <v-spacer></v-spacer>
    </v-app-bar>
    <v-main>
      <NameProject/>
      <Footer/>
    </v-main>
  </v-app>
</template>

<script>
import NameProject from './components/NameProject';
import Footer from './components/Footer'

export default {
  name: 'App',

  components: {
    NameProject,
    Footer
  },

  data: () => ({
    
  }),
};
</script>
