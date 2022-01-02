<template>
  <q-card class="my-card" flat bordered>
    <q-card-section horizontal>
      <q-item class="col-5">
        <q-item-section q-pa-md style="text-align: center">
          <q-item-label> {{ infoCompra.tipoDocumento }}</q-item-label>
          <q-item-label> Folio: {{ infoCompra.folio }}</q-item-label>
          <q-item-label caption>
            {{ infoCompra.fecha.split("-").reverse().join("-") }}
          </q-item-label>
        </q-item-section>
      </q-item>
      <!-- <q-separator vertical /> -->
      <q-item class="col" style="padding-left: 5vh">
        <q-item-section avatar q-pa-sm>
          <q-avatar>
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/1/19/CCU_LOGO.png"
            />
          </q-avatar>
        </q-item-section>
      </q-item>
      <q-item class="col-5">
        <q-item-section q-pa-md style="text-align: center">
          <q-item-label> {{ nombreProveedor }}</q-item-label>
          <q-item-label caption> {{ infoProveedor.rut }} </q-item-label>
        </q-item-section>
      </q-item>
    </q-card-section>

    <q-card-section horizontal v-if="registrada">
      <q-item-section q-pa-md style="text-align: center">
        <q-item-label caption>
          La compra ya se encuentra registrada en el sistema.
        </q-item-label>
      </q-item-section>
    </q-card-section>
    <q-separator />

    <q-card-section horizontal class="q-pa-md" style="text-align: center">
      <q-item-section>
        <q-item-label caption>
          Monto neto: ${{ montoNeto.toLocaleString() }}
        </q-item-label>
      </q-item-section>
      <q-item-section>
        <q-item-label caption> IVA: ${{ iva.toLocaleString() }} </q-item-label>
      </q-item-section>
      <q-item-section v-if="impAdicional">
        <q-item-label caption>
          Impuestos adicionales: ${{ impAdicional.toLocaleString() }}
        </q-item-label>
      </q-item-section>
    </q-card-section>
    <q-item-section class="q-pa-sm" style="text-align: center">
      <q-item-label>
        Monto total: ${{ montoTotal.toLocaleString() }}</q-item-label
      >
    </q-item-section>
  </q-card>
</template>

<script>
export default {
  props: {
    infoCompra: Object,
    infoProveedor: Object,
    registrada: Boolean,
  },

  setup(props) {
    const registrada = props.registrada;
    const nombreProveedor = props.infoProveedor.razonSocial;
    const montoNeto = parseInt(props.infoCompra.montoNeto);
    const montoTotal = parseInt(props.infoCompra.montoTotal);
    const iva = Math.round(montoNeto * 0.19);
    const _impAdicional = montoTotal - montoNeto - iva;
    const impAdicional = _impAdicional > 30 ? _impAdicional : null;
    return {
      registrada,
      nombreProveedor,
      infoCompra: props.infoCompra,
      infoProveedor: props.infoProveedor,
      montoTotal,
      montoNeto,
      iva,
      impAdicional,
    };
  },
};
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
</style>
