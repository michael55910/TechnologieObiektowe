<template>
  <div v-if="firstCheck">
    <apexchart height="350" type="candlestick" :options="chartOptions" :series="series"></apexchart>

    <b-form inline>
      <b-input-group prepend="Para kryptowalut: " class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedPairSymbol" :options="pairs" text-field="symbol" value-field="symbol"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Interwał" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedInterval" :options="intervals"></b-form-select>
      </b-input-group>

      <b-button variant="primary" @click="updateChart">Aktualizuj</b-button>
    </b-form>
  </div>
</template>

<script>
import DataService from "@/service/DataService";

export default {
  name: "Rates",
  withCredentials: true,
  data() {
    return {
      pageSize: 100,
      pairs: [],
      selectedPairSymbol: 'BNBBTC',
      intervals: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'],
      selectedInterval: '1m',
      dataLoading: true,
      firstCheck: false,
      series: [{
        data: []
      }],
      chartOptions: {
        chart: {
          type: 'candlestick',
          height: 350,
          animations:
              {
                enabled: false
              }
        },
        title: {
          text: 'Wykres świecowy',
          align: 'left'
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
    this.getPairs();
    this.updateChart();
  },
  methods: {
    updateChart() {
      this.dataLoading = true;
      DataService.getCandles(this.selectedPairSymbol, this.selectedInterval, true, undefined, this.pageSize, undefined)
          .then(response => {
            const newData = []
            for (let i = 0; i < response.data.results.length; i++) {
              let push_value = {};
              push_value.x = new Date(response.data.results[i]['open_time']);
              push_value.y = [response.data.results[i]['open'], response.data.results[i]['high'], response.data.results[i]['low'], response.data.results[i]['close']];
              newData.push(push_value);
            }
            this.series = [{
              data: newData
            }]
            this.dataLoading = false;
            this.firstCheck = true;
          })
          .catch(error => {
            console.log(error);
          });
    },
    getPairs() {
      DataService.getAllPairs('TRADING')
          .then(response => {
            this.pairs = response.data;
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