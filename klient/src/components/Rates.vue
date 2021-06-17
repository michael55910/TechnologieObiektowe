<template>
  <div v-if="firstCheck">
    <apexchart height="350" type="candlestick" :options="chartOptions" :series="series"></apexchart>

    <b-form inline>
      <b-input-group prepend="Pierwsza kryptowaluta" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="first_crypto_selection" :options="first_crypto_options"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Druga kryptowaluta" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="second_crypto_selection" :options="second_crypto_options"></b-form-select>
      </b-input-group>

      <b-input-group prepend="Okres czasu" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="period_selection" :options="period_options"></b-form-select>
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
      first_crypto_selection: 'BTC',
      first_crypto_options: [
        {value: 'BTC', text: 'Bitcoin'},
        {value: 'ETH', text: 'Ethereum'}
      ],
      second_crypto_selection: 'BTC',
      second_crypto_options: [
        {value: 'BTC', text: 'Bitcoin'},
        {value: 'ETH', text: 'Ethereum'}
      ],
      period_selection: 'BNBBTC',
      period_options: [
        {value: 'BNBBTC', text: 'Dzień'},
        {value: 'ETHBTC', text: 'Tydzień'},
        {value: 'ETHBTC', text: 'Miesiąc'},
        {value: 'ETHBTC', text: 'Rok'}
      ],
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
    this.updateChart();
  },
  methods: {
    updateChart() {
      this.dataLoading = true;
      DataService.getCandles('BNBBTC', '1m', true, undefined, this.pageSize, undefined)
          .then(response => {
            const newData = []
            for (let i = 0; i < this.pageSize; i++) {
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
    }
  }
}
</script>

<style scoped>

</style>