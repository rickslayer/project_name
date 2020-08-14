<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <h1 class="text-center display-1">Digite seu nome e a cidade e veja a frequência de nascimentos em cada década</h1>
      </v-col>
      <v-col cols=12>
        <v-alert 
          v-show="showAlert" 
          type="error" 
          class="text-uppercase"
          :dismissible=true>
           Não houve nenhum registro do nome {{this.name}} na cidade {{nome_cidade}}.
        </v-alert>
      </v-col>
      <v-col cols="6">
          <v-text-field
            label="Digite seu nome aqui"
            single-line
            v-model="name"
            @change="getDataNames"
          ></v-text-field>
      </v-col>
      <v-col cols="6">
         <v-autocomplete
          v-model="model"
          :items="items"
          :loading="isLoading"
          :search-input.sync="search"
          color="white"
          hide-no-data
          hide-selected
          item-text="Description"
          item-value="id"
          label="Sua Cidade"
          placeholder="Comece a digitar para pesquisar"
          prepend-icon="mdi-database-search"
          return-object
          @change="getSelected"
      ></v-autocomplete>
      </v-col>
      <v-col cols="12">
        <v-sparkline
            labelSize="4"
            :labels="value"
            :value="value"
            :gradient="gradient"
            :smooth="radius || false"
            :padding="padding"
            :line-width="width"
            :stroke-linecap="lineCap"
            :gradient-direction="gradientDirection"
            :fill=false
            :type="type"
            :auto-line-width="autoLineWidth"
             auto-draw
          >
          </v-sparkline>
      </v-col>
      <v-col cols="12">
        <v-data-table
            v-show="showTable"
            :headers="headers"
            :footer=false
            :items="names"
            :items-per-page="10"
            class="elevation-1"
          ></v-data-table>
      </v-col>
    

    </v-row>
  </v-container>
</template>

<script>
const axios = require('axios')

 const gradients = [
    ['#222'],
    ['#42b3f4'],
    ['red', 'orange', 'yellow'],
    ['purple', 'violet'],
    ['#00c6ff', '#F0F', '#FF0'],
    ['#f72047', '#ffd200', '#1feaea'],
  ]
  export default {
    name: 'NameProject',

    data: () => ({
      width: 2,
      radius: 10,
      padding: 8,
      lineCap: 'round',
      gradient: gradients[4],
      value: [],
      labels: [],
      gradientDirection: 'top',
      gradients,
      fill: 'fill',
      type: 'trend',
      autoLineWidth: false,
      name:"",
      headers: [
        {
          text: "Período de 10 em 10 anos",
          align: 'start',
          sortable: false,
          value: 'periodo'

        },
        {
          text: "Frequência dos nomes por década",
          value: 'frequencia'

        },

      ],
      names:[],
      showTable: false,
      descriptionLimit: 60,
      entries: [],
      isLoading: false,
      model: null,
      search: null,
      showAlert:false,
      nome_cidade: ""
    }),
    computed: {
      fields () {
        if (!this.model) return []
        return Object.keys(this.model).map(key => {
          return {
            key,
            value: this.model[key] || 'n/a',
          }
        })
      },
      items () {
        if (!this.entries) return []
        return this.entries.map(entry => {
          const Description = entry.nome.length > this.descriptionLimit
            ? entry.nome.slice(0, this.descriptionLimit) + '...'
            : entry.nome

          const id = entry.id
          return Object.assign({}, entry, { Description , id})
        })
      },
    },

    methods: {
      getDataNames() {
         let name = this.name
         if (name.length > 0){
          name = name.toUpperCase()
          name = name.replace(/\s/g,'') //Replace all whitespaces globally
          let cidade = ""
          if(this.model) {
            cidade = this.model ? "?localidade="+this.model['id'] : ""
          }
          axios.get(`${process.env.VUE_APP_URL_API_NOMES}/${name}${cidade}`)
          .then((response) => {
            if (response.data.length > 0){
              let data = response.data[0]
              let periodos = []
              let frequencias = []
              this.names = []
            for (let item of data.res) {
                var per = item.periodo
                per = per.replace(']', '')
                per = per.replace('[', '')
                per = per.replace('0[', '0')
                per = per.replace(',', ' ==========> ')
                
                frequencias.push(item.frequencia)
                periodos.push(per)
                this.names.push({
                  "periodo": per,
                  "frequencia": item.frequencia
                })
              }
              this.value = frequencias
              this.labels = periodos
              this.showTable = true

            }else {
              this.showAlert = true
              this.nome_cidade = this.model ? this.model['nome']: ""
              this.value = []
              this.labels = []
              this.showTable = false
              this.entries=[]
              this.model=null
              setTimeout(()=>{
                this.showAlert=false
              },6500)
            }
          })
         .catch((error) => {
            console.log(error)
            alert(error)
          })
         }
         
      },
      getSelected(){
        this.getDataNames()
      }

    },
    mounted(){
    
    },
    watch: {
      search () {
        if (this.items.length > 0) return
        if (this.isLoading) return
        this.isLoading = true

        fetch(`${process.env.VUE_APP_URL_API_CIDADES}`)
          .then(res => res.json())
          .then(res => {
            const { count } = res
            this.count = count
            this.entries = res
          })
          .catch(err => {
            console.log(err)
          })
          .finally(() => (this.isLoading = false))
      },
    },

   


  }
</script>
