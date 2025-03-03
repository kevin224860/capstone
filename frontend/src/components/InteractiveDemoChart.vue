<template>
    <div class="interactive-demo">
      <canvas ref="chart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js'
  
  export default {
    mounted() {
      Chart.register(...registerables)
      new Chart(this.$refs.chart, {
        type: 'bar',
        data: {
          labels: ['Bullish', 'Bearish', 'Neutral'],
          datasets: [{
            label: 'Prediction Confidence',
            data: [75, 20, 5],
            backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
          }]
        }
      })
    }
  }
  </script>
  
  <style>
  .interactive-demo {
    height: 400px;
  }
  </style>