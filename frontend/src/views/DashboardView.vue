<template>
  <div class="dashboard-container">
    <div class="content">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else>ERROR Cannot connect to account</h1>

      <PortfolioBox :portfolio="portfolio" :isMobile="isMobile" />

      <div class="options">
        <button class="add-stock-btn"  @click="toggleAddStockModal">Document Stock <i class="fa-solid fa-plus"> </i></button>
        <button class="generate-suggestion-btn">Get Suggestions <i class="fa-solid fa-bolt"> </i></button>
      </div>
    </div>
  </div>
  
  <AddStockComponent :show="showAddStockModal" @close="showAddStockModal = false" @stock-added="refreshStocks" />
</template>

<script>
import axios from "axios";
import PortfolioBox from "@/components/PortfolioBox.vue";
import AddStockComponent from "@/components/AddStockComponent.vue";


export default {
  name: "DashboardView",
  components: {
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
      console.warn("No token found, redirecting to login...");
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
      console.warn("Session expired or unauthorized. Redirecting to login.");
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
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.updateScreenSize);
  },
};
</script>
<style scoped>

.dashboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Arial, sans-serif;
  padding: 20px;
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
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-right: 5px;
}

.edit-btn {
  background: #28a745;
  color: white;
}

.edit-btn:hover {
  background: #1a6b2d;
  color: white;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #a32734;
  color: white;
}

.options {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  gap: 25px;
}
.add-stock-btn {
  display: block;
  margin: 20px auto;
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 16px;
}

.add-stock-btn:hover {
  background: #0056b3;
}

.generate-suggestion-btn{
  display: block;
  margin: 20px auto;
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 16px;
}

.generate-suggestion-btn:hover{
  background: #0056b3;
}

@media (max-width: 790px) {
  .desktop-view {
    display: none;
  }
  .mobile-view {
    display: block;
  }
}

/* Expand transition */
.expand-enter-active, .expand-leave-active {
  transition: max-height 0.3s ease-out, opacity 0.3s ease-in-out;
  overflow: hidden;
}

.expand-enter-from, .expand-leave-to {
  max-height: 0;
  opacity: 0;
}

.expand-enter-to, .expand-leave-from {
  max-height: 200px; /* Adjust this based on content height */
  opacity: 1;
}

</style>
