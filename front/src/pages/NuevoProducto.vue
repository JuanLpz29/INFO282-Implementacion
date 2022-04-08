<template>
  <div class="q-pa-md bruh fondo-blur1" style="max-width: auto">
    <h2 class="title">Agregar producto</h2>
    <q-form @submit.prevent="onSubmit" @reset="onReset" class="q-gutter-md">
      <div class="q-pa-md">
        <div class="row">
          <q-input
            filled
            v-model="nombre"
            label="Nombre del producto *"
            hint="ej: Pepsi zero 3 L"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Este campo es obligarorio',
            ]"
            :bg-color="nombre ? 'green-2' : ''"
          />
        </div>

        <div class="row q-gutter-md">
          <div class="col">
            <q-input
              filled
              v-model="stock"
              type="number"
              label="Stock *"
              hint="1, 6, 12, etc"
              lazy-rules
              :rules="[
                (val) => (val && val > 0) || 'Este campo es obligarorio',
              ]"
              :bg-color="stock ? 'green-2' : ''"
            />
          </div>
          <div class="col">
            <q-input
              filled
              v-model="cantidadRiesgo"
              type="number"
              label="Cantidad de riesgo"
              hint="Cantidad que indica un nivel crítico en el Stock del producto"
              lazy-rules
              :rules="[
                (val) => val >= 0 || 'Debe ingresar una cantidad válida',
              ]"
              :bg-color="cantidadRiesgo ? 'green-2' : ''"
            />
          </div>
        </div>

        <div class="row q-gutter-md">
          <div class="col">
            <q-input
              filled
              type="number"
              v-model="precioUnitario"
              label="Precio unitario *"
              hint="Precio de compra con impuestos del producto"
              lazy-rules
              :rules="[
                (val) => (val && val >= 0) || 'Este campo es obligarorio',
              ]"
              :bg-color="precioUnitario ? 'green-2' : ''"
            />
          </div>
          <div class="col">
            <q-input
              filled
              v-model="precioVenta"
              type="number"
              label="Precio de venta *"
              hint="Precio de
      venta del producto"
              lazy-rules
              :rules="[
                (val) => (val && val >= 0) || 'Este campo es obligarorio',
              ]"
              :bg-color="precioVenta ? 'green-2' : ''"
            />
          </div>
        </div>

        <div class="row q-gutter-md">
          <div class="col">
            <q-input
              filled
              v-model="categoria"
              label="Categoria"
              hint="Alimentos, bebidas, etc"
              :bg-color="categoria ? 'green-2' : ''"
            />
          </div>
          <div class="col">
            <q-input
              filled
              v-model="formato"
              label="Formato"
              hint="Caja, display, granel, etc"
              :bg-color="formato ? 'green-2' : ''"
            />
          </div>
        </div>
        <div class="row">
          <q-input
            filled
            v-model="descripcion"
            label="Descripcion del producto"
            hint="ej: Bebida gaseosa envase desechable"
            :bg-color="descripcion ? 'green-2' : ''"
          />
        </div>
        <div class="row">
          <q-input
            v-model="codigo"
            hint="Codigo de barras del producto"
            :bg-color="codigo ? 'green-2' : ''"
          />
          <!-- <q-popup-edit v-model="codigo">
            <q-input type="textarea" v-model="codigo" dense autofocus />
          </q-popup-edit> -->
        </div>

        <div class="btn-container">
          <q-btn label="Agregar" type="submit" color="secondary" />
          <q-btn
            label="Reiniciar"
            type="reset"
            color="secondary"
            flat
            class="q-ml-sm"
          />
        </div>
      </div>
    </q-form>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, getCurrentInstance } from "vue";
import rqts from "../myUtils/myUtils";

export default {
  setup() {
    const $q = useQuasar();
    const nombre = ref(null);
    const descripcion = ref(null);
    const categoria = ref(null);
    const formato = ref(null);
    const stock = ref(null);
    const cantidadRiesgo = ref(null);
    const precioUnitario = ref(null);
    const precioVenta = ref(null);
    const codigo = ref(null);

    function onBarcodeScanned(barcode) {
      if (barcode.length > 5) {
        codigo.value = barcode;
        console.log("scanned: ", codigo.value);
      }
    }

    const app = getCurrentInstance();
    const barcodeScanner =
      app.appContext.config.globalProperties.$barcodeScanner;
    barcodeScanner.init(onBarcodeScanned);

    return {
      nombre,
      descripcion,
      stock,
      categoria,
      formato,
      cantidadRiesgo,
      precioUnitario,
      precioVenta,
      codigo,
      async onSubmit(evt) {
        const producto = {
          // campos obligatorios
          nombre: nombre.value,
          stock: stock.value,
          precioUnitario: precioUnitario.value,
          precioVenta: precioVenta.value,
          // campos opcionales
          descripcion: descripcion.value,
          codigoBarra: codigo.value,
          cantidadRiesgo: cantidadRiesgo.value ? cantidadRiesgo.value : 0,
          categoria: categoria.value,
          formato: formato.value,
        };
        // modificar para notificar dependiendo si la creacion fue exitosa o falló
        const response = await rqts.postjson("productos/", producto);
        if (response.added == true) {
          $q.notify({
            color: "green-4",
            textColor: "white",
            icon: "cloud_done",
            message: "Producto agregado ",
          });
        } else {
          $q.notify({
            color: "red-4",
            textColor: "white",
            icon: "error",
            message: "Error al agregar producto",
          });
        }
        console.log(response);
      },
      onReset() {
        nombre.value = null;
        descripcion.value = "";
        categoria.value = "";
        formato.value = "";
        stock.value = null;
        cantidadRiesgo.value = null;
        precioUnitario.value = null;
        precioVenta.value = null;
        codigo.value = null;
      },
      oelarva() {
        $q.notify({
          color: "pink-4",
          textColor: "white",
          icon: "cloud_done",
          message: "pistolee mi rey",
        });
      },
    };
  },
};
</script>


<style lang="sass">
@import '../quasar-variables.sass'
.q-field__messages,
.q-field__bottom_row
    color: #1d2237
    font-weight: 500

.q-form
    border-radius: 12px
    padding: 1px 15px 15px 0px

.btn-container
    text-align: left
    margin-top: 20px

title
    width: 100%
</style>