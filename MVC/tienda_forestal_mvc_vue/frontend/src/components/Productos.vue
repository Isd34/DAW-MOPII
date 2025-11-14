<template>
  <div>
    <h2>Catálogo de Productos</h2>
    <div v-if="loading">Cargando productos...</div>
    <div v-else class="grid">
      <div v-for="p in productos" :key="p.id" class="card">
        <img :src="'/img/' + p.imagen" :alt="p.nombre" />
        <h3>{{ p.nombre }}</h3>
        <p>{{ p.descripcion }}</p>
        <strong>{{ p.precio }} €</strong><br>
        <small>Stock: {{ p.stock }}</small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const productos = ref([])
const loading = ref(true)

onMounted(async () => {
  const res = await axios.get('/api/productos')
  productos.value = res.data
  loading.value = false
})
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
.card {
  background: white;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}
.card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
</style>

