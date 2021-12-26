<template>
  <div class="q-pa-md">
    <q-table
      title="Compras"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :filter="filter"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      class="text-primary"
      @request="onRequest"
      :loading="loading"
      binary-state-sort
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

    <q-dialog :square="true" v-model="fixed" transition-hide="rotate">
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
import { ref, onMounted } from "vue";
import rqts from "../myUtils/myUtils";
import DetallesCompra from "../components/DetallesCompra.vue";

const columns = [
  //   {
  //     name: "idCompra",
  //     required: true,
  //     label: "Id de la Compra",
  //     align: "center",
  //     field: "idCompra",
  //     sortable: true,
  //     headerStyle: "width: 10vh",
  //   },
  {
    name: "folio",
    required: true,
    label: "Folio",
    align: "center",
    field: "folio",
    sortable: true,
    headerStyle: "width: 10vh",
  },
  {
    name: "idProveedor",
    align: "center",
    label: "Proveedor",
    field: "idProveedor",
    sortable: true,
    headerStyle: "width: 19vh",
  },
  {
    name: "tipoDocumento",
    align: "center",
    label: "Tipo de Documento",
    field: "tipoDocumento",
    sortable: true,
  },
  {
    name: "montoNeto",
    align: "center",
    label: "Monto Neto",
    format: (val, row) => `$${val.toLocaleString()}`,
    field: "montoNeto",
    sortable: true,
    headerStyle: "width: 20vh",
  },
  {
    name: "montoTotal",
    align: "center",
    label: "Monto Total",
    field: "montoTotal",
    format: (val, row) => `$${val.toLocaleString()}`,
    sortable: true,
    headerStyle: "width: 20vh",
  },
  {
    name: "fecha",
    align: "center",
    label: "Fecha",
    field: "fecha",
    format: (val, row) => `${val.split("-").reverse().join("-")}`,
    sortable: true,
  },
  {
    name: "detalles",
    align: "center",
    label: "Ver detalles",
    headerStyle: "width: 12vh; font-weight: 600",
    // field: "",
  },
];

export default {
  components: { DetallesCompra },
  async setup() {
    const loading = ref(false);
    const rows = ref([]);
    const filter = ref("");
    const pagination = ref({
      sortBy: "",
      descending: false,
      page: 1,
      rowsPerPage: 5,
      rowsNumber: 10,
    });

    async function onRequest(props) {
      loading.value = true;
      const { page, rowsPerPage, descending, sortBy } = props.pagination;
      const filter = props.filter ? props.filter : "";
      const order = descending ? "DESC" : "ASC";
      const response = await rqts.getPaginatedResults(
        "compras",
        page,
        filter,
        rowsPerPage,
        sortBy,
        order
      );
      console.log(response);
      const items = response.items;
      console.log(items);
      // clear out existing data and add new
      rows.value.splice(0, rows.value.length, ...items);
      pagination.value.rowsNumber = response.rowsNumber;
      // don't forget to update local pagination object
      pagination.value.page = page;
      pagination.value.rowsPerPage = rowsPerPage;
      pagination.value.sortBy = sortBy;
      pagination.value.descending = descending;
      loading.value = false;
    }

    onMounted(() => {
      // get initial data from server (1st page)
      onRequest({
        pagination: pagination.value,
        filter: undefined,
      });
    });

    return {
      columns,
      rows,
      filter,
      pagination,
      loading,
      onRequest,
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
