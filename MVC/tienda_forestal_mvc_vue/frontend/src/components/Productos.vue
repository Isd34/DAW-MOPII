<!-- ============================================================
   COMPONENTE Productos.vue
   --------------------------------------------------------------
   Vista principal del catálogo:
   - Consulta productos al backend Flask mediante api.js
   - Soporta búsqueda, filtros, ordenación y paginación
   - Usa Composition API (Vue 3)
   - Explicado línea por línea para que sea didáctico en clase
   ============================================================ -->

<template>
  <div>
    <h2>Catálogo de Productos</h2>

    <!-- ===============================
         BÚSQUEDA GENERAL (campo + botón)
         =============================== -->
    <input type="text" v-model="terminoBusqueda" placeholder="Aquí estuvo Iván Santos" @keyup.enter="accionEncontrar"
      class="search-input" />
    <button @click="accionEncontrar">Buscar</button>

    <!-- ===============================
         FILTROS AVANZADOS
         =============================== -->
    <div class="filtros">
      <input type="text" v-model="filtroTipo" placeholder="Tipo (motosierra, taladro…)" />
      <input type="text" v-model="filtroMarca" placeholder="Marca (STIHL, Makita…)" />
      <input type="number" v-model.number="precioMin" placeholder="Precio mínimo" />
      <input type="number" v-model.number="precioMax" placeholder="Precio máximo" />

      <select v-model="orden">
        <option value="">Orden</option>
        <option value="asc">Precio ascendente</option>
        <option value="desc">Precio descendente</option>
      </select>

      <button @click="accionFiltrar">Filtrar</button>
    </div>

    <!-- ===============================
         ESTADO DE CARGA
         =============================== -->
    <div v-if="loading">Cargando productos...</div>

    <!-- ===============================
         LISTA DE PRODUCTOS
         =============================== -->
    <div v-else class="grid">
      <div v-for="p in productos" :key="p.id" class="card">
        <img :src="'/img/' + p.imagen" :alt="p.nombre" />
        <h3>{{ p.nombre }}</h3>
        <p>{{ p.descripcion }}</p>
        <strong>{{ p.precio }} bucks</strong><br>
        <small>Stock: {{ p.stock }}</small>
      </div>
    </div>

    <!-- ===============================
         PAGINACIÓN
         =============================== -->
    <div class="paginacion" v-if="totalPaginas > 1">
      <button @click="cambiarPagina(paginaActual - 1)" :disabled="paginaActual === 1">
        ← Anterior
      </button>

      <button v-for="n in totalPaginas" :key="n" @click="cambiarPagina(n)" :class="{ activo: n === paginaActual }">
        {{ n }}
      </button>

      <button @click="cambiarPagina(paginaActual + 1)" :disabled="paginaActual === totalPaginas">
        Siguiente →
      </button>
    </div>

    <!-- Información adicional -->
    <p v-if="totalResultados > 0" style="color: green">
      Mostrando página {{ paginaActual }} de {{ totalPaginas }}
      ({{ totalResultados }} productos en total)
    </p>
  </div>
</template>

<script setup>
/* ============================================================
   IMPORTS
   ============================================================ */
import { ref } from "vue"

// Importamos las funciones del servicio api.js
// Estas funciones ya saben cómo llamar al backend Flask
import {
  obtenerProductos,
  filtrarProductos,
  buscarProductos
} from "@/services/api"


/* ============================================================
   VARIABLES REACTIVAS DEL COMPONENTE
   ============================================================ */

// Lista de productos cargados desde el backend
const productos = ref([])

// Indicador de carga (muestra "Cargando...")
const loading = ref(true)

// Campos de búsqueda y filtrado
const terminoBusqueda = ref("")
const filtroTipo = ref("")
const filtroMarca = ref("")
const precioMin = ref(null)
const precioMax = ref(null)
const orden = ref("")

// Paginación gestionada por el backend
const paginaActual = ref(1)
const porPagina = ref(10)
const totalPaginas = ref(1)
const totalResultados = ref(0)


/* ============================================================
   FUNCIÓN PRINCIPAL: cargar la lista de productos filtrados
   ------------------------------------------------------------
   - Llama a /api/productos/filtrar
   - Actualiza la lista, total de páginas y total de resultados
   ============================================================ */
const cargarProductos = async () => {
  loading.value = true

  try {
    // Llamamos a api.js con los parámetros actuales
    const data = await filtrarProductos({
      pagina: paginaActual.value,
      por_pagina: porPagina.value,
      tipo: filtroTipo.value,
      marca: filtroMarca.value,
      precio_min: precioMin.value,
      precio_max: precioMax.value,
      ordenar: orden.value
    })

    // El backend devuelve un objeto con:
    // productos, pagina_actual, total_paginas, total_resultados
    productos.value = data.productos
    paginaActual.value = data.pagina_actual
    totalPaginas.value = data.total_paginas
    totalResultados.value = data.total_resultados

  } catch (e) {
    console.error("Error cargando productos:", e)
    productos.value = []
  }

  loading.value = false
}


/* ============================================================
   FUNCIÓN: realizar búsqueda general
   ------------------------------------------------------------
   - Llama a /api/productos/buscar?termino=...
   - Se ejecuta al pulsar ENTER o el botón Buscar
   ============================================================ */
const accionEncontrar = async () => {
  paginaActual.value = 1

  // Si no hay texto, recargamos el catálogo normal
  if (!terminoBusqueda.value.trim()) {
    cargarProductos()
    return
  }

  loading.value = true

  try {
    const resultados = await buscarProductos(terminoBusqueda.value)
    productos.value = resultados

    // La búsqueda devuelve un array simple
    totalResultados.value = resultados.length
    totalPaginas.value = Math.ceil(resultados.length / porPagina.value)

  } catch (e) {
    console.error("Error en la búsqueda:", e)
  }

  loading.value = false
}


/* ============================================================
   FUNCIÓN: filtrado (reinicia a página 1)
   ============================================================ */
const accionFiltrar = () => {
  paginaActual.value = 1
  cargarProductos()
}


/* ============================================================
   FUNCIÓN: cambiar página (botones numerados)
   ============================================================ */
const cambiarPagina = (nuevaPagina) => {
  if (nuevaPagina < 1 || nuevaPagina > totalPaginas.value) return
  paginaActual.value = nuevaPagina
  cargarProductos()
}


/* ============================================================
   CARGA INICIAL DEL COMPONENTE
   ============================================================ */
cargarProductos()
</script>

<style scoped>
/* ============================================================
   ESTILOS MEJORADOS - DISEÑO MODERNO Y ELEGANTE
   ============================================================ */

/* Contenedor principal */
div > h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
  letter-spacing: -0.5px;
}

/* ---- BÚSQUEDA PRINCIPAL ---- */
.search-input {
  width: 60%;
  max-width: 500px;
  padding: 0.875rem 1.25rem;
  border: 2px solid #e0e0e0;
  border-radius: 50px;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
  margin-right: 0.75rem;
}

.search-input:focus {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.1);
}

/* ---- BOTONES GENERALES ---- */
button {
  padding: 0.875rem 1.75rem;
  background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.2);
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 106, 79, 0.3);
}

button:active:not(:disabled) {
  transform: translateY(0);
}

button:disabled {
  background: linear-gradient(135deg, #ccc 0%, #999 100%);
  cursor: not-allowed;
  opacity: 0.6;
}

/* ---- FILTROS AVANZADOS ---- */
.filtros {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 0.875rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.filtros input,
.filtros select {
  flex: 1;
  min-width: 180px;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  outline: none;
  background: white;
}

.filtros input:focus,
.filtros select:focus {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.1);
}

.filtros button {
  padding: 0.75rem 2rem;
}

/* ---- GRID DE PRODUCTOS ---- */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

/* ---- TARJETAS DE PRODUCTO ---- */
.card {
  background: white;
  padding: 0;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 35px rgba(45, 106, 79, 0.15);
  border-color: #2d6a4f;
}

.card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.card:hover img {
  transform: scale(1.05);
}

.card h3 {
  margin: 1rem 1.25rem 0.5rem;
  font-size: 1.25rem;
  color: #2c3e50;
  font-weight: 600;
  text-align: center;
}

.card p {
  margin: 0 1.25rem;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  flex-grow: 1;
  text-align: center;
}

.card strong {
  display: block;
  margin: auto 1.25rem 0.5rem;
  font-size: 1.5rem;
  color: #2d6a4f;
  font-weight: 700;
  text-align: center;
}

.card small {
  display: block;
  margin: 0 1.25rem 1.25rem;
  color: #888;
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

/* ---- ESTADO DE CARGA ---- */
div > div[v-if] {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
  font-weight: 500;
}

/* ---- PAGINACIÓN ---- */
.paginacion {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 3rem 0;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.paginacion button {
  min-width: 45px;
  padding: 0.65rem 1rem;
  margin: 0;
  background: white;
  color: #2d6a4f;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 0.95rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.paginacion button:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #2d6a4f;
  transform: translateY(-1px);
}

button.activo {
  background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%);
  color: white;
  border-color: #2d6a4f;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(45, 106, 79, 0.3);
}

/* ---- INFORMACIÓN ADICIONAL ---- */
p[style*="color: green"] {
  text-align: center;
  font-size: 1rem;
  font-weight: 500;
  margin-top: 1.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-radius: 10px;
  color: #155724 !important;
  border: 1px solid #c3e6cb;
}

/* ---- RESPONSIVE ---- */
@media (max-width: 768px) {
  .search-input {
    width: 100%;
    margin-bottom: 1rem;
    margin-right: 0;
  }

  .grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
  }

  .filtros {
    gap: 0.75rem;
  }

  .filtros input,
  .filtros select {
    min-width: 100%;
  }
}
</style>
