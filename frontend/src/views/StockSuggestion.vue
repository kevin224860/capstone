<template>
  <div class="app-container">
    <AppNavbar />
    
    <div class="suggestion-page">
      <!-- Header -->
      <div class="header">
        <button class="back-button" @click="$router.push('/dashboard')">
          ← Back to Dashboard
        </button>
        <h1>AI Generated Suggestions</h1>
        <p class="subtitle">Analyzing your portfolio for optimal opportunities</p>
      </div>

      <!-- Analyzing State -->
      <div v-if="isLoading" class="analyzing-state">
        <div class="loader">
          <div class="pulse"></div>
          <div class="pulse-delay"></div>
        </div>
        <h3>Crunching the numbers...</h3>
        <p>Analyzing 1000+ market indicators for optimal picks</p>
      </div>

      <!-- Results Grid -->
      <div v-else class="results-grid">
        <div 
          v-for="(stock, index) in suggestions" 
          :key="index" 
          class="stock-card"
          :class="getCardClass(stock.rating)"
        >
          <div class="card-header">
            <div class="stock-info">
              <h3>{{ stock.name }}</h3>
              <span class="ticker">{{ stock.ticker }}</span>
            </div>
            <div class="industry-tag">
              {{ stock.industry }}
            </div>
          </div>

          <div class="card-body">
            <div class="rating">
              <div class="rating-badge">
                {{ stock.rating }}
              </div>
              <span class="confidence">
                Confidence: {{ stock.confidence }}%
              </span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill"
                :style="{ width: stock.confidence + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <p class="disclaimer">
        *Simulated data for demonstration. Actual AI integration in development.
      </p>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';

export default {
  components: {
    AppNavbar
  },
  data() {
    return {
      isLoading: true,
      suggestions: []
    };
  },
  mounted() {
    this.fetchAISuggestions();
  },
  methods: {
    async fetchAISuggestions() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.$router.push('/login');
          return;
        }

        const response = await fetch('http://localhost:5000/api/suggestions', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        });

        if (response.status === 401) {
          localStorage.removeItem('token');
          this.$router.push('/login');
          return;
        }

        if (!response.ok) throw new Error('Failed to fetch suggestions');
        
        const data = await response.json();
        this.suggestions = data.suggestions;
        this.isLoading = false;
        
      } catch (error) {
        console.error('Error:', error);
        this.suggestions = [
          {
            ticker: "AAPL",
            name: "Apple Inc.",
            industry: "Technology",
            rating: "Strong Buy",
            confidence: 92
          },
          {
            ticker: "TSLA",
            name: "Tesla Inc.",
            industry: "Automotive",
            rating: "Hold",
            confidence: 65
          },
          {
            ticker: "GOOGL",
            name: "Alphabet Inc.",
            industry: "Technology",
            rating: "Buy",
            confidence: 84
          }
        ];
        this.isLoading = false;
      }
    },
    getCardClass(rating) {
      return {
        'strong-buy': rating === 'Strong Buy',
        'buy': rating === 'Buy',
        'hold': rating === 'Hold'
      };
    }
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-top: 100px; /* Increased padding for navbar */
}

.suggestion-page {
  padding: 2rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
}

.back-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: absolute;
  left: 1.5rem;
  top: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #2563eb;
}

.back-button:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}
.header h1 {
  font-size: 2.2rem;
  color: #2c3e50;
  margin: 1.5rem 0 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* Analyzing State */
.analyzing-state {
  text-align: center;
  padding: 4rem 0;
}

.loader {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
}

.pulse, .pulse-delay {
  position: absolute;
  border: 4px solid #6366f1;
  border-radius: 50%;
  width: 100%;
  height: 100%;
  animation: pulse 1.5s ease-out infinite;
  opacity: 0;
}

.pulse-delay {
  animation-delay: -0.75s;
}

@keyframes pulse {
  0% { transform: scale(0); opacity: 1; }
  100% { transform: scale(1); opacity: 0; }
}

/* Results Grid */
.results-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  padding: 1rem 0;
}

.stock-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  border: 1px solid #eee;
}

.stock-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.stock-info h3 {
  margin: 0;
  font-size: 1.3rem;
  color: #2c3e50;
  line-height: 1.4;
}

.ticker {
  color: #7f8c8d;
  font-size: 0.9rem;
  display: block;
  margin-top: 0.25rem;
}

.industry-tag {
  background: #f1f5f9;
  color: #64748b;
  padding: 0.35rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.rating {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.rating-badge {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
}

.strong-buy .rating-badge { background: #10b98120; color: #10b981; }
.buy .rating-badge { background: #3b82f620; color: #3b82f6; }
.hold .rating-badge { background: #f59e0b20; color: #f59e0b; }

.confidence {
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
}

.progress-bar {
  background: #f1f5f9;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.strong-buy .progress-fill { background: #10b981; }
.buy .progress-fill { background: #3b82f6; }
.hold .progress-fill { background: #f59e0b; }

.disclaimer {
  text-align: center;
  color: #94a3b8;
  margin-top: 3rem;
  font-size: 0.9rem;
  padding: 2rem 0 0;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .app-container {
    padding-top: 80px;
  }

  .suggestion-page {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.8rem;
    margin-top: 2rem;
  }

  .back-button {
    position: relative;
    top: 0;
    margin-bottom: 1rem;
  }

  .stock-card {
    padding: 1.2rem;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.6rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}
</style>