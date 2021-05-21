<template>
  <div v-if="dataCheck">
    <apexchart height="350" type="candlestick" :options="chartOptions" :series="series"></apexchart>
    <div>
      <b-button variant="outline-primary" @click="updateChart">Update!</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

export default {
  name: "Rates",
  withCredentials: true,
  data() {
    return {
      dataCheck: false,
      series: [{
        data: [
          {
            x: new Date(1538778600000),
            y: [6629.81, 6650.5, 6623.04, 6633.33]
          },
          {
            x: new Date(1538780400000),
            y: [6632.01, 6643.59, 6620, 6630.11]
          },
          {
            x: new Date(1538782200000),
            y: [6630.71, 6648.95, 6623.34, 6635.65]
          },
        ]
      }],
      chartOptions: {
        chart: {
          type: 'candlestick',
          height: 350
        },
        title: {
          text: 'CandleStick Chart',
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
    axios({
      method: 'get',
      url: 'rate/'
    })
        .then((response) => {
          for (let i = 0; i < 10; i++) {
            //let x = new Date(response.data[i]['open_time']);
            //let y = [6630.71, 6648.95, 6623.34, 6635.65];
            //this.ohlcv.push(response.data[i]['open_time'], y);
            console.log(response);
          }
          console.log(this.series[0].data[0]['x']);
          //this.series[0].data.pop();
          this.dataCheck = true;
        })
        .catch(function (error) {
          console.log(error);
        });
  },
  methods: {
    updateChart() {
      const newData = [
        {
          x: new Date(1538778600000),
          y: [6629.81, 6650.5, 6623.04, 6633.33]
        },
        {
          x: new Date(1538780400000),
          y: [6632.01, 6643.59, 6620, 6630.11]
        },
      ]

      this.series = [{
        data: newData
      }]
    }
  }
}
</script>

<style scoped>

</style>