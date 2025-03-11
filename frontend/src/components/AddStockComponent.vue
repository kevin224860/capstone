<template>
    <div v-if="show" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Add New Stock</h2>
  
        <div class="input-group">
          <label>Stock Symbol:</label>
          <input v-model="newStock.stock" class="input-field" />
          <p v-if="errors.stock" class="error-message">{{ errors.stock }}</p>
        </div>
  
        <div class="input-group">
          <label>Industry:</label>
          <select v-model="newStock.industry_id" class="input-field">
            <option disabled value="">Select an industry</option>
            <option v-for="industry in industries" :key="industry.id" :value="industry.id">
              {{ industry.name }}
            </option>
          </select>
          <p v-if="errors.industry_id" class="error-message">{{ errors.industry_id }}</p>
        </div>
  
        <div class="input-group">
          <label>Number:</label>
          <input v-model.number="newStock.number" type="number" class="input-field" />
          <p v-if="errors.number" class="error-message">{{ errors.number }}</p>
        </div>
  
        <div class="input-group">
          <label>Price per Share:</label>
          <input v-model.number="newStock.price_per_share" type="number" step="0.01" class="input-field" />
          <p v-if="errors.price_per_share" class="error-message">{{ errors.price_per_share }}</p>
        </div>
  
        <div class="input-group">
          <label>Date:</label>
          <input v-model="newStock.date" type="date" class="input-field" />
          <p v-if="errors.date" class="error-message">{{ errors.date }}</p>
        </div>
  
        <div class="button-group">
          <button class="save-btn" @click="handleStockSubmission">Add</button>
          <button class="cancel-btn" @click="closeModal">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    props: { show: Boolean },
    data() {
      return {
        newStock: {
          stock: "",
          industry_id: "",
          number: null,
          price_per_share: null,
          date: "",
        },
        industries: [],
        errors: {},
      };
    },
    async mounted() {
      await this.fetchIndustries();
    },
    methods: {
      validateSymbol() {
        if (!this.newStock.stock) {
          this.errors.stock = "Symbol is required";
        } else if (!/^[A-Z0-9]{1,5}([.-]?[A-Z0-9]{1,3})?$/.test(this.newStock.stock)) {
          this.errors.stock = "Invalid stock symbol format";
        } else {
          this.errors.stock = "";
        }
      },
  
      validateIndustry() {
        if (!this.newStock.industry_id) {
          this.errors.industry_id = "Industry is required";
        } else {
          this.errors.industry_id = "";
        }
      },
  
      validateNumber() {
        if (!this.newStock.number) {
          this.errors.number = "Number is required";
        } else if (isNaN(this.newStock.number) || !Number.isInteger(Number(this.newStock.number)) || this.newStock.number <= 0) {
          this.errors.number = "Number must be a positive integer";
        } else {
          this.errors.number = "";
        }
      },
  
      validatePrice() {
        if (!this.newStock.price_per_share) {
          this.errors.price_per_share = "Price per share is required";
        } else if (!/^\d+(\.\d{1,2})?$/.test(this.newStock.price_per_share)) {
          this.errors.price_per_share = "Invalid price format";
        } else {
          this.errors.price_per_share = "";
        }
      },
  
      validateDate() {
        if (!this.newStock.date) {
          this.errors.date = "Date is required";
        } else {
          this.errors.date = "";
        }
      },
  
      async handleStockSubmission() {
        this.validateSymbol();
        this.validateIndustry();
        this.validateNumber();
        this.validatePrice();
        this.validateDate();
  
        if (Object.values(this.errors).some((error) => error)) return;
  
        try {
          const response = await axios.post(`${process.env.VUE_APP_URL}${process.env.VUE_APP_ADDSTOCK}`, this.newStock, {
            headers: {
              "Content-Type": "application/json",
            },
          });
          this.$emit("close", response); // Properly close the modal
          window.location.reload();
        } catch (error) {
          console.error("Error adding stock:", error.response ? error.response.data : error.message);
        }
      },
  
      async fetchIndustries() {
        try {
          const response = await axios.get(`${process.env.VUE_APP_URL}${process.env.VUE_APP_INDUSTRIES}`);
          this.industries = response.data.industries.map((industry) => ({
            id: industry[0],
            name: industry[1],
          }));
        } catch (error) {
          console.error("Error fetching industries:", error);
        }
      },
  
      closeModal() {
        this.$emit("close");
      },
    },
  };
  </script>
  
  
  <style scoped>
  /* Styles same as EditComponent */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    background: white;
    padding: 25px;
    border-radius: 10px;
    width: 350px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
  .input-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
    text-align: left;
  }
  .input-field {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
    width: 100%;
  }
  .error-message{
    color: #dc3545;
  }
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
  }
  .save-btn {
    background: #007bff;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  .cancel-btn {
    background: #dc3545;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  .save-btn:hover {
    background: #0056b3;
  }
  .cancel-btn:hover {
    background: #b02a37;
  }
  </style>
  