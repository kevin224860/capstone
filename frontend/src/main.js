import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";

createApp(App).use(router).mount('#app')

axios.interceptors.response.use(
    (response) => response, // If the response is successful, return it
    (error) => {
      if (error.response && error.response.status === 401) {
        // If the backend returns 401 Unauthorized
        localStorage.removeItem("token"); // Clear token from localStorage
        delete axios.defaults.headers.common["Authorization"]; // Remove the header
        router.push("//login"); // Redirect to login page
      }
      return Promise.reject(error);
    }
  );