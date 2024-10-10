import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Register from '../views/Register.vue'; // Import the Register component

const routes = [
  { path: '/', component: Login },           // Login route
  { path: '/dashboard', component: Dashboard }, // Dashboard route
  { path: '/register', component: Register },   // Register route
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

