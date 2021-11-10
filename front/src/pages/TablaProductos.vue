<template>
  <div class="q-pa-md">
    <q-table
      title="los producctosss"
      :rows="myrows"
      :columns="mycolumns"
      :filter="filter"
      row-key="name"
      binary-state-sort
      card-class="bg-orange-1 "
      separator="horizontal"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      table-header-class="lmao"
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
import { ref } from "vue";
import { useQuasar } from "quasar";
import axios from "axios";

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

export default {
  async setup() {
    const $q = useQuasar();
    $q.loading.show({
      message: "Esperando a Parisi",
    });
    const apiUrl = "http://127.0.0.1:5000/productos/";
    const items = await axios.get(apiUrl).then((r) => r.data);
    console.log(items);
    $q.loading.hide();
    // expose to template
    return {
      mycolumns,
      myrows: ref(items),
      separator: ref("vertical"),
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 10,
      }),
    };
  },
};
</script>

<style>
.lmao {
  justify-content: center;
  text-align: center;
}
</style>