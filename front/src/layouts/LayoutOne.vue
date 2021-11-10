<template>
  <q-layout view="hHh LpR fFf" style="min-height: 0px;">

    <q-header bordered class="bg-light-green-7 text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Miselio
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab to="/" label="Home" />
        <q-route-tab to="/app/compras" label="Compras" />
        <q-route-tab to="/app/productos" label="Productos"/>
        <q-route-tab to="/app/ventas" label="Ventas"/>
        <q-route-tab to="/app/poto" label="Poto"/>

        <q-space/>
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
                  <q-item-section>es el perro jorge, el perro que no ladra, el perro que habla</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
        </q-btn>

      </q-tabs>
    </q-header>

    <q-page-container style="padding-top: 40px;">
      <suspense>
        <template #default>
        <router-view />
        </template>
        <template #fallback>
        <div>
            Loading...
        </div>
        </template>
      </suspense>
    </q-page-container>

  </q-layout>
</template>


<script>
import { useQuasar } from 'quasar'
export default {
    setup() {
        const $q = useQuasar()
        //$q.dark.set(true)
    },
}
</script>