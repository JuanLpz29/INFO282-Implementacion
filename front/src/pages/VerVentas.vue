<template>
  <q-page style="min-height: 60vh">
    <q-table
      title="Ventas"
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
    >
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

    <suspense>
      <template #default>
        <q-dialog v-model="fixed" transition-hide="rotate">
          <q-card style="max-width: 90vw">
            <q-card-section class="row items-center q-pb-none">
              <div class="text-h6">Detalles de la compra</div>
              <q-space />
              <q-btn icon="close" flat round dense v-close-popup />
            </q-card-section>

            <q-separator />
            <q-card-section style="max-height: 80vh">
              <detalles-venta :idVenta="idVenta" />
            </q-card-section>
          </q-card>
        </q-dialog>
      </template>
      <template #fallback> Loading... </template>
    </suspense>
  </q-page>
</template>

<script>
import { ref, onMounted } from "vue";
import rqts from "../myUtils/myUtils";
import DetallesVenta from "../components/DetallesVenta.vue";

const columns = [
  //   {
  //     name: "idVenta",
  //     required: true,
  //     label: "Id de la Venta",
  //     align: "center",
  //     field: "idVenta",
  //     sortable: true,
  //     headerStyle: "width: 10vh",
  //   },
  {
    name: "fecha",
    align: "center",
    label: "Fecha",
    field: "fecha",
    format: (val) => new Date(Date.parse(val + "Z")).toLocaleString("es-CL"),
    sortable: true,
  },
  {
    name: "estado",
    align: "center",
    label: "Estado",
    field: "estado",
    sortable: true,
  },
  {
    name: "total",
    align: "center",
    label: "Total",
    field: "total",
    format: (val, row) => `$${val.toLocaleString()}`,
    sortable: true,
  },
  {
    name: "idUsuario",
    align: "center",
    label: "Usuario",
    field: "idUsuario",
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
  components: { DetallesVenta },
  async setup() {
    const loading = ref(false);
    const rows = ref([]);
    const filter = ref("");
    const pagination = ref({
      sortBy: "fecha",
      descending: true,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: 10,
    });

    async function onRequest(props) {
      loading.value = true;
      const { page, rowsPerPage, descending, sortBy } = props.pagination;
      const filter = props.filter ? props.filter : "";
      const order = descending ? "DESC" : "ASC";
      const response = await rqts.getPaginatedResults(
        "ventas",
        page,
        filter,
        rowsPerPage,
        sortBy,
        order
      );
      const items = response.items;
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
      idVenta: ref(null),
      showDetails(row) {
        this.fixed = true;
        this.idVenta = row.idVenta;
        this.details = true;
        console.log(this.idVenta);
      },
    };
  },
};
</script>
