<template>
  <div class="q-pa-md column container" style="height: 85vh">
    <div class="q-gutter-md izquierda" style="max-width: 300px">
      <q-file
        outlined
        bottom-slots
        v-model="model"
        label="Mi_DTE.xml"
        accept=".xml"
        bg-color="orange-1"
        filled
        counter
        max-files="1"
        @update:model-value="modelUpdated"
      >
        <template v-slot:before>
          <q-icon name="attachment" />
        </template>

        <template v-slot:append>
          <q-icon
            v-if="model !== null"
            name="close"
            @click.stop="model = null"
            class="cursor-pointer"
          />
          <q-icon name="search" @click.stop />
        </template>

        <template v-slot:hint> Archivos XML </template>
      </q-file>

      <!-- activar boton cuando el usuario haya subido un archivo valido     -->
      <q-btn
        :disabled="model == null"
        color="light-green-7"
        label="Upload File"
        v-on:click="getInfo(model, productos)"
      />
    </div>
    <div class="derecha">
      {{ info }}
      {{ proveedor }}
    </div>
    <div class="poto">
      <q-page-container v-if="productos" style="padding-top: 40px">
        <productos-compra :items="productos" />
      </q-page-container>
      <div v-if="productos !== null" class="row justify-end">
        <q-btn
          :disabled="productos == null"
          class="q-mt-md"
          color="light-green-7"
          label="Subir compra"
          v-on:click="postJson(productos)"
        >
        </q-btn>
      </div>
    </div>

    <div v-if="productos">
      <q-btn class="right" />
    </div>
  </div>
</template>


<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import ProductosCompra from "./ProductosCompra.vue";

export default {
  components: { ProductosCompra },
  async setup() {
    const $q = useQuasar();
    return {
      btnOff: ref(true),
      info: ref(null),
      productos: ref(null),
      registrada: ref(false),
      proveedor: ref(null),
      fileReady: ref(false),
      model: ref(null),
      onRejected(rejectedEntries) {
        // Notify plugin needs to be installed
        // https://quasar.dev/quasar-plugins/notify#Installation
        fileReady = false;
        $q.notify({
          type: "negative",
          message: `${rejectedEntries.length} file(s) did not pass validation constraints`,
        });
      },
      modelUpdated(value, productos) {
        console.log("XD", value);
      },
      async getInfo(model) {
        $q.loading.show({
          message: "Esperando...",
        });
        const formData = new FormData();
        formData.append("file", model);
        const response = await rqts
          .post("compras/documento", formData)
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
        console.log(response);
        if (typeof response !== "undefined") {
          this.info = response.info;
          this.productos = response.productos;
          this.proveedor = response.proveedor;
          this.registrada = response.registrada;
        }
        // this.fileReady = false;
        this.model = null;
      },
      async postJson() {
        $q.loading.show({
          message: "xd...",
        });
        const compra = {
          info: this.info,
          proveedor: this.proveedor,
          productos: this.productos,
          registrada: this.registrada,
        };
        // modificar para notificar dependiendo si la creacion fue exitosa ofallo
        const response = await rqts
          .postjson("compras/upload", compra)
          .then((response) =>
            $q.notify({
              color: "green-4",
              textColor: "white",
              icon: "cloud_done",
              message: response,
            })
          )
          .catch((e) => {
            console.log(e);
          });
        $q.loading.hide();
      },
    };
  },
};
</script>

<style>
.container {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  grid-template-rows: min-content;
  grid-auto-columns: 1fr;
  gap: 25px 0px;
  grid-auto-flow: row;
  grid-template-areas:
    "izquierda derecha"
    "poto poto";
}

.poto {
  grid-area: poto;
}

.izquierda {
  grid-area: izquierda;
}

.derecha {
  grid-area: derecha;
}
</style>