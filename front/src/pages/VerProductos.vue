<template>
  <div class="q-pa-md">
    <q-table
      title="Productos"
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
        <q-input
          borderless
          dense
          debounce="300"
          v-model="filter"
          placeholder="Search"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="nombre" :props="props">
            {{ props.row.nombre }}
            <q-popup-edit v-model="props.row.nombre">
              <q-input v-model="props.row.nombre" dense autofocus counter />
            </q-popup-edit>
          </q-td>

          <q-td key="categoria" :props="props">
            {{ props.row.categoria }}
            <q-popup-edit
              v-model="props.row.categoria"
              title="Update categoria"
              buttons
            >
              <q-input
                type="textarea"
                v-model="props.row.categoria"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>

          <q-td key="stock" :props="props">
            {{ props.row.stock }}
            <q-popup-edit
              v-model="props.row.stock"
              title="Update stock"
              buttons
              persistent
            >
              <q-input
                type="number"
                v-model="props.row.stock"
                dense
                autofocus
                hint="Use buttons to close"
              />
            </q-popup-edit>
          </q-td>

          <q-td key="descripcion" :props="props">
            <div class="text-pre-wrap">{{ props.row.descripcion }}</div>
            <q-popup-edit v-model="props.row.descripcion">
              <q-input
                type="textarea"
                v-model="props.row.descripcion"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>

          <!-- <q-td key="protein" :props="props">{{ props.row.protein }}</q-td>
          <q-td key="sodium" :props="props">{{ props.row.sodium }}</q-td>
          <q-td key="calcium" :props="props">{{ props.row.calcium }}</q-td>
          <q-td key="iron" :props="props">{{ props.row.iron }}</q-td> -->
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";

const mycolumns = [
  {
    name: "nombre",
    required: true,
    label: "Un producto cualquiera",
    align: "left",
    field: (row) => row.nombre,
    format: (val) => `${val}`,
    sortable: true,
    style: "width: 35vh",
    headerStyle: "width: 35vh",
  },
  {
    name: "categoria",
    align: "center",
    label: "Categoria",
    field: "categoria",
    sortable: true,
    style: "width: 12vh",
    headerStyle: "width: 12vh",
    align: "center",
  },

  {
    name: "stock",
    label: "Stock",
    field: "stock",
    sortable: true,
    style: "width: 7vh",
    headerStyle: "width: 7vh",
    align: "center",
  },

  {
    name: "descripcion",
    label: "Descripcion",
    field: "descripcion",
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },
];
// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
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