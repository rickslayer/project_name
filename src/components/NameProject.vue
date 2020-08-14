<template>
  <v-container>
     
    <v-row class="text-center">
      <v-col cols="12">
        <h1 class="text-center display-1">Digite um nome e uma cidade para ver a frequência dos nascimentos por década</h1>
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
    
      <v-col cols="12" sm="6">
          <v-text-field
            label="Seu Nome"
            placeholder="digite seu primeiro nome"
            dense
            filled
            v-model="name"
            @change="getDataNames"
            @keyup="uppercaseName"
          ></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
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
          return-object
          dense
          filled
          @change="getSelected"
      ></v-autocomplete>
      </v-col>
      <v-col cols=12>
        <h1 class="text--secondary" v-show="showCounter">Total de nomes: {{counter}}</h1>
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
    ['#00c6ff', '#F0F', '#FF0'],
  ]
  export default {
    name: 'NameProject',

    data: () => ({
      width: 2,
      radius: 10,
      padding: 8,
      lineCap: 'round',
      gradient: gradients[0],
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
          text: "Período",
          align: 'start',
          sortable: false,
          value: 'periodo'
        },
        {
          text: "Frequência p/ década",
          value: 'frequencia'
        },
        {
          text: "Nome",
          value: "nome_pessoa"
        }
      ],
      names:[],
      showTable: false,
      descriptionLimit: 60,
      entries: [],
      isLoading: false,
      model: null,
      search: null,
      showAlert:false,
      nome_cidade: "",
      counter: 0,
      showCounter: false
      
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
      uppercaseName(e) {
       let letter = e.target.value
       this.name = letter.toUpperCase()
      },
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
              this.counter = 0
            for (let item of data.res) {
                var per = item.periodo
                per = per.replace(']', '')
                per = per.replace('[', '')
                per = per.replace('0[', '0')
                per = per.replace(',', ' ==========> ')
                this.counter += item.frequencia
                frequencias.push(item.frequencia)
                periodos.push(per)
                this.names.push({
                  "periodo": per,
                  "frequencia": item.frequencia,
                  "nome_pessoa": this.name
                })
              }
              this.value = frequencias
              this.labels = periodos
              this.showTable = true
              this.showCounter = true

            }else {
              this.showAlert = true
              this.nome_cidade = this.model ? this.model['nome']: ""
              this.value = []
              this.labels = []
              this.showTable = false
              this.entries=[]
              this.model=null
              this.showCounter = false
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
