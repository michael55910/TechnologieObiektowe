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

      <b-button variant="primary" @click="updateData">Aktualizuj</b-button>
    </b-form>
  </div>
</template>

<script>
import DataService from "@/service/DataService";

export default {
  name: "Comparison",
  props: {
    pairs: {
      type: Array,
      required: true
    },
    intervals: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      pageSize: 100,
      selectedPairSymbol: 'BNBBTC',
      selectedInterval: '1m',
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
      availablePredictions: []
    };
  },
  created() {
    // this.updateData();
  },
  methods: {
    updateLineChart() {
      this.dataLoading = true;
      DataService.getLineValues(this.selectedPairSymbol, this.selectedInterval, true, this.pageSize, undefined)
          .then(response => {
            const newData = []
            for (let i = 0; i < response.data.results.length; i++) {
              let push_value = {};
              push_value.x = new Date(response.data.results[i]['timestamp']);
              push_value.y = [response.data.results[i]['value']];
              newData.push(push_value);
            }
            this.series = [{
              name: 'Wartość rzeczywista',
              data: newData
            }]
            this.dataLoading = false;
            this.firstCheck = true;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getAvailablePredictions() {
      DataService.getPredictions(this.selectedPairSymbol, this.selectedInterval)
          .then(response => {
            this.availablePredictions = response.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    updateData() {
      this.updateLineChart();
      this.getAvailablePredictions();
    }
  }
}
</script>

<style scoped>

</style>