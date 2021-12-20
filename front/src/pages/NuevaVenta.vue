<template>
  <!-- <div class="q-pa-md"> -->
  <q-page class="f-container" style="min-height: 60vh">
    <div class="grid-child-element">
      <div class="first-container">
        <div class="inner-container">
          <q-form class="q-pa-md formulario-codigo" @submit.prevent="onSubmit">
            <q-input
              style="width: 300px"
              rounded
              label="Ingrese codigo de barra"
              outlined
              v-model="codigo"
            >
              <template v-slot:after>
                <q-btn round dense flat icon="send" @click="onSubmit" />
              </template>
            </q-input>
          </q-form>
        </div>
        <div class="operations-container">
          <div class="cancelar-venta">
            <div class="formulario-cancelar">
              <q-btn
                :disabled="!idVentaCancel"
                icon="cancel"
                label="Cancelar Venta"
                type="submit"
                color="negative"
                id="btn-cancelar"
                @click="confirmCancelar = true"
              />
            </div>
            <div v-if="ventaAnterior">
              cancelar venta anterior (id {{ idVentaCancel }})
            </div>
          </div>

          <div class="buscar-producto inner-container">
            <q-btn
              icon="search"
              label="Buscar producto"
              type="submit"
              color="dark"
              id="btn-cancelar"
              @click="() => (buscar = true)"
            ></q-btn>
          </div>
        </div>
      </div>

      <q-table
        ref="myTab"
        :title="titulotabla"
        :rows="rows"
        :columns="mycolumns"
        row-key="name"
        separator="horizontal"
        style="table-layout: fixed; height: 500px"
        wrap-cells
        :loading="loading"
        virtual-scroll
        :rows-per-page-options="[0]"
        class="tabla-ventas"
        no-data-label="Escanee o busque un producto"
        no-results-label="No se encontraron productos"
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
              <template
                v-if="col.name !== 'cantidad' && col.name !== 'eliminar'"
              >
                {{ col.value }}
              </template>
              <template v-else-if="col.name === 'cantidad'">
                {{ col.value }}
                <!-- <q-popup-edit
                  v-model.number="props.row.cantidad"
                  buttons
                  v-slot="scope"
                  :validate="cantidadRangeValidation"
                  @hide="cantidadRangeValidation"
                  @save="actualizar(props.row)"
                > -->
                <q-popup-edit
                  v-model.number="props.row.cantidad"
                  buttons
                  :validate="(val) => val >= 0 && val < 100"
                  @save="
                    (val, previous) => actualizar(props.row, val, previous)
                  "
                >
                  <template v-slot="scope">
                    <q-input
                      type="number"
                      v-model="scope.value"
                      :model-value="scope.value"
                      dense
                      autofocus
                      counter
                      reactive-rules
                      :rules="[
                        (val) =>
                          scope.validate(scope.value) ||
                          'Debe ingresar una cantidad entre 0 y 100',
                      ]"
                      @keyup.enter="scope.set"
                      hint="Elija una nueva cantidad de producto"
                    />
                  </template>
                </q-popup-edit>
              </template>

              <template v-else>
                <q-btn
                  class="flex-center"
                  color="negative"
                  :disable="loading"
                  label="X"
                  @click="actualizar(props.row, 0, props.row.cantidad)"
                />
              </template>
            </q-td>
          </q-tr>
        </template>

        <template v-slot:no-data="{ message }">
          <div class="full-width row flex-center text-positive q-gutter-sm">
            <span> {{ message }} </span>
          </div>
        </template>
      </q-table>
    </div>
    <div class="grid-child-element">
      <table class="full-table">
        <tbody>
          <tr>
            <td><h4 class="label">Total:</h4></td>
            <td>
              <h4 class="info">${{ total.toLocaleString() }}</h4>
            </td>
          </tr>
          <!-- <tr>
            <td><h4>Vuelto:</h4></td>
            <td>
              <h4>{{ total }}</h4>
            </td>
          </tr> -->
        </tbody>
      </table>

      <q-select
        outlined
        v-model="medio"
        :options="selectMedio"
        label="Medios de pago"
        emit-value
      />

      <q-select
        outlined
        v-model="documento"
        :options="tipoDeDocumento"
        label="Tipo de documento"
        class="selector-documento"
      />

      <div v-if="medio == 'Efectivo'" class="vuelto-container">
        <q-input outlined v-model="monto" placeholder="Calcular vuelto...">
          <template v-slot:prepend>
            <q-icon name="money" />
          </template>
        </q-input>

        <table class="full-table vuelto">
          <tbody>
            <tr>
              <td><h4>Vuelto:</h4></td>
              <td>
                <h4>
                  ${{
                    (monto - total > 0 ? monto - total : 0).toLocaleString()
                  }}
                </h4>
              </td>
            </tr>
            <!-- <tr>
            <td><h4>Vuelto:</h4></td>
            <td>
              <h4>{{ total }}</h4>
            </td>
          </tr> -->
          </tbody>
        </table>
      </div>
      <div class="btns-finalizar">
        <q-form
          class="formulario-finalizar-venta"
          @submit.prevent="confirmFinalizar"
        >
          <q-btn
            :disabled="!idVentaCancel"
            icon="done"
            color="positive"
            class="full-width"
            label="Finalizar venta"
            :disable="total == false"
            type="submit"
            @click="confirmFinalizar = true"
          />
        </q-form>
      </div>
    </div>
  </q-page>
  <!-- </div> -->
  <q-page-sticky position="bottom-left" :offset="[18, 12]">
    <!-- <div class="q-pa-md finalizar-compra"> -->

    <!-- </div> -->
  </q-page-sticky>

  <q-dialog v-model="buscar" transition-hide="rotate">
    <q-card style="max-width: 90vw">
      <q-card-section class="row items-center q-pb-none">
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <buscador-productos @enlarge-text="producto = $event" />
    </q-card>
  </q-dialog>

  <q-dialog v-model="confirmCancelar" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm"
          >¿Estás seguro que deseas cancelar la venta en curso?</span
        >
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="No" color="negative" v-close-popup />
        <q-btn
          flat
          label="Si"
          color="dark"
          v-close-popup
          @click="cancelarVenta"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="confirmFinalizar" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm"
          >¿Estás seguro que deseas finalizar la venta en curso?</span
        >
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="No" color="negative" v-close-popup />
        <q-btn
          flat
          label="Si"
          color="dark"
          v-close-popup
          @click="finalizarVenta"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>



<script>
import { ref, getCurrentInstance, watch, onMounted } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import buscadorProductos from "../components/BuscadorProductos.vue";
import updateUsername from "../plugins/updateUsername";
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
  {
    name: "eliminar",
    align: "center",
    label: "Eliminar",
    headerStyle: "font-weight: 600",
    // field: "",
  },
];
const codes = [
  "870657",
  "9002490221010",
  "870837",
  "871093",
  "7804300004019",
  "7868863",
  "7868863",
  "7868865",
  "7868862",
  "2242095",
];

Array.prototype.random = function () {
  return this[Math.floor(Math.random() * this.length)];
};

// QTable needs to know the total number of rows available in order to correctly render the pagination links. Should filtering cause the rowsNumber to change then it must be modified dynamically.
export default {
  components: { buscadorProductos },

  async setup() {
    const { currentUser, currentUserId } = updateUsername();
    const loading = ref(false);
    const $q = useQuasar();
    const codigo = ref(null);
    const rowCount = ref(0);
    const rows = ref([]);
    // const inputcantidad = ref(1);
    const total = ref(0);
    const titulotabla = ref("Agregue productos para iniciar la venta");
    const idVenta = ref(null);
    const idVentaCancel = ref(null);
    const myTab = ref(null);
    const producto = ref(null);
    const medio = ref("Efectivo");
    const monto = ref(null);
    const vuelto = ref(0);
    const documento = ref("Boleta");
    const ventaAnterior = ref(false);
    const errorCantidad = ref(false);
    const errorMessageCantidad = ref("");

    function vaciarVariables() {
      rows.value = [];
      total.value = 0;
      idVenta.value = null;
      idVentaCancel.value = null;
    }

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
      titulotabla.value = "Venta en curso";
      //   si hay al menos un producto ver si es que el que se quiere agregar es el mismo
      if (rows.value[0] !== undefined) {
        var existe = verExistencia(row.codigoBarra);
      }

      // si no existe, agregar una row
      if (existe === null) {
        loading.value = true;

        if (rows.value.length === 0) {
          rowCount.value = 0;
        }

        row.id = ++rowCount.value;
        const newRow = { ...row };
        rows.value = [...rows.value.slice(0, rows.value.length + 1), newRow];
        loading.value = false;
      }
      // si existe, modificar la row correspondiente
      else {
        rows.value.splice(existe, 1, row);
      }
      // parece que se murio el autoscroll
      myTab.value.scrollTo(1000, "end-force");
    }

    async function onSubmit(evt) {
      if (!idVenta.value) {
        iniciarVenta();
      } else {
        actualizarVenta();
      }
    }

    async function iniciarVenta() {
      const argsIniciarVenta = {
        nombre: currentUser.value,
        codigoBarra: codigo.value,
      };
      $q.loading.show({
        message: "Cargando...",
      });
      console.log("INICIANDOOOO");
      const infoVenta = await rqts
        .postjson(`ventas/`, argsIniciarVenta)
        .catch((e) => {
          console.log(e);
        });
      $q.loading.hide();
      const ok = checkAndAdd(infoVenta);
      if (ok == true) {
        idVenta.value = infoVenta.venta.idVenta;
        idVentaCancel.value = infoVenta.venta.idVenta;
      }
    }

    async function actualizarVenta() {
      const updateArgs = {
        operation: "update",
        cantidad: 1,
        codigoBarra: codigo.value,
      };
      $q.loading.show({
        message: "Cargando...",
      });
      const infoVenta = await rqts
        .putjson(`ventas/${idVenta.value}`, updateArgs)
        .catch((e) => {
          console.log(e);
        });
      $q.loading.hide();
      checkAndAdd(infoVenta);
    }

    function checkAndAdd(infoVenta) {
      console.log("checkeando", infoVenta);
      if (infoVenta.venta) {
        total.value = infoVenta.venta.total;
        addRow(infoVenta.producto);
        return true;
      } else if (infoVenta.statusText == "CONFLICT") {
        // alternativa permitir reanudar_venta()
        console.log("error!", infoVenta.message);
        idVentaCancel.value = parseInt(infoVenta.message.split(":")[1]);
        titulotabla.value = "Debe cancelar la venta anterior ";
      } else if (infoVenta.statusText == "NOT FOUND") {
        console.log("error!", infoVenta.message);
        // ok = agregar_producto(nuevo_barcode, nuevo_nombre, nuevo_precio)
        // if ok
        //  codigo.value = nuevo_barcode
        //  return onsubmit()
      } else {
        console.log("error desconocido!", infoVenta.message);
      }
      return false;
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
    watch(producto, (producto, prevCount) => {
      console.log("xzd", producto);
      codigo.value = producto.codigoBarra;
      onSubmit();
    });

    watch(currentUser, (currentUser, prevCount) => {
      console.log("xzd", currentUser);
      alert("bye");
      vaciarVariables();
    });

    async function setIdToCancel() {
      if (currentUserId.value) {
        const resp = await rqts.get(`usuarios/${currentUserId.value}`);
        console.log(resp);
        if (resp.idVentaActiva) {
          idVentaCancel.value = resp.idVentaActiva;
          ventaAnterior.value = resp.idVentaActiva;
        }
      }
    }
    onMounted(() => {
      setIdToCancel();
    });

    return {
      barcodeScanner,
      loading,
      medio,
      vuelto,
      monto,
      mycolumns,
      rows,
      codigo,
      rowCount,
      //   inputcantidad,
      total,
      idVenta,
      currentUser,
      separator: ref("vertical"),
      pagination: ref({
        rowsPerPage: 0,
      }),
      buscar: ref(false),
      selectMedio: ["Efectivo", "Debito", "Credito", "Fiado"],
      tipoDeDocumento: ["Boleta", "Factura", "Guia de despacho"],
      onSubmit,
      idVentaCancel,
      errorMessageCantidad,
      errorCantidad,
      myTab,
      producto,
      medio,
      documento,
      titulotabla,
      ventaAnterior,
      confirmFinalizar: ref(false),
      confirmCancelar: ref(false),
      cantidadRangeValidation(val) {
        if (val < 0 || val > 100) {
          errorCantidad.value = true;
          errorMessageCantidad.value = "Debe ser entre 0 y 100";
          return false;
        }
        errorCantidad.value = false;
        errorMessageCantidad.value = "";
        return true;
      },

      async actualizar(row, val, prev) {
        $q.loading.show({
          message: "Cargando...",
        });
        console.log("CANTIDAD", row.cantidad);
        if (isNaN(val) || val < 0) {
          row.cantidad = prev;
        } else {
          row.cantidad = val;
        }
        const req_args = {
          operation: "update",
          cantidad: row.cantidad,
          codigoBarra: row.codigoBarra,
          set: true,
        };
        const items = await rqts
          .putjson(`ventas/${idVenta.value}`, req_args)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        const idx = verExistencia(items.producto.codigoBarra);
        if (val == 0) {
          this.removeRow(idx);
        } else {
          rows.value.splice(idx, 1, items.producto);
        }
        total.value = items.venta.total;
      },

      removeRow(index) {
        rows.value = [
          ...rows.value.slice(0, index),
          ...rows.value.slice(index + 1),
        ];
      },

      async cancelarVenta() {
        $q.loading.show({
          message: "Cargando...",
        });
        console.log("idVentaCancel", idVentaCancel.value);

        const req_args = {
          operation: "cancel",
          nombre: currentUser.value,
        };
        const respuesta = await rqts
          .putjson(`ventas/${idVentaCancel.value}`, req_args)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        vaciarVariables();
        ventaAnterior.value = false;
        titulotabla.value = "Agregue productos para iniciar la venta";
      },

      async finalizarVenta() {
        $q.loading.show({
          message: "Cargando...",
        });
        const req_args_confirm = {
          operation: "confirm",
          nombre: currentUser.value,
        };
        const respuesta_c = await rqts
          .putjson(`ventas/${idVenta.value}`, req_args_confirm)
          .catch((e) => {
            console.log(e);
          });
        message: "";
        const req_args = {
          operation: "pay",
          nombre: currentUser.value,
          medio: medio.value,
        };

        const respuesta = await rqts
          .putjson(`ventas/${idVenta.value}`, req_args)
          .then((response) =>
            $q.notify({
              color: "green-4",
              textColor: "white",
              icon: "cloud_done",
              message: "pagada",
            })
          )
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        console.log(respuesta);
        vaciarVariables();
      },
    };
  },
};
</script>


<style lang="sass">
label
    width: 100%

.first-container
    display: grid
    grid-template-columns: 50% 50%!important

    /* justify-content: space-between; */

.operations-container
    display: flex
    justify-content: flex-end

.f-container
    display: grid
    grid-template-columns: 68% 32%
    grid-gap: 20px

.grid-child-element
    margin: 10px

h4
    margin: 0
    margin-bottom: 50px
    padding: 0

.grid-child-element
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12)
    border-radius: 6px
    padding: 20px

.btns-finalizar
    display: flex
    flex-direction: column

.full-table
    width: 100%

.full-table > td
    width: 50%

.full-table td
    text-align: left

.vuelto-container
    margin-top: 30px

.label
    color: $negative
    font-weight: bold

.selector-documento
    margin-top: 10px

form.q-form.formulario-finalizar-venta
    padding: 0
    padding-bottom: 10px
.btn-finalizar-venta
    width: 100%
    padding: 10px

.vuelto h4
    font-size: 22px

.formulario-cancelar
    margin-right: 10px
</style>
