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
            <td>{{ item[0] }}</td>
            <td>{{ item[1] }}</td>
            <td>{{ item[2] }}</td>
            <td>${{ item[3] }}</td>
            <td>{{ formatDate(item[4]) }}</td>
            <td>
                <div class="action-buttons">
                    <button class="edit-btn">Edit <i class="fa-regular fa-pen-to-square"></i></button>
                    <button class="delete-btn">Delete <i class="fa-solid fa-trash"></i></button>
                </div>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Mobile View -->
      <div class="mobile-view" v-if="isMobile">
        <div v-for="(item, index) in portfolio" :key="item.code" class="stock-card">
          <div class="stock-header" @click="toggleExpand(index)">
            <h3>{{ item[0] }}</h3>
            <i :class="expandedIndex === index ? 'fa-solid fa-angle-up' : 'fa-solid fa-angle-down'"></i>
          </div>
          <transition name="expand">
            <div v-if="expandedIndex === index" class="stock-details">
              <p><strong>Industry:</strong> {{ item[1] }}</p>
              <p><strong>Number:</strong> {{ item[2] }}</p>
              <p><strong>Price per share:</strong> ${{ item[3] }}</p>
              <p><strong>Date:</strong> {{ formatDate(item[4]) }}</p>
              <div class="button-group">
                <button class="edit-btn">Edit <i class="fa-regular fa-pen-to-square"></i></button>
                <button class="delete-btn">Delete <i class="fa-solid fa-trash"></i></button>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    
    props: {
      portfolio: Array,
      isMobile: Boolean
    },
    data() {
      return {
        expandedIndex: null
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
  