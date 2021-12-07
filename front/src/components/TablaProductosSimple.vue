<template>
  <!-- <q-page style="min-height: 0vh; padding-left: 0px"> -->
  <div class="q-pa-sm">
    <q-table
      title="Productos"
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
    </q-table>
    <!-- </q-page> -->
  </div>
</template>

<script>
import { ref } from "vue";
const columns = [
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

export default {
  props: {
    items: Array,
    esVenta: Boolean,
  },

  setup(props) {
    if (props.esVenta) {
      columns[2].label = "Cantidad";
    }
    return {
      columns,
      items: ref(props.items),
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 5,
      }),
    };
  },
};
</script>
