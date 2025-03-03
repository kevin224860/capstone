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
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      }
    },
    mounted() {
      this.renderChart(this.data, this.options)
    }
  }
  </script>