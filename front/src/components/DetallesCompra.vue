<template>
  <!-- <q-page class="chido"> -->
  <q-page style="min-height: 60vh">
    <q-page-container style="padding-top: 25px; padding-left: 32px">
      <informacion-compra :infoCompra="info" :infoProveedor="proveedor" />
    </q-page-container>
    <q-page-container style="padding-top: 25px; padding-left: 25px">
      <tabla-productos-simple :items="productos" :esVenta="false" />
    </q-page-container>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import TablaProductosSimple from "./TablaProductosSimple.vue";
import InformacionCompra from "./InformacionCompra.vue";
import ProductosCompra from "./ProductosCompra.vue";

export default {
  components: { TablaProductosSimple, InformacionCompra, ProductosCompra },
  props: {
    idCompra: Number,
  },
  async setup(props) {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargandoo...",
    });

    const response = await rqts
      .get("compras/" + props.idCompra + "/") /*.then(r => r.items)*/
      .catch((e) => {
        console.log(e);
      });
    $q.loading.hide();
    console.log(response);
    let info;
    let productos;
    let proveedor;
    if (typeof response !== "undefined") {
      info = response.info;
      productos = response.productos;
      proveedor = response.proveedor;
    }
    return {
      info,
      productos,
      proveedor,
    };
  },
};
</script>

