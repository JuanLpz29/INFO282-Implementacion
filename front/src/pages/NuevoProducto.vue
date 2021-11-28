<template>
  <div class="q-pa-md bruh fondo-blur1" style="max-width: auto">
    <h2 class="title">Agregar producto</h2>
    <q-form @submit.prevent="onSubmit" @reset="onReset" class="q-gutter-md">
      <q-input
        filled
        v-model="nombre"
        label="Nombre del producto"
        hint="ej: Pepsi zero 3 L"
        bg-color="#363A4D"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Este campo es obligarorio',
        ]"
      />
      <q-input
        filled
        v-model="descripcion"
        label="Descripcion del producto"
        hint="ej: Bebida gaseosa envase desechable"
        bg-color="#363A4D"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Este campo es obligarorio',
        ]"
      />
      <q-input
        filled
        v-model="stock"
        type="number"
        label="Stock"
        hint="1, 6, 12, etc"
        bg-color="#363A4D"
        lazy-rules
        :rules="[(val) => (val && val > 0) || 'Este campo es obligarorio']"
      />
      <q-input
        filled
        type="number"
        v-model="precioUnitario"
        label="Precio unitario"
        hint="precio de compra"
        bg-color="#363A4D"
        lazy-rules
        :rules="[(val) => (val && val >= 0) || 'Este campo es obligarorio']"
      />
      <q-input
        filled
        v-model="valorItem"
        type="number"
        label="Valtor item"
        hint="precio de
      venta"
        bg-color="#363A4D"
        lazy-rules
        :rules="[(val) => (val && val >= 0) || 'Este campo es obligarorio']"
      />
      <q-input
        filled
        type="text"
        v-model="codigoBarra"
        label="Codigo de barras"
        hint="Opcional"
        bg-color="#363A4D"
      >
        <template v-slot:append>
          <q-icon name="filter_center_focus" @click.stop="oelarva" />
        </template>
      </q-input>
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
    </q-form>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { ref } from "vue";
import rqts from "../myUtils/myUtils";

export default {
  setup() {
    const $q = useQuasar();
    const nombre = ref(null);
    const descripcion = ref(null);
    const stock = ref(null);
    const precioUnitario = ref(null);
    const valorItem = ref(null);
    const codigoBarra = ref(null);
    return {
      nombre,
      descripcion,
      stock,
      precioUnitario,
      valorItem,
      codigoBarra,
      async onSubmit(evt) {
        $q.loading.show({
          message: "Cargandoo...",
        });
        const producto = {
          nombre: nombre.value,
          descripcion: descripcion.value,
          stock: stock.value,
          precioUnitario: precioUnitario.value,
          valorItem: valorItem.value,
          codigoBarra: codigoBarra.value,
        };
        // modificar para notificar dependiendo si la creacion fue exitosa ofallo
        const response = await rqts
          .postjson("productos/nuevo/", producto)
          .then((response) =>
            $q.notify({
              color: "green-4",
              textColor: "white",
              icon: "cloud_done",
              message: response,
            })
          )
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
      },
      onReset() {
        nombre.value = "cocacola 1 L";
        descripcion.value = "bebida pulentamente de pana que toma la gente g";
        stock.value = 13;
        precioUnitario.value = 1200;
        valorItem.value = 1500;
        codigoBarra.value = 1234567;
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
    // background-color: $fondo
    background-color: $fondo-tabla
    padding: 1px 15px 15px 0px

.btn-container
    text-align: left
    margin-top: 20px

title
    width: 100%
</style>