<template>
  <div class="q-pa-md column" style="height: 85vh">
    <div class="q-gutter-md" style="max-width: 300px">
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
        v-on:click="fileReady = !fileReady"
      />
    </div>

    <q-page-container v-if="fileReady" style="padding-top: 40px">
      <suspense>
        <template #default>
          <subir-archivo v-model:archivo="model" />
        </template>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </suspense>
    </q-page-container>
  </div>
</template>


<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import SubirArchivo from "../components/SubirArchivo.vue";

export default {
  components: { SubirArchivo },
  async setup() {
    const $q = useQuasar();
    return {
      btnOff: ref(true),
      fileReady: ref(false),
      model: ref(null),
      onRejected(rejectedEntries) {
        // Notify plugin needs to be installed
        // https://quasar.dev/quasar-plugins/notify#Installation
        $q.notify({
          type: "negative",
          message: `${rejectedEntries.length} file(s) did not pass validation constraints`,
        });
      },
      modelUpdated(value) {
        console.log("XD", value);
      },
    };
  },
};
</script>