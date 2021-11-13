<template>
  <div class="q-pa-md bruh fondo-blur1" style="max-width: 400px">
    <q-form
      action="http://146.83.216.218:8008/productos/nuevo/"
      method="post"
      @submit.prevent="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
    >
      <q-input
        filled
        v-model="nombre"
        label="Nombre del producto"
        hint="ej: Pepsi zero 3 L"
        bg-color="orange-1"
        lazy-rules
        :rules="[(val) => (val && val.length > 0) || 'Please type something']"
      />
      <q-input
        filled
        v-model="stock"
        type="number"
        label="Stock"
        hint="1, 6, 12, etc"
        bg-color="orange-1"
        lazy-rules
        :rules="[(val) => (val && val > 0) || 'Please type something']"
      />
      <q-input
        filled
        type="number"
        v-model="precioUnitario"
        label="Precio unitario"
        hint="precio de compra"
        bg-color="orange-1"
        lazy-rules
        :rules="[(val) => (val && val >= 0) || 'Please type something']"
      />
      <q-input
        filled
        v-model="valorItem"
        type="number"
        label="Valtor item"
        hint="precio de
      venta"
        bg-color="orange-1"
        lazy-rules
        :rules="[(val) => (val && val >= 0) || 'Please type something']"
      />
      <q-input
        filled
        type="text"
        v-model="codigoBarra"
        label="Codigo de barras"
        hint="opcional pero no me quejo si lo pones"
        bg-color="orange-1"
      >
        <template v-slot:append>
          <q-icon name="filter_center_focus" @click.stop="oelarva" />
        </template>
      </q-input>
      <div>
        <q-btn label="Submit" type="submit" color="primary" />
        <q-btn
          label="Reset"
          type="reset"
          color="primary"
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
export default {
  setup() {
    const $q = useQuasar();
    const nombre = ref(null);
    const stock = ref(null);
    const precioUnitario = ref(null);
    const valorItem = ref(null);
    const codigoBarra = ref(null);
    return {
      nombre,
      stock,
      precioUnitario,
      valorItem,
      codigoBarra,
      onSubmit(evt) {
        $q.notify({
          color: "green-4",
          textColor: "white",
          icon: "cloud_done",
          message: "Submitted",
        });
        // yo cacho que hay que hacer el submit alan tigua
        // para mostrar lo que responda el server como resultado
        // de la operacion
        evt.target.submit();
      },
      onReset() {
        nombre.value = null;
        stock.value = null;
        precioUnitario.value = null;
        valorItem.value = null;
        codigoBarra.value = null;
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
    color: aquamarine

.q-form
    border-radius: 12px
    // background-color: $fondo
    background-color: $fondo-tabla
    padding: 1px 15px 15px 0px
</style>