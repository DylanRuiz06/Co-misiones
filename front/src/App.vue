<script setup>
import { computed, onMounted, ref } from 'vue'

const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'
const sellers = ref([])
const rules = ref([])
const summary = ref([])
const loading = ref(false)
const error = ref('')
const sellerForm = ref({ id: null, name: '', email: '', active: true })
const dates = ref({ start: firstDayOfMonth(), end: today() })
const saleForm = ref({ seller: '', amount: '', sale_date: today(), description: '' })

function today() {
  return new Date().toISOString().slice(0, 10)
}

function firstDayOfMonth() {
  const date = new Date()
  return new Date(date.getFullYear(), date.getMonth(), 1).toISOString().slice(0, 10)
}

async function request(path, options = {}) {
  const response = await fetch(`${apiUrl}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!response.ok) throw new Error((await response.json()).detail || 'No se pudo completar la solicitud.')
  return response.json()
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    const [sellerData, ruleData] = await Promise.all([request('/sellers/'), request('/rules/')])
    sellers.value = sellerData.filter((seller) => seller.active)
    rules.value = ruleData
    if (!saleForm.value.seller && sellers.value.length) saleForm.value.seller = sellers.value[0].id
    await loadSummary()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function editSeller(seller) {
  sellerForm.value = { id: seller.id, name: seller.name, email: seller.email, active: seller.active }
}

function resetSellerForm() {
  sellerForm.value = { id: null, name: '', email: '', active: true }
}

async function saveSeller() {
  error.value = ''
  try {
    const id = sellerForm.value.id
    const path = id ? `/sellers/${id}/` : '/sellers/'
    const method = id ? 'PATCH' : 'POST'
    await request(path, { method, body: JSON.stringify(sellerForm.value) })
    resetSellerForm()
    await loadData()
  } catch (err) {
    error.value = err.message
  }
}

async function deleteSeller(seller) {
  if (!window.confirm(`¿Eliminar a ${seller.name}? También se eliminarán sus ventas.`)) return
  error.value = ''
  try {
    await request(`/sellers/${seller.id}/`, { method: 'DELETE' })
    if (String(saleForm.value.seller) === String(seller.id)) saleForm.value.seller = ''
    await loadData()
  } catch (err) {
    error.value = err.message
  }
}

async function loadSummary() {
  const params = new URLSearchParams({ start_date: dates.value.start, end_date: dates.value.end })
  summary.value = (await request(`/commission-summary/?${params}`)).results
}

async function addSale() {
  error.value = ''
  try {
    await request('/sales/', { method: 'POST', body: JSON.stringify({ ...saleForm.value, amount: Number(saleForm.value.amount) }) })
    saleForm.value.amount = ''
    saleForm.value.description = ''
    await loadSummary()
  } catch (err) {
    error.value = err.message
  }
}

const totalCommission = computed(() => summary.value.reduce((total, row) => total + Number(row.commission), 0))
const totalSales = computed(() => summary.value.reduce((total, row) => total + Number(row.total_sales), 0))
const money = (value) => new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' }).format(Number(value))
</script>

<template>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Panel de comisiones</p>
        <h1>Control de ventas</h1>
        <p class="intro">Registra vendedores y ventas, y consulta las comisiones por periodo.</p>
      </div>
    </header>

    <section class="toolbar">
      <div>
        <p class="label">Periodo de análisis</p>
        <div class="date-fields">
          <label>Desde <input v-model="dates.start" type="date" /></label>
          <label>Hasta <input v-model="dates.end" type="date" /></label>
          <button class="primary" :disabled="loading" @click="loadSummary">Actualizar</button>
        </div>
      </div>
      <div class="stats">
        <div><span>Ventas del periodo</span><strong>{{ money(totalSales) }}</strong></div>
        <div><span>Comisiones estimadas</span><strong class="accent">{{ money(totalCommission) }}</strong></div>
      </div>
    </section>

    <p v-if="error" class="error">{{ error }}</p>

    <section class="content-grid">
      <div class="table-card">
        <div class="section-heading"><div><p class="eyebrow">Rendimiento</p><h2>Resumen por vendedor</h2></div><span class="count">{{ summary.length }} activos</span></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Vendedor</th><th>Total vendido</th><th>Regla alcanzada</th><th>Comisión</th></tr></thead>
            <tbody>
              <tr v-for="row in summary" :key="row.seller_id">
                <td><strong>{{ row.seller_name }}</strong><small>Vendedor activo</small></td>
                <td>{{ money(row.total_sales) }}</td>
                <td><span class="pill">{{ row.commission_percent }}% · {{ row.rule_name }}</span></td>
                <td class="commission">{{ money(row.commission) }}</td>
              </tr>
              <tr v-if="!summary.length"><td colspan="4" class="empty">No hay vendedores activos o datos para este periodo.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <aside class="side-card">
        <p class="eyebrow">Carga rápida</p><h2>Registrar venta</h2>
        <p v-if="!sellers.length" class="hint">Primero registra un vendedor.</p>
        <form @submit.prevent="addSale">
          <label>Vendedor<select v-model="saleForm.seller" :disabled="!sellers.length" required><option disabled value="">Selecciona un vendedor</option><option v-for="seller in sellers" :key="seller.id" :value="seller.id">{{ seller.name }}</option></select></label>
          <label>Monto (USD)<input v-model="saleForm.amount" type="number" min="0" step="0.01" required placeholder="0.00" /></label>
          <label>Fecha<input v-model="saleForm.sale_date" type="date" required /></label>
          <label>Descripción <input v-model="saleForm.description" maxlength="200" placeholder="Cliente o producto" /></label>
          <button class="primary full" type="submit">Guardar venta</button>
        </form>
        <div class="rules"><p class="label">Reglas activas</p><div v-for="rule in rules" :key="rule.id" class="rule"><span>{{ rule.name }}</span><strong>{{ rule.minimum_sales }} · {{ rule.commission_percent }}%</strong></div></div>
      </aside>
    </section>

    <section class="sellers-card">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Administración</p>
          <h2>Agregar vendedor</h2>
        </div>
        <span class="count">{{ sellers.length }} registrados</span>
      </div>

      <form class="seller-form" @submit.prevent="saveSeller">
        <label>
          Nombre
          <input v-model="sellerForm.name" required placeholder="Nombre completo" />
        </label>
        <label>
          Correo
          <input v-model="sellerForm.email" type="email" placeholder="correo@ejemplo.com" />
        </label>
        <label class="checkbox-label">
          <input v-model="sellerForm.active" type="checkbox" />
          Activo
        </label>
        <div class="form-actions">
          <button class="primary" type="submit">{{ sellerForm.id ? 'Actualizar vendedor' : 'Agregar vendedor' }}</button>
          <button v-if="sellerForm.id" class="secondary" type="button" @click="resetSellerForm">Cancelar</button>
        </div>
      </form>

      <div class="seller-list">
        <div v-for="seller in sellers" :key="seller.id" class="seller-row">
          <span>
            <strong>{{ seller.name }}</strong>
            <small>{{ seller.email || 'Sin correo' }}</small>
          </span>
          <span class="row-actions">
            <button class="secondary" type="button" @click="editSeller(seller)">Editar</button>
            <button class="danger" type="button" @click="deleteSeller(seller)">Eliminar</button>
          </span>
        </div>
        <p v-if="!sellers.length" class="empty">No hay vendedores registrados.</p>
      </div>
    </section>

  </main>
</template>
