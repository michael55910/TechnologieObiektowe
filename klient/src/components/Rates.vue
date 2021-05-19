<template>
  <div id="chart-container">
    <fusioncharts
        :type="type"
        :width="width"
        :height="height"
        :dataFormat="dataFormat"
        :dataSource="dataSource"
    ></fusioncharts>
  </div>
</template>

<script>
import FusionCharts from "fusioncharts";
import Charts from "fusioncharts/fusioncharts.charts";
import FCComponent from "vue-fusioncharts";

Charts(FusionCharts);

const dataSource = {
  chart: {
    caption: "Bitcoin Price",
    subcaption: "Q4-2017",
    numberprefix: "$",
    pyaxisname: "Price (USD)",
    vyaxisname: "Volume traded",
    theme: "fusion",
    showvolumechart: "1",
    vnumberprefix: "$"
  },
  categories: [
    {
      category: [
        {
          label: "Oct",
          x: "1"
        },
        {
          label: "Nov",
          x: "32"
        },
        {
          label: "Dec",
          x: "62"
        }
      ]
    }
  ],
  dataset: [
    {
      data: [
        {
          tooltext:
              "<b>Oct 01, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4341.05,
          high: 4403.74,
          low: 4269.81,
          close: 4403.74,
          volume: 1208210000,
          x: 1
        },
        {
          tooltext:
              "<b>Oct 02, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4395.81,
          high: 4470.23,
          low: 4377.46,
          close: 4409.32,
          volume: 1431730000,
          x: 2
        },
        {
          tooltext:
              "<b>Oct 03, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4408.46,
          high: 4432.47,
          low: 4258.89,
          close: 4317.48,
          volume: 1288020000,
          x: 3
        },
        {
          tooltext:
              "<b>Oct 04, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4319.37,
          high: 4352.31,
          low: 4210.42,
          close: 4229.36,
          volume: 1116770000,
          x: 4
        },
        {
          tooltext:
              "<b>Oct 05, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4229.88,
          high: 4362.64,
          low: 4164.05,
          close: 4328.41,
          volume: 1161770000,
          x: 5
        },
        {
          tooltext:
              "<b>Oct 06, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4324.46,
          high: 4413.27,
          low: 4320.53,
          close: 4370.81,
          volume: 1069940000,
          x: 6
        },
        {
          tooltext:
              "<b>Oct 07, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4369.35,
          high: 4443.88,
          low: 4321.05,
          close: 4426.89,
          volume: 906928000,
          x: 7
        },
        {
          tooltext:
              "<b>Oct 08, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4429.67,
          high: 4624.14,
          low: 4405.64,
          close: 4610.48,
          volume: 1313870000,
          x: 8
        },
        {
          tooltext:
              "<b>Oct 09, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4614.52,
          high: 4878.71,
          low: 4564.25,
          close: 4772.02,
          volume: 1968740000,
          x: 9
        },
        {
          tooltext:
              "<b>Oct 10, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 4776.21,
          high: 4922.17,
          low: 4765.1,
          close: 4781.99,
          volume: 1597140000,
          x: 10
        },
        {
          tooltext:
              "<b>Dec 30, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 14681.9,
          high: 14681.9,
          low: 12350.1,
          close: 12952.2,
          volume: 14452600000,
          x: 91
        },
        {
          tooltext:
              "<b>Dec 31, 2017</b><br>Open: <b>$openDataValue</b><br>Close: <b>$closeDataValue</b><br>High: <b>$highDataValue</b><br>Low: <b>$lowDataValue</b><br>Volume: <b>$volumeDataValue</b>",
          open: 12897.7,
          high: 14377.4,
          low: 12755.6,
          close: 14156.4,
          volume: 12136300000,
          x: 92
        }
      ]
    }
  ]
};

export default {
  name: "Rates",
  components: {
    fusioncharts: FCComponent
  },
  data: () => ({
    type: "candlestick",
    width: "100%",
    height: "100%",
    dataFormat: "json",
    dataSource
  })
}
</script>

<style scoped>

</style>