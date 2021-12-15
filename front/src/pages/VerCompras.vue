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

    <q-dialog v-model="fixed" transition-hide="rotate">
      <q-card style="max-width: 90vw">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Detalles de la compra</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />
        <q-card-section style="max-height: 80vh">
          <suspense>
            <template #default>
              <detalles-compra :idCompra="idCompra" />
            </template>
            <template #fallback> </template>
          </suspense>
        </q-card-section>
      </q-card>
    </q-dialog>
    
  </div>
</template>

<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import DetallesCompra from "../components/DetallesCompra.vue";

const columns = [
  {
    name: "idCompra",
    required: true,
    label: "Id de la Compra",
    align: "center",
    field: "idCompra",
    sortable: true,
    headerStyle: "width: 10vh",
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
    name: "montoNeto",
    align: "center",
    label: "monto Neto de la compra",
    format: (val, row) => `$${val.toLocaleString()}`,
    field: "montoNeto",
    sortable: true,
  },
  {
    name: "montoTotal",
    align: "center",
    label: "Monto Total de la compra",
    field: "montoTotal",
    format: (val, row) => `$${val.toLocaleString()}`,
    sortable: true,
  },
  {
    name: "fecha",
    align: "center",
    label: "Fecha de la compra",
    field: "fecha",
    format: (val, row) => `${val.split("-").reverse().join("-")}`,
    sortable: true,
  },
  {
    name: "detalles",
    align: "center",
    label: "Ver detalles",
    headerStyle: "font-weight: 600",
    // field: "",
  },
];

export default {
  components: { DetallesCompra },
  async setup() {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargando...",
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
      fixed: ref(false),
      msg: ref(""),
      details: ref(false),
      idCompra: ref(null),
      showDetails(row) {
        this.fixed = true;
        this.idCompra = row.idCompra;
        this.details = true;
        console.log(this.idCompra);
      },
    };
  },
};

</script>
