<template>
  <q-layout view="hHh LpR fFf" style="min-height: 0px">
    <q-header bordered class="bg-dark texto" height-hint="120">
      <q-toolbar>
        <q-toolbar-title class="text-primary"> La Tentación </q-toolbar-title>
      </q-toolbar>

      <!-- <q-tabs align="left"> -->
      <q-tabs>
        <div v-if="currentUser" class="row" align="left">
          <q-route-tab to="/" label="Home" class="text-primary" />
          <q-route-tab to="/app/compras" label="Compras" class="text-primary" />
          <q-route-tab
            to="/app/productos"
            label="Productos"
            class="text-primary"
          />
          <q-route-tab
            to="/app/ventas/nueva"
            label="Ventas"
            class="text-primary"
          />
        </div>
        <q-space />
        <!-- <q-toggle
          :label="`switch ${blueModel}`"
          v-model="blueModel"
          color="purple-12"
          false-value="off"
          true-value="ON"
          @update:model-value="modelUpdated"
        /> -->
        <!-- <q-tabs align="right"> -->
        <q-item clickable class="right" @click="opciones">
          <q-menu v-if="currentUser" auto-close :offset="[0, 0]">
            <q-list style="min-width: 150px">
              <q-item clickable>
                <q-item-section>Mi cuenta (nada aun)</q-item-section>
              </q-item>
              <q-item clickable @click="logOutUser">
                <q-item-section>Cerrar sesion</q-item-section>
              </q-item>
            </q-list>
          </q-menu>

          <q-item-section avatar>
            <q-icon round flat name="manage_accounts" style="font-size: 32px" />
          </q-item-section>
          <div v-if="currentUser">Hola, {{ currentUser }}!</div>
          <div v-else>Iniciar sesion</div>
        </q-item>
      </q-tabs>
    </q-header>

    <q-page-container style="padding-top: 40px">
      <q-dialog v-model="fixed" transition-hide="rotate">
        <nuevo-login @close-dialog="fixed = false" />
      </q-dialog>
      <suspense>
        <template #default>
          <router-view v-if="currentUser" />
        </template>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </suspense>
    </q-page-container>
  </q-layout>
</template>


<script>
import { ref, watch } from "vue";
import updateUsername from "../plugins/updateUsername";
import NuevoLogin from "../components/NuevoLogin.vue";
export default {
  components: { NuevoLogin },
  setup() {
    const { currentUser, setCurrentUser } = updateUsername();
    const info = ref(null);
    const fixed = ref(false);
    // function updateOnSucc(user, pass) {
    //   const succ = rqts.loginxd(info.user, info.pass);
    //   console.log(succ);
    // }
    watch(info, (info, prevCount) => {
      console.log("deweltaaaa");
      if (typeof info == String) {
        alert("error en las credenciales");
      } else {
        console.log("el usuario", info.nombre);
        setCurrentUser(info.nombre);
      }
    });
    return {
      currentUser,
      fixed,
      info,
      logOutUser() {
        setCurrentUser("");
      },
      opciones() {
        console.log(currentUser.value);
        if (currentUser.value) {
          console.log("opcion 1");
        } else {
          console.log("opcion 2");
          fixed.value = true;
        }
      },
    };
  },
};
</script>