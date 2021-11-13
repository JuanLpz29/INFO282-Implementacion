
<template>
  <div class="q-pa-md fit">
    <q-layout
      view="hHh LpR fFf"
      container
      padding
      style="height: 84vh"
      class="shadow-2 rounded-borders row"
    >
      <q-drawer
        v-model="drawer"
        show-if-above
        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"
        :width="250"
        :breakpoint="400"
        bordered
      >
        <!-- <q-scroll-area class="fit"> -->
        <q-list padding>
          <q-item clickable v-ripple to="/app/productos/ver">
            <q-item-section avatar>
              <q-icon name="storefront" />
            </q-item-section>

            <q-item-section>
              <p class="centered">Ver Productos</p>
            </q-item-section>
          </q-item>

          <q-item active clickable v-ripple to="/app/productos/new">
            <q-item-section avatar>
              <q-icon name="add_circle_outline" />
            </q-item-section>

            <q-item-section>
              <p class="center">Agregar un producto</p>
            </q-item-section>
          </q-item>

          <q-separator />
        </q-list>
        <!-- </q-scroll-area> -->
      </q-drawer>

      <q-page-container>
        <q-page padding style="padding-top: 66px">
          <suspense>
            <template #default>
              <router-view />
            </template>
            <template #fallback>
              <div>Loading...</div>
            </template>
          </suspense>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  setup() {
    return {
      drawer: ref(false),
      miniState: ref(true),
    };
  },
};
</script>