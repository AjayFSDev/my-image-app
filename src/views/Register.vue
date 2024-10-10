<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div class="input-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          @input="validateUsername"
          required
          :class="{ 'is-invalid': usernameError }"
        />
        <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          @input="validatePassword"
          required
          :class="{ 'is-invalid': passwordError }"
        />
        <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
      </div>
      <button type="submit" :disabled="isSubmitting">Register</button>
      <p v-if="registrationMessage">{{ registrationMessage }}</p>
    </form>
    <p>Already have an account? <router-link to="/">Login here</router-link></p>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import axios from 'axios'; // Import axios for making HTTP requests

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const usernameError = ref('');
    const passwordError = ref('');
    const isSubmitting = ref(false);
    const registrationMessage = ref('');

    const validateUsername = () => {
      usernameError.value = username.value.length < 3 ? 'Username must be at least 3 characters long.' : '';
    };

    const validatePassword = () => {
      passwordError.value = password.value.length < 6 ? 'Password must be at least 6 characters long.' : '';
    };

    const register = async () => {
      // Validate inputs
      validateUsername();
      validatePassword();

      if (usernameError.value || passwordError.value) {
        return; // Don't submit if there are validation errors
      }

      isSubmitting.value = true;
      registrationMessage.value = '';

      try {
        // API call to register the user
        const response = await axios.post('http://127.0.0.1:5000/register', {
          username: username.value,
          password: password.value,
        });
        registrationMessage.value = response.data.message; // Display success message
        // Clear the fields after successful registration
        username.value = '';
        password.value = '';
      } catch (error) {
        // Handle error response
        if (error.response) {
          registrationMessage.value = error.response.data.error; // Show error message from server
        } else {
          registrationMessage.value = 'An error occurred during registration.';
        }
      } finally {
        isSubmitting.value = false; // Enable the button again
      }
    };

    return { username, password, register, usernameError, passwordError, isSubmitting, registrationMessage };
  },
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.input-group {
  margin-bottom: 1rem;
}

label {
  margin-bottom: 0.5rem;
  display: block;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input.is-invalid {
  border-color: red;
}

.error-message {
  color: red;
  font-size: 0.875rem;
}

button {
  width: 100%;
  padding: 0.5rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
