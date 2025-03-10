<template>
  <div class="interactive-demo-container">
    <div class="interactive-demo">
      <canvas ref="chart"></canvas>
    </div>
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
          backgroundColor: ['#4CAF50', '#F44336', '#FFC107'],
          borderWidth: 0,
          borderRadius: 4,
          barThickness: 'flex',
          maxBarThickness: 40
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'x',
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: '#e0e0e0'
            },
            ticks: {
              callback: function(value) {
                return value + '%'
              }
            }
          }
        }
      }
    })
  }
}
</script>

<style scoped>
.interactive-demo-container {
  position: relative;
  width: 100%;
  padding-top: 60%; /* Custom Aspect Ratio */
}

.interactive-demo {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 10px;
}

@media (max-width: 768px) {
  .interactive-demo-container {
    padding-top: 80%; /* Taller aspect ratio for mobile */
  }
  
  .interactive-demo {
    padding: 5px;
  }
}
</style>