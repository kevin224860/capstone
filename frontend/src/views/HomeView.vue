<template>
  <div class="home">

    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="brand">
        <v-icon color="primary">mdi-chart-areaspline</v-icon>
       <!-- <font-awesome-icon icon="fa-solid fa-money-bill-trend-up" />-->
        Round Trade AI
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
          <div class="cta-buttons">
            <v-btn x-large color="primary" @click="$router.push('/login')">
              Start Predicting Now
            </v-btn>
          </div>
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
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.hero {
  padding: 4rem 5%;
  display: flex;
  align-items: center;
  min-height: 70vh;
}
.auth-buttons {
  display: flex;
  gap: 16px; /* Adjust this value as needed */
}

/* OR if you need browser fallback */
.login-btn {
  margin-right: 16px !important;
}
.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text {
  max-width: 600px;
}

h1 {
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.subheading {
  font-size: 1.25rem;
  color: #64748b;
  margin-bottom: 2rem;
}

.hero-chart {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.value-props {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 4rem 5%;
  background: white;
}

.prop-card {
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  transition: transform 0.3s ease;
  border: 1px solid #e2e8f0;
}

.prop-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.mini-chart {
  height: 100px;
  margin-top: 1rem;
}

.demo-preview {
  padding: 4rem 5%;
  background: #f8fafc;
}

.chart-container {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  margin: 2rem auto;
  max-width: 800px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.demo-text {
  text-align: center;
  color: #64748b;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  .navbar {
    padding: 1rem;
  }
}
</style>