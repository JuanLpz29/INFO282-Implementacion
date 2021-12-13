<template>
  <!-- <div class="q-pa-md"> -->
  <q-page style="min-height: 60vh">
    <div class="container">
      <div class="q-pa-md input-codigo">
        <q-form class="q-pa-md formulario-codigo" @submit.prevent="onSubmit">
          <q-btn
            icon="pin"
            stack
            label="random"
            color="dark"
            style="margin-right: 20px"
            @click="randomCode"
          />
          <q-input
            style="width: 150px"
            rounded
            outlined
            v-model="codigo"
            id="input-codigo"
            label="Codigo de barra"
          />
          <q-btn
            label="Agregar"
            type="submit"
            color="dark"
            style="margin-left: 20px"
          />
        </q-form>
      </div>

      <div class="q-pa-md cancelar-venta">
        <q-form class="formulario-cancelar" @submit.prevent="cancelarVenta">
          <q-btn
            label="Cancelar Venta"
            type="submit"
            color="negative"
            id="btn-cancelar"
            style="margin-left: 40px"
          />
        </q-form>
        <div v-if="idVentaCancel">
          cancelar venta anterior (id {{ idVentaCancel }})
        </div>
      </div>
    </div>

    <q-table
      ref="myTab"
      title="Venta en curso"
      :rows="rows"
      :columns="mycolumns"
      row-key="name"
      separator="horizontal"
      style="table-layout: fixed; height: 400px"
      wrap-cells
      :loading="loading"
      virtual-scroll
      :rows-per-page-options="[0]"
      class="tabla-ventas"
      no-data-label="Pistolee mi rey"
      no-results-label="The filter didn't uncover any results"
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
                :validate="cantidadRangeValidation"
                @hide="cantidadRangeValidation"
                @save="actualizar(props.row)"
              >
                <q-input
                  type="number"
                  v-model="scope.value"
                  dense
                  autofocus
                  counter
                  :rules="cantidadRules"
                  reactive-rules
                  @keyup.enter="scope.set"
                  hint="Enter a number between 1 and 100"
                  :error="errorCantidad"
                  :error-message="errorMessageCantidad"
                />
              </q-popup-edit>
            </template>
          </q-td>

          <!-- <td> -->
          <!-- <template v-slot:after> -->
          <q-btn
            class="flex-center"
            color="negative"
            :disable="loading"
            label="X"
            @click="removeRow(props.row)"
          />
          <!-- </td> -->
          <!-- </template> -->
        </q-tr>
      </template>

      <template v-slot:no-data="{ icon, message, filter }">
        <div class="full-width row flex-center text-positive q-gutter-sm">
          <q-icon size="2em" name="sentiment_neutral" />
          <span> {{ message }} </span>
          <q-icon size="2em" :name="filter ? 'filter_b_and_w' : icon" />
        </div>
      </template>
    </q-table>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <div class="total-pagar">
        <q-markup-table class="inner-total">
          <thead>
            <tr>
              <th class="text-left total-label">Total a pagar:</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-left total-price">
                ${{ total.toLocaleString() }}
              </td>
            </tr>
          </tbody>
        </q-markup-table>
      </div>
    </q-page-sticky>
  </q-page>
  <!-- </div> -->
  <q-page-sticky position="bottom-left" :offset="[18, 12]">
    <!-- <div class="q-pa-md finalizar-compra"> -->
    <q-form class="formulario-cancelar" @submit.prevent="finalizarVenta">
      <q-btn
        color="positive"
        class="full-width"
        label="Finalizar Venta"
        :disable="total == false"
        type="submit"
        style="padding: 20px; font-weight: 600; width: 600px"
      />
    </q-form>
    <!-- </div> -->
  </q-page-sticky>
</template>



<script>
import { ref, getCurrentInstance } from "vue";
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
    format: (val) => `$${val.toLocaleString()}`,
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },
];
const codes = [
  "870657",
  "9002490221010",
  "871093",
  "870837",
  "2203308",
  "2225336",
  "2241129",
  "2241366",
  "2241455",
  "2242095",
  "2242265",
  "2242362",
  "700561",
  "7804300122928",
  "7802420510205",
  "10154005C",
  "7702367003900",
  "7804616480040",
];

Array.prototype.random = function () {
  return this[Math.floor(Math.random() * this.length)];
};
var idVentaActual = [];
// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
  async setup() {
    const loading = ref(false);
    const $q = useQuasar();
    // const barcode = ref(null);
    const codigo = ref(null);
    const rowCount = ref(0);
    const rows = ref([]);
    const inputcantidad = ref(1);
    const total = ref(0);
    const idVenta = ref(null);
    const idVentaCancel = ref(null);
    const usuario = ref("joselo");
    const myTab = ref(null);

    const errorCantidad = ref(false);
    const errorMessageCantidad = ref("");

    function verExistencia(codigo) {
      var existe = null;
      rows.value.forEach((element, i) => {
        if (element.codigoBarra === codigo) {
          existe = i;
        }
      });
      return existe;
    }

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
        rows.value.splice(existe, 1, row);
      }

      myTab.value.scrollTo(1000, "end-force");
      //   row.subtotal = parseInt(row.subtotal);
    }
    // const app = getCurrentInstance()
    // const barcodeScanner = app.appContext.config.globalProperties.$BarcodeScanner\

    async function onSubmit(evt) {
      $q.loading.show({
        message: "Cargando...",
      });
      if (!idVenta.value) {
        const reqUrl = `?user=${usuario.value}&barcode=${codigo.value}`;
        const infoVenta = await rqts
          .get(`ventas/start/${reqUrl}`)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        if (infoVenta.venta) {
          total.value = infoVenta.venta.total;
          idVenta.value = infoVenta.venta.idVenta;
          addRow(infoVenta.producto);
        } else {
          idVentaCancel.value = parseInt(infoVenta.split(":")[1]);
        }
      } else {
        const reqUrl = `?cantidad=1&barcode=${codigo.value}&idVenta=${idVenta.value}`;
        const items = await rqts.get(`ventas/update/${reqUrl}`).catch((e) => {
          console.log(e);
        });
        $q.loading.hide();
        total.value = items.venta.total;
        addRow(items.producto);
      }
    }

    // funcion que maneja el scaneo en cualquier parte
    function onBarcodeScanned(barcode) {
      if (barcode.length > 5) {
        codigo.value = barcode;
        console.log("scanned: ", codigo.value);
        onSubmit();
      }
    }

    const app = getCurrentInstance();
    const barcodeScanner =
      app.appContext.config.globalProperties.$barcodeScanner;
    barcodeScanner.init(onBarcodeScanned);

    return {
      barcodeScanner,
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
      onSubmit,
      idVentaCancel,
      errorMessageCantidad,
      errorCantidad,
      myTab,
      cantidadRangeValidation(val) {
        if (val < 0 || val > 100) {
          errorCantidad.value = true;
          errorMessageCantidad.value = "The value must be between 0 and 100!";
          return false;
        }
        errorCantidad.value = false;
        errorMessageCantidad.value = "";
        return true;
      },

      randomCode() {
        codigo.value = codes.random();
      },
      async actualizar(row) {
        $q.loading.show({
          message: "Cargando...",
        });
        if (isNaN(row.cantidad) || row.cantidad < 0) {
          row.cantidad = 1;
        }

        console.log("fijando la cantidad");
        const reqUrl = `?cantidad=${row.cantidad}&barcode=${row.codigoBarra}&idVenta=${idVenta.value}&set=true`;
        const items = await rqts.get(`ventas/update/${reqUrl}`).catch((e) => {
          console.log(e);
        });
        $q.loading.hide();
        rows.value.splice(
          verExistencia(items.producto.codigoBarra),
          1,
          items.producto
        );
        total.value = items.venta.total;
      },

      async removeRow(row) {
        console.log(row.codigoBarra);
        var index = verExistencia(row.codigoBarra);
        row.cantidad = 0;
        await this.actualizar(row);
        rows.value = [
          ...rows.value.slice(0, index),
          ...rows.value.slice(index + 1),
        ];
      },

      async cancelarVenta() {
        $q.loading.show({
          message: "Cargando...",
        });
        let idToCancel;
        if (idVentaCancel.value) {
          idToCancel = idVentaCancel.value;
          idVentaCancel.value = null;
        } else {
          idToCancel = idVenta.value;
        }
        const reqUrl = `?idVenta=${idToCancel}&user=${usuario.value}`;
        const respuesta = await rqts
          .get(`ventas/cancel/${reqUrl}`)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        //rows._rawValue = [];
        // location.reload();
      },

      async finalizarVenta() {
        $q.loading.show({
          message: "Cargando...",
        });
        const reqUrl = `?idVenta=${idVenta.value}&user=${usuario.value}`;
        const respuesta = await rqts
          .get(`ventas/confirm/${reqUrl}`)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        //rows._rawValue = [];
        location.reload();
      },
    };
  },
};
</script>


