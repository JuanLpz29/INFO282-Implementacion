<template>
  <div class="q-pa-md">
    <q-layout view="hHh Lpr lff" container style="height: 85vh" class="shadow-2 rounded-borders">
      <q-header elevated class="bg-black">
        <q-toolbar>
          <q-btn flat @click="drawer = !drawer" round dense icon="menu" />
          <q-toolbar-title>Header</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="drawer"
        show-if-above

        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"

        :width="200"
        :breakpoint="500"
        bordered
        class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <q-list padding>
            <q-item clickable v-ripple to="/app/compras/ver">
              <q-item-section avatar>
                <q-icon name="inbox" />
              </q-item-section>

              <q-item-section>
                Ver Compras
              </q-item-section>
            </q-item>

            <q-item active clickable v-ripple to="/app/compras/subir">
              <q-item-section avatar>
                <q-icon name="star" />
              </q-item-section>

              <q-item-section>
                Subir un documento
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple to="/">
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                NaNaChi
              </q-item-section>
            </q-item>

            <q-separator />
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <router-view>

        </router-view>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  setup () {
    return {
      drawer: ref(false),
      miniState: ref(true)
    }
  }
}
</script>