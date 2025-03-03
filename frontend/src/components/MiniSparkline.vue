<template>
    <div class="mini-sparkline">
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
          labels: ['Q1', 'Q2', 'Q3', 'Q4'],
          datasets: [{
            data: [12, 19, 3, 5],
            borderColor: '#4CAF50',
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          }
        }
      })
    }
  }
  </script>
  
  <style>
  .mini-sparkline {
    height: 100px;
  }
  </style>