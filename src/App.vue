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
    <v-tooltip bottom>
       <template v-slot:activator="{ on, attrs }">
       <v-btn 
       @click="dialog = true"
       icon 
       color="white"
        v-bind="attrs"
          v-on="on">
      <v-icon>mdi-information</v-icon>
    </v-btn>
       </template>
    <span>De onde são esses dados?</span>
    </v-tooltip>
    </v-app-bar>
    <v-dialog
      v-model="dialog"
      max-width="350"
    >
      <v-card>
        <v-card-title class="headline">Dados originais do IBGE</v-card-title>

        <v-card-text>
Este projeto utiliza dados dos serviços oficiais do IBGE localizados na página <a target="_blank" href="https://servicodados.ibge.gov.br/api/docs">https://servicodados.ibge.gov.br/api/docs</a>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
    dialog:false,
  }),
};
</script>
