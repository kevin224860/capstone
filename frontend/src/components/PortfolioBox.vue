<template>
    <div class="portfolio-box" v-if="portfolio.length > 0">
      <h2>Your Portfolio</h2>
  
      <!-- Desktop View -->
      <table v-if="!isMobile" class="desktop-view">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Industry</th>
            <th>Number</th>
            <th>Price (per share)</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in portfolio" :key="item.code">
            <td>{{ item.stock }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.number }}</td>
            <td>${{ item.price_per_share }}</td>
            <td>{{ formatDate(item.date) }}</td>
            <td>
                <div class="action-buttons">
                    <button class="edit-btn" @click="editStock(item)">Edit <i class="fa-regular fa-pen-to-square"></i></button>
                    <button class="delete-btn" @click="deleteStock(item.entry_ID)">Delete <i class="fa-solid fa-trash"></i></button>
                </div>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Mobile View -->
      <div class="mobile-view" v-if="isMobile">
        <div v-for="(item, index) in portfolio" :key="item.code" class="stock-card">
          <div class="stock-header" @click="toggleExpand(index)">
            <h3>{{ item.stock }}</h3>
            <i :class="expandedIndex === index ? 'fa-solid fa-angle-up' : 'fa-solid fa-angle-down'"></i>
          </div>
          <transition name="expand">
            <div v-if="expandedIndex === index" class="stock-details">
              <p><strong>Industry:</strong> {{ item.name }}</p>
              <p><strong>Number:</strong> {{ item.number }}</p>
              <p><strong>Price per share:</strong> ${{ item.price_per_share }}</p>
              <p><strong>Date:</strong> {{ formatDate(item.date) }}</p>
              <div class="button-group">
                <button class="edit-btn" @click="editStock(item)">Edit <i class="fa-regular fa-pen-to-square"></i></button>
                <button class="delete-btn" @click="deleteStock(item.entry_ID)">Delete <i class="fa-solid fa-trash"></i></button>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <EditComponent 
      :show="isModalVisible" 
      :stock="selectedStock"
      @close="isModalVisible = false"
    />
  </template>
  
  <script>
  import axios from "axios";
  import EditComponent from './EditComponent.vue';


  export default {
    components: { EditComponent },
    props: {
      portfolio: Array,
      isMobile: Boolean
    },
    data() {
      return {
        localPortfolio: [...this.portfolio],
        expandedIndex: null,
        isModalVisible: false,
        selectedStock: null
      };
    },
    methods: {
      toggleExpand(index) {
        this.expandedIndex = this.expandedIndex === index ? null : index;
      },

      formatDate(dateString) {
        
        const date = new Date(dateString);

        if(this.isMobile){
          const formatter = new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          });

          return formatter.format(date);
        }
        
        

        return new Intl.DateTimeFormat("en-US").format(date);
        
      },

      editStock(stock) {
        this.selectedStock = { ...stock }; // Clone stock to prevent direct modification
        this.isModalVisible = true;
        console.log(this.selectedStock);
      },

      // Send delete request to backend
      async deleteStock(stockId) {
        const confirmDelete = window.confirm("Are you sure you want to delete this stock?");
  
        if (!confirmDelete) {
          console.log("Stock deletion cancelled");
          return;
        }
        
        try {
          const token = localStorage.getItem("token");
          await axios.delete(`http://localhost:5000/api/portfolio/${stockId}`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          console.log(`Stock with ID: ${stockId} deleted`);

          // Refresh or fetch the updated portfolio
          window.location.reload();

        } catch (error) {
          console.error("Error deleting stock:", error);
        }
      }
    }
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
  width: 90%;
  max-width: 8000px;
  overflow-x: auto; 
  text-align: center;
  border: 2px solid black;
}

.portfolio-box h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 10px;
}


table {
  width: 100%;
  border-collapse: collapse; 
  margin-top: 10px;
  border: 2px solid black;
  border-radius: 10px;
}

.desktop-view table {
  width: 100%;  
  border-collapse: collapse; 
  margin-top: 10px;
}

.desktop-view th,
.desktop-view td {
  padding: 12px;
  text-align: left;
  width: auto;  
}

.desktop-view th:last-child,
.desktop-view td:last-child {
  white-space: nowrap; 
  width: 1%; 
}




.action-buttons {
  display: flex;
  justify-content: flex-start; 
  gap: 10px; 
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #007bff; 
  color: white;
  font-weight: bold;
}

tbody {
  border-radius: 100px;
}

tbody tr:nth-child(even) {
  background: #f2f2f2;
}

tbody tr:hover {
  background: #ddd;
}

th:first-child {
  border-top-left-radius: 8px;
}

th:last-child {
  border-top-right-radius: 8px;
}

tbody tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}

tbody tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
}
tbody tr:last-child td {
  border-bottom: none;
}


.action-buttons {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.edit-btn {
  background: #28a745;
  color: white;
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-btn:hover {
  background: #1a6b2d;
}

.delete-btn {
  background: #dc3545; 
  color: white;
  display: flex;
  align-items: center;
  gap: 5px;
}

.delete-btn:hover {
  background: #a32734;
}

.desktop-view {
  display: block;
}

.mobile-view {
  display: none;
}

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

.stock-details {
  text-align: left;
  padding: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

/* Expand Transition */
.expand-enter-active, .expand-leave-active {
  transition: max-height 0.3s ease-out, opacity 0.3s ease-in-out;
  overflow: hidden;
}

.expand-enter-from, .expand-leave-to {
  max-height: 0;
  opacity: 0;
}

.expand-enter-to, .expand-leave-from {
  max-height: 200px;
  opacity: 1;
}

@media (max-width: 790px) {
  .desktop-view {
    display: none;
  }
  .mobile-view {
    display: block;
  }
}


</style>
  