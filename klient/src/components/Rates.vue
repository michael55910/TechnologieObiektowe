<template>
  <div v-if="dataCheck">
    <apexchart height="350" type="candlestick" :options="chartOptions" :series="series"></apexchart>
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
        data: []
      }],
      chartOptions: {
        chart: {
          type: 'candlestick',
          height: 350
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
    axios({
      method: 'get',
      url: 'candle/'
    })
        .then((response) => {
          const newData = []
          for (let i = 0; i < response.data.length; i++) {
            let push_value = {};
            push_value.x = new Date(response.data[i]['open_time']);
            push_value.y = [response.data[i]['open'], response.data[i]['high'], response.data[i]['low'], response.data[i]['close']];
            newData.push(push_value);
          }
          this.series = [{
            data: newData
          }]
          this.dataCheck = true;
        })
        .catch(function (error) {
          console.log(error);
        });
  }
}
</script>

<style scoped>

</style>