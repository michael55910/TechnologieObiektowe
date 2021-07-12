<template>
  <b-card no-body>
    <b-tabs card>
      <b-tab title="Kursy" active>
        <!--        <b-card-text>Tab contents 1</b-card-text>-->
        <Rates :pairs="pairs" :intervals="intervals"/>
      </b-tab>
      <b-tab title="Przewidywania">
        <Predictions :pairs="pairs" :intervals="intervals" :predictionModels="predictionModels"/>
      </b-tab>
      <b-tab title="Porównanie">
        <Comparison :pairs="pairs" :intervals="intervals"/>
      </b-tab>
      <b-tab title="Uczenie">
        <Learning :pairs="pairs" :intervals="intervals" :learning-methods="predictionMethods"
                  :predictionModels="predictionModels" v-on:prediction-models-update="getPredictionModels"/>
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Rates from "@/components/Rates";
import Comparison from "@/components/Comparison";
import Predictions from "@/components/Predictions";
import Learning from "@/components/Learning";
import DataService from "@/service/DataService";

export default {
  name: "Home",
  components: {Learning, Predictions, Comparison, Rates},
  data() {
    return {
      pairs: [],
      // intervals: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'],
      intervals: [],
      predictionMethods: [],
      predictionModels: []
    }
  },
  methods: {
    getPairs() {
      DataService.getAllPairs('TRADING')
          .then(response => {
            this.pairs = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getIntervals() {
      DataService.getIntervals()
          .then(response => {
            this.intervals = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getPredictionMethods() {
      DataService.getPredictionMethods()
          .then(response => {
            this.predictionMethods = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getPredictionModels() {
      DataService.getPredictionModels()
          .then(response => {
            this.predictionModels = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    }
  },
  created() {
    this.getPairs();
    this.getIntervals();
    this.getPredictionMethods();
    this.getPredictionModels();

  }
}
</script>

<style scoped>

</style>