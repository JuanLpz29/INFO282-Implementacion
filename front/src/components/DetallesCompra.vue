<template>
  <!-- <q-page class="chido"> -->
  <q-page style="min-height: 60vh">
    <q-page-container class="q-pa-md" style="padding-left: 16px">
      <informacion-compra :infoCompra="info" :infoProveedor="proveedor" />
    </q-page-container>
    <q-page-container class="q-pa-md" style="padding-left: 16px">
      <tabla-productos-simple
        :columns="columns"
        :items="productos"
        :esVenta="false"
      />
    </q-page-container>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import TablaProductosSimple from "./TablaProductosSimple.vue";
import InformacionCompra from "./InformacionCompra.vue";

const columns = [
  {
    name: "nombre",
    required: true,
    label: "Nombre",
    align: "left",
    field: (row) => row.nombre,
    format: (val) => `${val}`,
    sortable: true,
    style: "width: 30vh",
    headerStyle: "width: 35vh",
  },
  {
    name: "cantidad",
    label: "Cantidad",
    field: "cantidad",
    sortable: true,
    style: "width: 20",
    headerStyle: "width: 20vh",
    align: "center",
  },
  {
    name: "precioUnitario",
    align: "center",
    label: "Precio Unitario",
    field: "precioUnitario",
    format: (val) =>
      isNaN(parseInt(val)) ? `$0` : `$${parseInt(val).toLocaleString()}`,
    sortable: true,
    style: "width: 25vh",
    headerStyle: "width: 22vh",
    align: "center",
  },
  {
    name: "precioVenta",
    align: "center",
    label: "Precio venta",
    field: "precioVenta",
    format: (val) =>
      isNaN(parseInt(val)) ? `$0` : `$${parseInt(val).toLocaleString()}`,
    sortable: true,
    style: "width: 25vh",
    headerStyle: "width: 22vh",
    align: "center",
  },
];
export default {
  components: { TablaProductosSimple, InformacionCompra },
  props: {
    idCompra: Number,
  },
  async setup(props) {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargandoo...",
    });

    const response = await rqts.get("compras/" + props.idCompra + "/");
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
      columns,
      info,
      productos,
      proveedor,
    };
  },
};
</script>

