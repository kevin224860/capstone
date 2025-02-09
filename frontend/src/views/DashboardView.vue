<template>
  <div class="dashboard-container">
    <div class="content">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else>Welcome to your Dashboard</h1>

      <!-- Desktop View -->
      <div class="portfolio-box desktop-view" v-if="!isMobile && portfolio.length > 0">
        <h2>Your Portfolio</h2>
        <table>
          <thead>
            <tr>
              <th>Code</th>
              <th>Industry</th>
              <th>Number</th>
              <th>Price (per share)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in portfolio" :key="item.code">
              <td>{{ item.code }}</td>
              <td>{{ item.industry }}</td>
              <td>{{ item.number }}</td>
              <td>${{ item.price }}</td>
              <td>
                <button class="edit-btn">Edit</button>
                <button class="delete-btn">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mobile View -->
      <div class="portfolio-box mobile-view" v-if="isMobile && portfolio.length > 0">
        <h2>Your Portfolio</h2>
        <div v-for="(item, index) in portfolio" :key="item.code" class="stock-card">
          <div class="stock-header" @click="toggleExpand(index)">
            <h3>{{ item.code }}</h3>
            <i :class="expandedIndex === index ? 'fa-solid fa-angle-up' : 'fa-solid fa-angle-down'"></i>
          </div>
          
          <div v-if="expandedIndex === index" class="stock-details">
            <p><strong>Industry:</strong> {{ item.industry }}</p>
            <p><strong>Number:</strong> {{ item.number }}</p>
            <p><strong>Price per share:</strong> ${{ item.price }}</p>
            <div class="button-group">
              <button class="edit-btn">Edit</button>
              <button class="delete-btn">Delete</button>
            </div>
          </div>
        </div>
      </div>
      <button class="add-stock-btn">Add New Stock</button>

      
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DashboardView",
  data() {
    return {
      firstName: "",
      portfolio: [],
      expandedIndex: null,
      isMobile: window.innerWidth <= 768,
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
    async getPortfolio() {
      try {
        const path = `${process.env.VUE_APP_URL}${process.env.VUE_APP_PORTFOLIO}`;
        const res = await axios.get(path, { withCredentials: true });
        this.portfolio = res.data.portfolio || res.data; 
      } catch (err) {
        console.error("Error fetching portfolio:", err);
      }
    },

    toggleExpand(index) {
      this.expandedIndex = this.expandedIndex === index ? null : index;
    },

    updateScreenSize() {
      this.isMobile = window.innerWidth <= 768; 
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
  height: 100vh;
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  padding: 20px;
}

.content {
  text-align: center;
  width: 100%;
  max-width: 800px;
}

.portfolio-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  width: 90%;
  max-width: 600px;
  text-align: center;
}


.desktop-view {
  display: block;
}

.mobile-view {
  display: none;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
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

tbody tr:nth-child(even) {
  background: #f2f2f2;
}

tbody tr:hover {
  background: #ddd;
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

.delete-btn {
  background: #dc3545;
  color: white;
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

@media (max-width: 768px) {
  .desktop-view {
    display: none;
  }
  .mobile-view {
    display: block;
  }
}
</style>
