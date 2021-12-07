<template>
  <!-- <div class="q-pa-md"> -->
  <q-page style="min-height: 60vh">
    <div class="container">
      <div class="q-pa-md input-codigo">
        870657 2203308 9002490221010 2241366
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

      <div class="q-pa-md cancelar-venta">
        <q-form class="formulario-cancelar" @submit.prevent="cancelarVenta">
          <q-btn
            label="Cancelar Venta"
            type="submit"
            color="dark"
            style="margin-left: 40px"
          />
        </q-form>
      </div>
    </div>

    <q-table
      title="Productos"
      :rows="rows"
      :columns="mycolumns"
      row-key="name"
      separator="horizontal"
      style="table-layout: fixed"
      wrap-cells
      :loading="loading"
      virtual-scroll
      :rows-per-page-options="[0]"
      class="tabla-ventas"
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
            <template v-if="col.name !== 'cantidad'">
              {{ col.value }}
            </template>
            <template v-else>
              {{ col.value }}
              <q-popup-edit
                v-model.number="props.row.cantidad"
                buttons
                v-slot="scope"
              >
                <q-input
                  v-model="scope.value"
                  dense
                  autofocus
                  counter
                  @keyup.enter="scope.set"
                />
              </q-popup-edit>
            </template>
          </q-td>
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
            <td class="text-left total-price">${{ total }}</td>
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
    name: "cantidad",
    label: "Cantidad",
    field: "cantidad",
    style: "width: 7vh",
    headerStyle: "width: 7vh",
    align: "center",
  },

  {
    name: "subtotal",
    label: "Subtotal",
    field: "subtotal",
    format: (val, row) => `$${(row.cantidad * row.valorItem).toLocaleString()}`,
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
    const inputcantidad = ref(1);
    const total = ref(0);
    const idVenta = ref(null);
    const usuario = ref("joselo");

    function verExistencia(codigo) {
      var existe = null;
      rows.value.forEach((element, i) => {
        if (element.codigoBarra === codigo) {
          existe = i;
        }
      });
      return existe;
    }

    // emulate fetching data from server
    function addRow(row) {
      if (rows.value[0] !== undefined) {
        var existe = verExistencia(row.codigoBarra);
      }

      if (existe === null) {
        loading.value = true;

        if (rows.value.length === 0) {
          rowCount.value = 0;
        }

        row.id = ++rowCount.value;
        const newRow = { ...row }; // extend({}, row, { name: `${row.name} (${row.__count})` })
        rows.value = [...rows.value.slice(0, rows.value.length + 1), newRow];
        loading.value = false;
      } else {
        console.log(existe, rows.value[existe]);
        rows.value.splice(existe, 1, row);
      }
      row.subtotal = parseInt(row.valorItem) * row.cantidad;
    }

    // expose to template
    return {
      loading,
      mycolumns,
      rows,
      codigo,
      rowCount,
      inputcantidad,
      total,
      idVenta,
      usuario,
      separator: ref("vertical"),
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

        if (!idVenta.value) {
          console.log("Existe id venta");
          const reqUrl = `?user=${usuario.value}&barcode=${codigo.value}`;
          const infoVenta = await rqts
            .get(`ventas/start/${reqUrl}`)
            .catch((e) => {
              console.log(e);
            });
          $q.loading.hide();
          total.value = infoVenta.venta.total;
          idVenta.value = infoVenta.venta.idVenta;

          console.log(infoVenta.producto);
          addRow(infoVenta.producto);
        } else {
          console.log("reservnado");
          const reqUrl = `?cantidad=1&barcode=${codigo.value}&idVenta=${idVenta.value}`;
          const items = await rqts.get(`ventas/update/${reqUrl}`).catch((e) => {
            console.log(e);
          });
          $q.loading.hide();
          total.value = items.venta.total;
          addRow(items.producto);
        }
      },

      async cancelarVenta() {
        $q.loading.show({
          message: "Cargando...",
        });
        const reqUrl = `?idVenta=${idVenta.value}&user=${usuario.value}`;
        const respuesta = await rqts
          .get(`ventas/cancel/${reqUrl}`)
          .catch((e) => {
            console.log(e);
          });
        console.log(respuesta);
        $q.loading.hide();
      },

      nuevaCantidad(cantidad) {
        console.log(cantidad);
        return cantidad.set;
      },
    };
  },
};
</script>


