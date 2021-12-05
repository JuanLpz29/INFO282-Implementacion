<template>
  <!-- <div class="q-pa-md"> -->
  <q-page style="min-height: 60vh">
    <div class="q-pa-md input-codigo">
      870657
      <q-form
        class="formulario-codigo"
        @submit.prevent="onSubmit"
        @reset="onReset"
      >
        <q-input
          class=""
          rounded
          outlined
          v-model="codigo"
          label="Codigo de barra"
        />
        <q-btn
          label="Agregar"
          type="submit"
          color="dark"
          style="margin-left: 40px"
        />
      </q-form>
    </div>

    <q-table
      title="Productos"
      :rows="rows"
      :columns="mycolumns"
      row-key="name"
      binary-state-sort
      separator="horizontal"
      style="table-layout: fixed"
      wrap-cells
      @request="onRequest"
      :loading="loading"
      virtual-scroll
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
    >
      <template v-slot:top-right>
        <div class="bg-white rounded-borders">
          <q-input
            borderless
            dense
            debounce="300"
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
    </q-table>

    <div class="total-pagar">
      <q-markup-table>
        <thead>
          <tr>
            <th class="text-left">Total a pagar:</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="text-left">{{total}}</td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
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
    style: "width: 35vh",
    headerStyle: "width: 35vh",
  },

  {
    name: "precio",
    label: "Precio",
    field: "precio",
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },

  {
    name: "stock",
    label: "Cantidad",
    field: "stock",
    style: "width: 7vh",
    headerStyle: "width: 7vh",
    align: "center",
  },

  {
    name: "subtotal",
    label: "Subtotal",
    field: "subtotal",
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },
];

const rows = [];

// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
  async setup() {
    const loading = ref(false);
    const $q = useQuasar();
    // const barcode = ref(null);
    const codigo = ref(null);
    const rowCount = ref(10);
    const rows = ref([]);

    // emulate fetching data from server
    function addRow(row) {
      total += row.valorItem;
      console.log(row)
      loading.value = true;
      setTimeout(() => {
        const index = Math.floor(Math.random() * (rows.value.length + 1));

        if (rows.value.length === 0) {
          rowCount.value = 0;
        }

        row.id = ++rowCount.value;
        const newRow = { ...row }; // extend({}, row, { name: `${row.name} (${row.__count})` })
        rows.value = [
          ...rows.value.slice(0, index),
          newRow,
          ...rows.value.slice(index),
        ];
        loading.value = false;
      }, 500);
    }

    // expose to template
    return {
      mycolumns,
      rows,
      codigo,
      rowCount,
      total: ref(0),
      separator: ref("vertical"),
      pagination: ref({
        rowsPerPage: 0}),
      

      async onSubmit(evt) {
        console.log("submit ", codigo.value);
        $q.loading.show({
          message: "Cargando...",
        });
        const productoVenta = {
          barcode: codigo.value,
          cantidad: 1,
        };
        const reqUrl = `?barcode=${productoVenta.barcode}&cantidad=${productoVenta.cantidad}`;
        const items = await rqts
          .get(`productos/reservar/${reqUrl}`)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();

        console.log(items);
        addRow(items);
      },
    };
  },
};
</script>


