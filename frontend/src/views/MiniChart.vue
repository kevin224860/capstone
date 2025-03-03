<template>
    <div>
      <Line :data="data" :options="options" />
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import { Chart, registerables } from 'chart.js'
  
  Chart.register(...registerables)
  
  export default {
    extends: Line,
    props: ['data'],
    data() {
      return {
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
          },
          scales: {
            x: { display: false },
            y: { display: false }
          }
        }
      }
    },
    mounted() {
      this.renderChart(this.data, this.options)
    }
  }
  </script>