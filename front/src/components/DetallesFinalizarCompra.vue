<template>
  <div class="q-pa-md finalizar-compra-form" style="max-width: 1000px">
    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-select
        outlined
        v-model="pagos"
        :options="mediosDePago"
        label="Medios de pago"
      />

      <q-select
        outlined
        v-model="documento"
        :options="tipoDeDocumento"
        label="Tipo de documento"
      />

      <div>
        <q-btn label="Finalizar venta" type="submit" color="dark" />
      </div>
    </q-form>
    <!-- acá deberia ir el if de si la opcion es efectivo -->
    <!-- <q-page-container
      v-if="pagos.value == 'efectivo' "
      style="padding-top: 25px; padding-left: 25px"
    > -->
      <q-form class="q-pa-md vuelto" @submit.prevent="calcularVuelto">
        <q-input outlined v-model="pago" :dense="dense" />
        <q-btn label="vuelto" type="submit" color="dark" />
      </q-form>
      <div
        style="
          display: flex;
          justify-content: space-between;
          margin-bottom: 10px;
        "
      >
        <div class="text-h6">Monto a pagar:</div>
        <div class="text-h5">${{ total.toLocaleString() }}</div>
      </div>

      <div style="display: flex; justify-content: space-between">
        <div class="text-h6" style="font-weight: bold">Vuelto:</div>
        <div class="text-h5" style="color: red">
          ${{ vuelto.toLocaleString() }}
        </div>
      </div>
    <!-- </q-page-container> -->
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { ref, getCurrentInstance } from "vue";
import rqts from "../myUtils/myUtils";

export default {
  props: {
    total: Number,
  },

  setup(props) {
    const $q = useQuasar();
    const accept = ref(false);
    const pago = ref(null);
    const vuelto = ref(0);

    return {
      total: ref(props.total),
      accept,
      pago,
      vuelto,
      pagos: ref(null),
      documento: ref(null),
      mediosDePago: ["Efectivo", "Debito", "Credito", "Fiado"],
      tipoDeDocumento: ["Boleta", "Factura", "Guia de despacho"],

      async onSubmit() {
        $q.loading.show({
          message: "Cargando...",
        });
      },

      calcularVuelto() {
        vuelto.value = pago.value - props.total;
        console.log(vuelto);
      },
    };
  },
};
</script>

<style lang="sass">
@import '../quasar-variables.sass'
.vuelto
  display: flex
</style>


