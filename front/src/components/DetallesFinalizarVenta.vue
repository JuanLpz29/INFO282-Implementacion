<template>
  <div class="q-pa-md finalizar-compra-form">
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

      <div v-if="pagos == 'Efectivo'" style="padding-top: 25px">
        <q-form class="q-pa-md vuelto" @submit.prevent="calcularVuelto">
          <q-input
            outlined
            v-model="pago"
            :dense="dense"
            placeholder="Efectivo recibido"
          />
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
      </div>

      <div>
        <q-btn label="Finalizar venta" type="submit" color="positive" style="width: 100%; padding: 15px 20px"/>
      </div>
    </q-form>
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


