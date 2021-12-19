<template>
  <q-card rounded class="shadow-24" style="width: 300px; height: 485px">
    <q-card-section class="bg-dark" style="height: 12vh">
      <h4 class="text-h5 text-white absolute-center">Iniciar Sesion</h4>
      <div class="absolute-top-right">
        <q-btn
          fab
          icon="close"
          color="purple-4"
          @click="$emit('close-dialog')"
        />
      </div>
    </q-card-section>
    <q-card-section>
      <q-form class="q-px-sm q-mt-lg">
        <q-input
          square
          clearable
          v-model="userref"
          type="username"
          label="Username"
        >
          <template v-slot:prepend>
            <q-icon name="person" />
          </template>
        </q-input>
        <q-input
          square
          clearable
          v-model="passref"
          type="password"
          label="Password"
          @keydown.enter.prevent="emitter(info)"
        >
          <template v-slot:prepend>
            <q-icon name="lock" />
          </template>
        </q-input>
      </q-form>
    </q-card-section>
    <q-card-actions class="q-px-lg">
      <q-btn
        unelevated
        size="lg"
        color="purple-4"
        class="full-width text-white"
        label="Comenzar"
        @click="emitter(info)"
      />
    </q-card-actions>
  </q-card>
</template>

<script>
import rqts from "../myUtils/myUtils";
import updateUsername from "../plugins/updateUsername";
import { ref, getCurrentInstance, reactive, toRef } from "vue";
export default {
  methods: {
    async emitter(info) {
      const succ = await rqts.loginxd(info.user, info.pass);
      if (succ.nombre !== undefined) {
        console.log(succ.nombre, succ.idUsuario);
        this.setCurrentUser(succ.nombre, succ.idUsuario);
        this.$emit("close-dialog");
      } else {
        alert(succ);
        info.pass = "";
      }
    },
  },

  name: "Login",
  setup() {
    const info = reactive({
      user: null,
      pass: null,
    });

    const userref = toRef(info, "user");
    const passref = toRef(info, "pass");
    const { currentUser, setCurrentUser } = updateUsername();
    return {
      info,
      userref,
      passref,
      setCurrentUser,
    };
  },
};
</script>

<style>
</style>