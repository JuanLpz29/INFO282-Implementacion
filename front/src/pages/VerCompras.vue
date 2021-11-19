<template>
  <div class="q-pa-md">
    <q-table
      title="Compras"
      :rows="items"
      :columns="columns"
      row-key="name"
      :filter="filter"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      class="text-primary"
    >
      <template v-slot:top-right>
        <div class="bg-white rounded-borders">
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Filtrar"
            style="margin-left: 8px"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </template>
    </q-table>
  </div>
</template>

<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";

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
      message: "Esperando...",
    });
    const items = await rqts.get("compras/").catch((e) => {
      console.log(e);
    });
    $q.loading.hide();
    if (typeof items == "undefined") {
      console.log("XDDDDDDD");
    }
    console.log(items);

    return {
      columns,
      items,
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 10,
      }),
    };
  },
};
</script>
