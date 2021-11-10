<template>
  <div class="q-pa-md">
    <q-table
      title="Compras"
      :rows="items"
      :columns="columns"
      row-key="name"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      class="color5"
    />
  </div>
</template>

<script >
import { ref } from "vue";
import axios from "axios";
import { useQuasar } from "quasar";
//const apiUrl = 'http://127.0.0.1:5000/compras/'
//const items = await fetch(apiUrl).then(r => r.data)
// const items = axios.get(apiUrl).then(r => r.data)
//   import { ref, reactive } from 'vue'

const columns = [
  {
    name: "idCompra",
    required: true,
    label: "Id de la Compra",
    align: "left",
    field: "idCompra",
    sortable: true,
  },
  {
    name: "idProveedor",
    align: "center",
    label: "Id del proveedor",
    field: "idProveedor",
    sortable: true,
  },
  {
    name: "tipoDocumento",
    align: "center",
    label: "Tipo del Documento",
    field: "tipoDocumento",
    sortable: true,
  },
  {
    name: "montoTotal",
    align: "center",
    label: "Monto Total de la compra",
    field: "montoTotal",
    sortable: true,
  },
  {
    name: "fecha",
    align: "center",
    label: "Fecha de la compra",
    field: "fecha",
    sortable: true,
  },
  {
    name: "montoNeto",
    align: "center",
    label: "monto Neto de la compra",
    field: "montoNeto",
    sortable: true,
  },
];

export default {
  async setup() {
    const $q = useQuasar();
    $q.loading.show({
      message: "Quemando el arduino...",
    });
    const apiUrl = "http://127.0.0.1:5000/compras/";
    const items = await axios
      .get(apiUrl)
      .then((r) => r.data)
      .catch((e) => {
        console.log(e);
        $q.loading.hide();
      });
    console.log(items);
    $q.loading.hide();
    // expose to template

    return {
      columns,
      items,
      pagination: ref({
        rowsPerPage: 10,
      }),
    };
  },
};
</script>




