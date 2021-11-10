<template>
<div>
    {{ selected }}
    <div v-if="selected === 'productos'" class="demo">
        productosss
        <li v-for="item in items" :key="item.nombre">
        {{ item.nombre }} - precio unitario: ${{ item.precioUnitario }}
        </li>
    </div>
    <div v-else-if="selected === 'compras'">
        comprasss
        <li v-for="item in items" :key="item.idCompra">
        {{ item.tipoDocumento }}  - monto neto: ${{ item.montoNeto }}
    </li>
    </div>
    </div>
</template>

<script>
export default {
  props: {
    selected: {
      type: String,
      default: 'Cock'
    },
    items: {
      type: Array,
      default: null
    }
  }
}
</script>

<style>

</style>
