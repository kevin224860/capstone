<template>
    <div class="signup-container">
      <h1>Sign Up</h1>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            v-model="firstName"
            placeholder="Enter your first name"
            required
          />
        </div>
        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="lastName"
            placeholder="Enter your last name"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password:</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm your password"
            required
          />
        </div>
        <button type="submit">Sign Up</button>
        <div class="already-have-account">
          <h6>
            Already have an account? Click <router-link to="/login">here</router-link>
            to log in.
          </h6>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "SignupPage",
    data() {
      return {
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: "",
      };
    },
    methods: {
      handleSignup() {
        if (this.firstName && this.lastName && this.email && this.password && this.confirmPassword) {
          if (this.password !== this.confirmPassword) {
            alert("Passwords do not match.");
            return  ;
          }
          console.log("First Name:", this.firstName);
          console.log("Last Name:", this.lastName);
          console.log("Email:", this.email);
          console.log("Password:", this.password);
          alert("Signup successful!");
          // Add your signup logic here (e.g., API call)
        } else {
          alert("Please fill in all fields.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .already-have-account {
    text-align: center;
    margin-top: 10px;
  }
  </style>
  