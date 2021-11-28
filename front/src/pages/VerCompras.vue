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
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <template v-if="col.name !== 'detalles'">
              {{ col.value }}
            </template>
            <template v-else>
              <q-btn
                unelevated
                icon="zoom_in"
                @click="showDetails(props.row)"
              ></q-btn>
            </template>
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="fixed">
      <q-card>
        <q-card-section>
          <div class="text-h6">Terms of Agreement</div>
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 50vh" class="scroll">
          idCompra a buscar: {{ msg }}
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Decline" color="dakr" v-close-popup />
          <q-btn flat label="Accept" color="dark" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
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
  {
    name: "detalles",
    align: "center",
    label: "detalles",
    field: "",
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

    function showDetails(row) {
      console.log(row);
      this.fixed = true;
      this.msg = row.idCompra;
    }

    return {
      columns,
      items,
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 10,
      }),
      showDetails,
      fixed: ref(false),
      msg: ref(""),
    };
  },
};
</script>
