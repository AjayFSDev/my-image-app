<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input
          type="text"
          v-model="username"
          placeholder="Username"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <router-link to="/register">Register here</router-link>
      </p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const login = () => {
      // Simulated login logic (replace with actual API call)
      if (username.value === 'user' && password.value === 'password') {
        // Redirect to the dashboard on successful login
        router.push('/dashboard');
      } else {
        errorMessage.value = 'Invalid username or password';
      }
    };

    return { username, password, login, errorMessage };
  },
};
</script>

<style scoped>
html, body {
  height: 100%; /* Full height for body */
  margin: 0; /* No margin */
  display: flex; /* Flexbox for centering */
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  background-color: #f8f9fa; /* Light background color */
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw; /* Full width */
  height: 100vh; /* Full height */
}

.login-card {
  background-color: white; /* White background for card */
  padding: 40px; /* Increased padding */
  border-radius: 15px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
  text-align: center; /* Center text */
  width: 100%; /* Full width */
  max-width: 400px; /* Maximum width */
}

h1 {
  font-size: 2.5rem; /* Increase font size for heading */
}

input {
  width: calc(100% - 20px); /* Full width with padding */
  padding: 10px; /* Padding for input */
  margin-bottom: 20px; /* Space between inputs */
  border: 1px solid #ced4da; /* Border color */
  border-radius: 5px; /* Rounded corners for inputs */
}

button {
  width: 100%; /* Full width for button */
  padding: 10px; /* Padding for button */
  background-color: #007bff; /* Bootstrap primary color */
  color: white; /* Text color */
  border: none; /* No border */
  border-radius: 5px; /* Rounded corners */
  font-size: 1.2rem; /* Increase font size for button */
  cursor: pointer; /* Pointer cursor */
}

button:hover {
  background-color: #0056b3; /* Darker color on hover */
}

.error {
  color: red; /* Error message color */
  margin-top: 10px; /* Space above error message */
}
</style> so this is my login.vue