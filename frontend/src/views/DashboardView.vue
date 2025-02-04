<template>
    <div class="dashboard-container">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else>Welcome to your Dashboard</h1>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    name: "DashboardView",
  data() {
    return {
      firstName: "",
    };
  },
  
  // method to run once the user attemps to go to the dashboard route
  async created() {
    // get the token out of local storage
    const token = localStorage.getItem("token"); 

    // if token is null go to the login page
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

      } catch (error) {
        // go back to login page because unauthorised access 
        console.warn("Session expired or unauthorized. Redirecting to login.");
        this.$router.push("/login");  
      }
    },
    methods: {
      
    },
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
  