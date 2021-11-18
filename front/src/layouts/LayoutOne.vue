<template>
  <q-layout view="hHh LpR fFf" style="min-height: 0px">
    <q-header bordered class="bg-dark texto" height-hint="120">
      <q-toolbar>
        <q-toolbar-title class="text-primary">
          <q-avatar>
            <img src=" https://i.redd.it/okazwxmx2aw31.png" />
          </q-avatar>
          Miselio
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab to="/" label="Home" class="text-primary" />
        <q-route-tab to="/app/compras" label="Compras" class="text-primary" />
        <q-route-tab
          to="/app/productos"
          label="Productos"
          class="text-primary"
        />
        <q-route-tab to="/app/ventas" label="Ventas" class="text-primary" />
        <q-space />
        <q-toggle
          :label="`Modo sexo is ${blueModel}`"
          v-model="blueModel"
          color="purple-12"
          false-value="off"
          true-value="ON"
          @update:model-value="modelUpdated"
        />
        <q-btn round flat icon="manage_accounts" class="right">
          <q-menu auto-close :offset="[110, 0]">
            <q-list style="min-width: 150px">
              <q-item clickable>
                <q-item-section>Mi cuenta</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Cerrar sesion</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section
                  >es el perro jorge, el perro que no ladra, el perro que
                  habla</q-item-section
                >
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-tabs>
    </q-header>

    <q-page-container style="padding-top: 40px">
      <suspense>
        <template #default>
          <router-view />
        </template>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </suspense>
    </q-page-container>
  </q-layout>
</template>


<script>
import { ref } from "vue";
import { useQuasar, setCssVar } from "quasar";
export default {
  setup() {
    const $q = useQuasar();
    //$q.dark.set(true)
    return {
      blueModel: ref("ON"),
      modelUpdated(value) {
        if (value == "ON") {
          console.log("SEXOOO");
          setCssVar("primary", "#ec8bdc");
          //   setCssVar("dark", "#ffffff");
          //   setCssVar("bg-file", "src/assets/bg2.png");
        } else {
          console.log("off");
          setCssVar("primary", "#31CCEC");
          setCssVar("dark", "#051a21");
        }
      },
    };
  },
};
</script>