<template>
  <div class="home">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="brand">
        <v-icon color="primary">mdi-chart-areaspline</v-icon>
        <span>Round Trade AI</span>
      </div>
      <div class="auth-buttons">
  <v-btn text color="primary" @click="$router.push('/login')">Login</v-btn>
  <v-btn color="primary" @click="$router.push('/signup')">Register</v-btn>
</div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-text">
          <h1>Smart Stock Predictions Powered by AI</h1>
          <p class="subheading">Harness machine learning to make informed investment decisions</p>
          <v-btn block large color="primary" @click="$router.push('/login')" class="cta-btn">
            Start Predicting Now
          </v-btn>
        </div>
        <div class="hero-chart">
          <PreviewChart />
        </div>
      </div>
    </section>

    <!-- Value Proposition Section -->
    <section class="value-props">
      <div class="prop-card">
        <v-icon large color="primary">mdi-artificial-intelligence</v-icon>
        <h3>Advanced AI Analysis</h3>
        <p>Our neural networks analyze historical data and market trends</p>
      </div>
      
      <div class="prop-card">
        <v-icon large color="primary">mdi-chart-timeline</v-icon>
        <h3>Real-time Predictions</h3>
        <p>Get up-to-date forecasts and market insights</p>
        <div class="mini-chart">
          <MiniSparkline />
        </div>
      </div>

      <div class="prop-card">
        <v-icon large color="primary">mdi-shield-alert</v-icon>
        <h3>Risk Evaluation</h3>
        <p>Understand potential risks with confidence scoring</p>
      </div>
    </section>

    <!-- Demo Preview Section -->
    <section class="demo-preview">
      <div class="demo-content">
        <h2>See Our Predictions in Action</h2>
        <div class="chart-container">
          <InteractiveDemoChart />
        </div>
        <p class="demo-text">Sample prediction for AAPL (Apple Inc.) - Next 30 Days</p>
      </div>
    </section>
  </div>
</template>

<script>
import PreviewChart from '@/components/PreviewChart.vue';
import MiniSparkline from '@/components/MiniSparkline.vue';
import InteractiveDemoChart from '@/components/InteractiveDemoChart.vue';

export default {
  name: 'HomeView',
  components: {
    PreviewChart,
    MiniSparkline,
    InteractiveDemoChart
  }
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #f8fafc;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 5%;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: relative;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.hero {
  padding: 2rem 5%;
  display: flex;
  align-items: center;
  min-height: auto;
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text {
  order: 2;
  width: 100%;
}

h1 {
  font-size: 2rem;
  line-height: 1.3;
  margin-bottom: 1rem;
  color: #1e293b;
}

.subheading {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 1.5rem;
}

.hero-chart {
  order: 1;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  width: 100%;
}

.value-props {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  padding: 2rem 5%;
  background: white;
}

.prop-card {
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.demo-preview {
  padding: 2rem 5%;
  background: #f8fafc;
}

.chart-container {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin: 1rem auto;
  width: 100%;
}

.cta-btn {
  margin-top: 1.5rem;
}

@media (min-width: 768px) {
  .navbar {
    padding: 1rem 5%;
  }

  .brand {
    font-size: 1.5rem;
  }

  .hero {
    min-height: 70vh;
    padding: 4rem 5%;
  }

  .hero-content {
    flex-direction: row;
    gap: 3rem;
  }

  .hero-text {
    order: 1;
    width: 50%;
  }

  .hero-chart {
    order: 2;
    width: 50%;
  }

  h1 {
    font-size: 3.5rem;
  }

  .subheading {
    font-size: 1.25rem;
  }

  .value-props {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    padding: 4rem 5%;
  }

  .chart-container {
    padding: 2rem;
    max-width: 800px;
  }
}

@media (max-width: 480px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .auth-buttons {
    width: 100%;
    justify-content: space-between;
  }

  .auth-buttons .v-btn {
    flex: 1;
  }

  h1 {
    font-size: 1.75rem;
  }
}
</style>