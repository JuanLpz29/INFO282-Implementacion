<template>
  <!-- <q-page class="chido"> -->
  <q-page style="min-height: 60vh">
    <q-page-container style="padding-top: 25px; padding-left: 32px">
      <informacion-venta :infoVenta="info" :infoUsuario="vendedor" />
    </q-page-container>
    <q-page-container style="padding-top: 25px; padding-left: 25px">
      <tabla-productos-simple :items="productos" :esVenta="true" />
    </q-page-container>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import TablaProductosSimple from "./TablaProductosSimple.vue";
import InformacionVenta from "./InformacionVenta.vue";

export default {
  components: { TablaProductosSimple, InformacionVenta },
  props: {
    idVenta: Number,
  },
  async setup(props) {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargandoo...",
    });

    const response = await rqts
      .get("ventas/details/" + props.idVenta + "/")
      .catch((e) => {
        console.log(e);
      });
    $q.loading.hide();
    console.log(response);
    let info;
    let productos;
    let vendedor;
    if (typeof response !== "undefined") {
      info = response.info;
      productos = response.productos;
      vendedor = response.vendedor;
    }
    return {
      info,
      productos,
      vendedor,
    };
  },
};
</script>
