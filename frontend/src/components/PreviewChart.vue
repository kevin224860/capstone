<template>
    <div class="preview-chart">
      <canvas ref="chart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js'
  
  export default {
    mounted() {
      Chart.register(...registerables)
      new Chart(this.$refs.chart, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
          datasets: [{
            label: 'Stock Price',
            data: [150, 165, 155, 170, 185],
            borderColor: '#2196F3',
            tension: 0.4
          }]
        }
      })
    }
  }
  </script>
  
  <style>
  .preview-chart {
    height: 300px;
  }
  </style>