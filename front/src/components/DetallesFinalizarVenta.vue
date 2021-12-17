<template>
  <div class="q-pa-md finalizar-compra-form">
    <!-- <q-form class="q-gutter-md" @submit.prevent="onSubmit"> -->
    <q-select
      outlined
      v-model="medio"
      :options="mediosDePago"
      label="Medios de pago"
      emit-value
    />

    <q-select
      outlined
      v-model="documento"
      :options="tipoDeDocumento"
      label="Tipo de documento"
    />

    <div v-if="medio == 'Efectivo'" style="padding-top: 25px">
      <q-form class="q-pa-md vuelto">
        <q-input
          outlined
          v-model="monto"
          :dense="dense"
          placeholder="Efectivo recibido"
        />
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
          ${{ (monto - total > 0 ? monto - total : 0).toLocaleString() }}
        </div>
      </div>
    </div>

    <div>
      <q-btn
        label="Finalizar venta"
        type="submit"
        color="positive"
        style="width: 100%; padding: 15px 20px"
        @click="$emit('enlargeText', medio)"
        v-close-popup
      />
    </div>
    <!-- </q-form> -->
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
  emits: ["enlargeText"],
  setup(props) {
    const $q = useQuasar();
    const accept = ref(false);
    const medio = ref(null);
    const vuelto = ref(0);
    const monto = ref(0);

    return {
      total: ref(props.total),
      accept,
      medio,
      vuelto,
      monto,
      pagos: ref(null),
      documento: ref(null),
      mediosDePago: ["Efectivo", "Debito", "Credito", "Fiado"],
      tipoDeDocumento: ["Boleta", "Factura", "Guia de despacho"],

      methods: {
        submitForm(email, password) {
          this.$emit("enlargeText", medio.value);
        },
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


