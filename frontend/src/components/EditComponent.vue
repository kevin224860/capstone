<template>
    <div v-if="show" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Edit Stock</h2>
  
        <div class="input-group">
          <label>Stock Symbol:</label>
          <input v-model="editedStock.stock" class="input-field" />
          <p v-if="errors.stock" class="error-message">{{ errors.stock }}</p>
        </div>
  
        <div class="input-group">
          <label>Industry:</label>
          <select v-model="editedStock.name" class="input-field">
            <option disabled value="">Select an industry</option>
            <option v-for="industry in industries" :key="industry.id" :value="industry.id">
                {{ industry.name }}
            </option>
           </select>
           <p v-if="errors.name" class="error-message">{{ errors.name }}</p>
        </div>
  
        <div class="input-group">
          <label>Number:</label>
          <input v-model.number="editedStock.number" type="number" class="input-field" />
          <p v-if="errors.number" class="error-message">{{ errors.number }}</p>

        </div>
  
        <div class="input-group">
            <label>Price per share:</label>
            <input v-model.number="editedStock.price_per_share" type="number" step="0.01" class="input-field" />
            <p v-if="errors.price_per_share" class="error-message">{{ errors.price_per_share }}</p>
        </div>
  
        <div class="input-group">
            <label>Date:</label>
            <input v-model="formattedDate" type="date" class="input-field" />
            <p v-if="errors.date" class="error-message">{{ errors.date }}</p>
        </div>
  
        <div class="button-group">
            <button class="save-btn" @click="() => { console.log('Save button clicked'); updateStock(); }">Save</button>
            <button class="cancel-btn" @click="closeModal">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    props: { show: Boolean, stock: Object },
    data() {
      return {
        editedStock: { ...this.stock },
        industries: [], // Store fetched industries
        errors: {},
        isModalVisible: false,
      };
    },
    computed: {
    formattedDate: {
      get() {
        if (!this.editedStock.date) return "";
        const date = new Date(this.editedStock.date);
        console.log(date.toISOString().split("T")[0]);
        return date.toISOString().split("T")[0]; // Format to 'YYYY-MM-DD'
      },
      set(value) {
        this.editedStock.date = value;
      }
    }
  },
  watch: {
    stock(newVal) {
        this.editedStock = { ...newVal };

        // Convert the industry name to industry ID
        const selectedIndustry = this.industries.find(ind => ind.name === newVal.name);
        if (selectedIndustry) {
        this.editedStock.name = selectedIndustry.id;  // Store ID instead of name
        }
    },
    modelValue(newVal) {
        if (!newVal) {
        this.$emit('close');
        }
    }
  },
  async mounted() {
    await this.fetchIndustries();
  },
    methods: {
        validateSymbol() {
            if (!this.editedStock.stock) {
            this.errors.stock = "Symbol is required";
            } else if (!/^[A-Z0-9]{1,5}([.-]?[A-Z0-9]{1,3})?$/.test(this.editedStock.stock)) {
            this.errors.stock = "Invalid stock symbol format";
            } else {
            this.errors.stock = "";
            }
        },
    
        validateIndustry() {
            if (!this.editedStock.name) {
            this.errors.name = "Industry is required";
            } else {
            this.errors.name = "";
            }
        },
    
        validateNumber() {
            if (!this.editedStock.number) {
            this.errors.number = "Number is required";
            } else if (isNaN(this.editedStock.number) || !Number.isInteger(Number(this.editedStock.number)) || this.editedStock.number <= 0) {
            this.errors.number = "Number must be a positive integer";
            } else {
            this.errors.number = "";
            }
        },
    
        validatePrice() {
            if (!this.editedStock.price_per_share) {
            this.errors.price_per_share = "Price per share is required";
            } else if (!/^\d+(\.\d{1,2})?$/.test(this.editedStock.price_per_share)) {
            this.errors.price_per_share = "Invalid price format";
            } else {
            this.errors.price_per_share = "";
            }
        },
    
        validateDate() {
            if (!this.editedStock.date) {
            this.errors.date = "Date is required";
            } else {
            this.errors.date = "";
            }
        },

        async updateStock() {
            console.log(`${process.env.VUE_APP_UPDATESTOCK}`);
            this.validateSymbol();
            this.validateIndustry();
            this.validateNumber();
            this.validatePrice();
            this.validateDate();
    
            if (Object.values(this.errors).some((error) => error)) return;

            try {
                console.log(`${process.env.VUE_APP_URL}${process.env.VUE_APP_UPDATESTOCK}/${this.editedStock.entry_ID}`);
                const token = localStorage.getItem("token");
                const response = await axios.put(`${process.env.VUE_APP_URL}${process.env.VUE_APP_UPDATESTOCK}/${this.editedStock.entry_ID}`,
                    this.editedStock,
                    {
                    headers: { Authorization: `Bearer ${token}` },
                    }
                );

                this.$emit("close", response); // Properly close the modal
                window.location.reload();

            } catch (error) {
                console.error("Error updating stock:", error);
            }
        },
      async fetchIndustries() {
        try {
            const response = await axios.get(`${process.env.VUE_APP_URL}${process.env.VUE_APP_INDUSTRIES}`);
            this.industries = response.data.industries.map(industry => ({
            id: industry[0],  // Industry ID
            name: industry[1]  // Industry Name
            }));
        } catch (error) {
            console.error("Error fetching industries:", error);
        }
      },
      closeModal() {
        this.$emit("close");
      }
    }
  };
  </script>
  
  <style scoped>
  /* Modal Overlay */
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
  
  /* Modal Box */
  .modal-content {
    background: white;
    padding: 25px;
    border-radius: 10px;
    width: 350px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
  
  /* Input Fields */
  .input-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
    text-align: left;
  }
  
  .input-group label {
    font-weight: bold;
    margin-bottom: 5px;
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
  
  /* Button Group */
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
  