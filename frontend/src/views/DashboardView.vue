<template>
  <div class="app-container">
    <AppNavbar />
    
    <div class="dashboard-content">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else class="error">ERROR: Cannot connect to account</h1>

      <PortfolioBox :portfolio="portfolio" :isMobile="isMobile" />

      <div class="action-buttons">
        <button class="action-btn stock-btn" @click="documentStock">
          <i class="fas fa-plus"></i>
          Document Stock
        </button>
        <button class="action-btn suggestion-btn" @click="generateSuggestions">
          <i class="fas fa-bolt"></i>
          Get Suggestions
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AppNavbar from "@/components/AppNavbar.vue";
import PortfolioBox from "@/components/PortfolioBox.vue";

export default {
  name: "DashboardView",
  components: {
    AppNavbar,
    PortfolioBox
  },
  data() {
    return {
      firstName: "",
      portfolio: [],
      isMobile: window.innerWidth <= 790,
    };
  },
  async created() {
    window.addEventListener("resize", this.updateScreenSize);
    this.updateScreenSize();

    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
      return;
    }

    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    try {
      const response = await axios.get(`${process.env.VUE_APP_URL}${process.env.VUE_APP_DASHBOARD}`, {
        withCredentials: true
      });
      this.firstName = response.data.first_name;
      this.getPortfolio();
    } catch (error) {
      this.$router.push("/login");
    }
  },
  methods: {
    async getPortfolio() {
      try {
        const path = `${process.env.VUE_APP_URL}${process.env.VUE_APP_PORTFOLIO}`;
        const res = await axios.get(path, { withCredentials: true });
        this.portfolio = res.data.portfolio || res.data;
      } catch (err) {
        console.error("Error fetching portfolio:", err);
      }
    },
    updateScreenSize() {
      this.isMobile = window.innerWidth <= 790;
    },
    documentStock() {
      // Add document stock logic
    },
    generateSuggestions() {
      this.$router.push('/suggestions');
    }
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.updateScreenSize);
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-content {
  max-width: 1200px;
  margin: 80px auto 0;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.error {
  color: #dc3545;
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.action-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-btn {
  background-color: #007bff;
  color: white;
}

.suggestion-btn {
  background-color: #28a745;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 790px) {
  .dashboard-content {
    padding: 15px;
    margin-top: 70px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>