<template>
  <!-- <div class="q-pa-md"> -->
  <q-page style="min-height: 60vh">
    <q-table
      title="Busca el producto que necesitas"
      :rows="rows"
      :columns="mycolumns"
      row-key="name"
      :filter="filter"
      v-model:pagination="pagination"
      binary-state-sort
      separator="horizontal"
      style="table-layout: fixed"
      wrap-cells
      @request="onRequest"
      :rows-per-page-options="[0]"
      :loading="loading"
    >
      <template v-slot:top-right>
        <div class="bg-white rounded-borders">
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Search"
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
                icon="add"
                class="flex-center"
                color="positive"
                :disable="loading"
                @click="$emit('enlargeText', props.row)"
                v-close-popup
              />
            </template>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </q-page>
  <!-- </div> -->
</template>

<script>
import { ref, onMounted } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";

const mycolumns = [
  {
    name: "nombre",
    required: true,
    label: "Nombre del producto",
    align: "left",
    field: (row) => row.nombre,
    format: (val) => `${val}`,
    sortable: true,
    style: "width: 35vh",
    headerStyle: "width: 35vh",
  },

  {
    name: "descripcion",
    label: "Descripcion",
    field: "descripcion",
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },

  {
    name: "detalles",
    align: "center",
    label: "Agregar",
    headerStyle: "font-weight: 600",
    // field: "",
  },
];
// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
  emits: ["enlargeText"],

  async setup() {
    const loading = ref(false);
    const rows = ref([]);
    const filter = ref("");
    const pagination = ref({
      sortBy: "",
      descending: false,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: 10,
    });

    async function fetchFromServer(page, filter, rowsPerPage, sortBy, order) {
      // buscar una forma mejor
      const reqUrl = `?page=${page}&filter=${filter}&per_page=${rowsPerPage}&sortby=${sortBy}&order=${order}`;
      const items = await rqts.get(`productos/${reqUrl}`).catch((e) => {
        console.log(e);
      });

      if (typeof items == "undefined") {
        console.log("XDDDDDDD");
      }
      return items;
    }

    async function onRequest(props) {
      loading.value = true;
      const { page, rowsPerPage, descending, sortBy } = props.pagination;
      const filter = props.filter ? props.filter : "";
      const order = descending ? "DESC" : "ASC";
      console.log(sortBy);
      const response = await fetchFromServer(
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

    // expose to template
    return {
      mycolumns,
      rows,
      separator: ref("vertical"),
      filter,
      pagination,
      loading,

      onRequest,
    };
  },
};
</script>