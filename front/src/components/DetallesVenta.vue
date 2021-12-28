<template>
  <!-- <q-page class="chido"> -->
  <q-page style="min-height: 60vh">
    <q-page-container style="padding-top: 25px; padding-left: 32px">
      <informacion-venta :infoVenta="info" :infoUsuario="vendedor" />
    </q-page-container>
    <q-page-container style="padding-top: 25px; padding-left: 25px">
      <tabla-productos-simple :items="productos" :columns="columns" />
    </q-page-container>
  </q-page>
</template>

<script>
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import TablaProductosSimple from "./TablaProductosSimple.vue";
import InformacionVenta from "./InformacionVenta.vue";

const columns = [
  {
    name: "nombre",
    required: true,
    label: "Nombre",
    align: "left",
    field: (row) => row.nombre,
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
    name: "precioVenta",
    align: "center",
    label: "Precio venta",
    field: "precioVenta",
    sortable: true,
    style: "width: 25vh",
    headerStyle: "width: 22vh",
    align: "center",
  },
  {
    name: "subtotal",
    align: "center",
    label: "Subtotal",
    field: (row) => row.precioVenta * row.cantidad,
    sortable: true,
    style: "width: 25vh",
    headerStyle: "width: 22vh",
    align: "center",
  },
];

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
      .get("ventas/" + props.idVenta + "/")
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
      columns,
      info,
      productos,
      vendedor,
    };
  },
};
</script>
