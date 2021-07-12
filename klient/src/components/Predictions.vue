<template>
  <div>
    <apexchart v-if="firstCheck" :options="chartOptions" :series="series"></apexchart>

    <b-form inline>
      <b-input-group prepend="Para kryptowalut" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedPairSymbol" :options="pairs" text-field="symbol"
                       value-field="symbol"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Interwał" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedInterval" :options="intervals"></b-form-select>
      </b-input-group>

      <b-button variant="primary" @click="getAvailablePredictions">Pobierz przewidywania</b-button>
    </b-form>

    <b-form class="mt-5" inline>
      <b-input-group prepend="Para kryptowalut" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedNewPairSymbol" :options="pairs" text-field="symbol"
                       value-field="symbol"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Interwał" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedNewInterval" :options="intervals"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Nauczony model" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedNewModel" :options="predictionModels" value-field="name"
                       text-field="name"></b-form-select>
      </b-input-group>

      <b-button variant="primary" @click="createNewPrediction">Oblicz nowe przewidywania</b-button>
    </b-form>
  </div>
</template>

<script>

import DataService from "@/service/DataService";

export default {
  name: "Predictions",
  props: {
    pairs: {
      type: Array,
      required: true
    },
    intervals: {
      type: Array,
      required: true
    },
    predictionModels: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      pageSize: 100,
      selectedPairSymbol: 'BNBBTC',
      selectedInterval: '1m',
      selectedNewPairSymbol: 'BNBBTC',
      selectedNewInterval: '1m',
      selectedNewModel: '',
      selectedPredictionId: undefined,
      dataLoading: false,
      firstCheck: false,
      series: [{
        data: []
      }],
      chartOptions: {
        chart: {
          type: 'line',
          height: 350,
          animations:
              {
                enabled: false
              }
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          tooltip: {
            enabled: true
          }
        }
      },
    };
  },
  created() {

  },
  methods: {
    getAvailablePredictions() {
      DataService.getPredictions(this.selectedPairSymbol, this.selectedInterval)
          .then(response => {
            this.availablePredictions = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    createNewPrediction() {
      console.log(this.predictionModels);
      console.log(this.selectedNewModel);
      DataService.createPrediction(this.selectedNewPairSymbol, this.selectedNewInterval, this.selectedNewModel)
          .then(response => {
            if (response.status === 200) {
              console.log("New prediction created successfully")
            }
          })
          .catch(error => {
            console.log(error);
          });
    },
    getPredictedData() {
      DataService.getPredictedData(this.selectedPredictionId)
          .then(response => {
            const newData = []
            for (let i = 0; i < response.data.results.length; i++) {
              let push_value = {};
              push_value.x = new Date(response.data.results[i]['timestamp']);
              push_value.y = [response.data.results[i]['value']];
              newData.push(push_value);
            }
            this.series = [{
              name: 'Przewidywanie',
              data: newData
            }]
            this.dataLoading = false;
            this.firstCheck = true;
          })
          .catch(error => {
            console.log(error);
          });
    }
  }

}

</script>

<style scoped>

</style>