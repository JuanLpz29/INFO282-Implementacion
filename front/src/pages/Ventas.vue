<template>
  <!-- <div class="q-pa-md"> -->
  <q-page style="min-height: 60vh">
    <div class="q-pa-md input-codigo">
      870657 2203308
      <q-form class="formulario-codigo" @submit.prevent="onSubmit">
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
      :loading="loading"
      virtual-scroll
      :rows-per-page-options="[0]"
      class="tabla-ventas"
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
        <q-tr :props="props" class="td-tabla">
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
            <th class="text-left total-label">Total a pagar:</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="text-left total-price">${{ total.toLocaleString() }}</td>
          </tr>
        </tbody>
      </q-markup-table>
    </div>
  </q-page>
  <!-- </div> -->
</template>

<script>
import { ref, onMounted, computed } from "vue";
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
    name: "valorItem",
    label: "Precio",
    field: "valorItem",
    format: (val, row) => `$${val.toLocaleString()}`,
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
    format: (val, row) => `$${(row.stock * row.valorItem).toLocaleString()}`,
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },
];

var idVentaActual = [];

// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
  async setup() {
    const loading = ref(false);
    const $q = useQuasar();
    // const barcode = ref(null);
    const codigo = ref(null);
    const rowCount = ref(10);
    const rows = ref([]);
    const total = ref(0);

    function verExistencia(codigo) {
      var existe = false;
      rows.value.forEach((element) => {
        if (element.codigoBarra === codigo) {
          existe = true;
          element.stock += 1;
        }
      });
      return existe;
    }

    // emulate fetching data from server
    function addRow(row) {
      if (rows.value[0] !== undefined) {
        var existe = verExistencia(row.codigoBarra);
        console.log(existe);
      }

      if (!existe) {
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
      total.value += parseInt(row.valorItem);
    }

    // expose to template
    return {
      loading,
      mycolumns,
      rows,
      codigo,
      rowCount,
      total,
      separator: ref("vertical"),
      aaaa: ref(0),
      pagination: ref({
        rowsPerPage: 0,
      }),

      async onSubmit(evt) {
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
        addRow(items);
      },
    };
  },
  computed: {
    getTotal() {
      this.aaaa += 1;
      console.log("aaaaa le pegó");
      console.log(this.rows.value);
      return this.aaaa;
    },
  },
};
</script>


