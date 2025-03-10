<template>
  <div class="preview-chart-container">
    <div class="preview-chart">
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
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
          label: 'Stock Price',
          data: [150, 165, 155, 170, 185],
          borderColor: '#2196F3',
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 3,
          pointHoverRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              padding: 20
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              maxRotation: 0,
              autoSkipPadding: 20
            }
          },
          y: {
            beginAtZero: false,
            grid: {
              color: '#e0e0e0'
            }
          }
        }
      }
    })
  }
}
</script>

<style scoped>
.preview-chart-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
}

.preview-chart {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 12px;
}

@media (max-width: 768px) {
  .preview-chart-container {
    padding-top: 75%; /* 4:3 Aspect Ratio for mobile */
  }
}
</style>