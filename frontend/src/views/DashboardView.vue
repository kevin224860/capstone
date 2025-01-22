<template>
    <div class="dashboard-container">
      <h1>Welcome to your Dashboard</h1>
    </div>
  </template>
  
  <script>
  export default {
    name: "DashboardView",
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Full screen height */
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
  }
  
  h1 {
    font-size: 3rem;
    color: #333;
  }
  </style>
  