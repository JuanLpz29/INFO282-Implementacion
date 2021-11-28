<template>
  <q-page class="chido">
    {{ info }}

    {{ proveedor }}

    <q-page-container style="padding-top: 40px">
      <tabla-productos-simple :items="productos" />
    </q-page-container>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import TablaProductosSimple from "./TablaProductosSimple.vue";

export default {
  components: { TablaProductosSimple },
  props: {
    idCompra: Number,
  },
  async setup(props) {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargandoo...",
    });

    const response = await rqts
      .get("compras/details/" + props.idCompra + "/")
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

