<template>
  <div class="app-container">
    <AppNavbar />
    
    <div class="dashboard-content">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else class="error">ERROR: Cannot connect to account</h1>

      <PortfolioBox :portfolio="portfolio" :isMobile="isMobile" />

      <div class="action-buttons">
        <button class="action-btn stock-btn" @click="toggleAddStockModal">
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
  
  <AddStockComponent :show="showAddStockModal" @close="showAddStockModal = false" @stock-added="refreshStocks" />
</template>

<script>
import axios from "axios";
import AppNavbar from "@/components/AppNavbar.vue";
import PortfolioBox from "@/components/PortfolioBox.vue";
import AddStockComponent from "@/components/AddStockComponent.vue";


export default {
  name: "DashboardView",
  components: {
    AppNavbar,
    PortfolioBox,
    AddStockComponent
  },
  data() {
    return {
      firstName: "",
      portfolio: [],
      isMobile: window.innerWidth <= 790,
      showModal: false,
      industries: [],
      stock: { 
        symbol: "",
        industry: null,
        number: null,
        price_per_share: "",
        date: "",
      },
      showAddStockModal: false,
      errors: {}
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
    toggleAddStockModal() {
    this.showAddStockModal = !this.showAddStockModal;
  },
  async refreshStocks() {
    await this.fetchStocks(); // Refresh the stock list
  },
  
    async fetchIndustries(){
      try{
        const response = await axios.get(`${process.env.VUE_APP_URL}${process.env.VUE_APP_INDUSTRIES}`);
        this.industries = response.data.industries.map(industry => ({
          id: industry[0], 
          name: industry[1]
        }));

      }catch (error) {
        console.error("Error fetching industries:", error);
      }
    },
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
}
.content {
  text-align: center;
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}


.portfolio-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  width: 100%;
  max-width: 800px;
  text-align: center;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

.desktop-view {
  display: block;
}

.mobile-view {
  display: none;
}

table {
  width: 100%;
  border-collapse: separate;
  margin-top: 10px;
  border: 2px solid black;
  border-radius: 10px;
  border-spacing: 0;
}

th:first-child {
  border-top-left-radius: 8px;
}

th:last-child {
  border-top-right-radius: 8px;
}

tbody tr:last-child td:first-child {
  border-bottom-left-radius: 10px;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #007bff;
  color: white;
}



/* Stock Card Styling for Mobile */
.stock-card {
  background: #ffffff;
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stock-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  font-size: 1.2rem;
  font-weight: bold;
  background: #007bff;
  color: white;
  border-radius: 6px;
}

.expand-icon {
  font-size: 1.5rem;
}

.stock-details {
  text-align: left;
  padding: 10px;
}

.button-group {
  margin-top: 10px;
}

button {
  padding: 8px 12px;
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