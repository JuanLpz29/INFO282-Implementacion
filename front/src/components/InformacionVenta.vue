<template>
  <q-card class="my-card" flat bordered>
    <q-card-section horizontal>
      <q-item-section style="padding: 20px 30px">
        <q-item-label> {{ infoVenta.total }}</q-item-label>
        <q-item-label caption> {{ infoVenta.fecha ?? "fecha" }} </q-item-label>
      </q-item-section>

      <!-- <q-separator vertical /> -->
      <q-item>
        <q-item-section avatar>
          <q-avatar style="padding-left: 50px; margin: 15px 15px">
            <img
              src="https://e7.pngegg.com/pngimages/680/985/png-clipart-kirito-asuna-sword-art-online-drawing-anime-asuna-black-hair-computer-wallpaper.png"
            />
          </q-avatar>
        </q-item-section>

        <q-item-section style="padding: 20px 20px">
          <q-item-label> {{ infoUsuario.nombre }}</q-item-label>
          <q-item-label caption> {{ infoUsuario.rol }} </q-item-label>
        </q-item-section>
      </q-item>
    </q-card-section>

    <q-separator />

    <q-card-section horizontal>
      <q-item-section style="padding: 20px 20px; text-align: center">
        <q-item-label> Monto total: ${{ montoTotal }}</q-item-label>
      </q-item-section>
      <q-card-section> </q-card-section>
    </q-card-section>
  </q-card>
</template>


<script>
import { ref } from "vue";
export default {
  props: {
    infoVenta: Object,
    infoUsuario: Object,
  },

  setup(props) {
    return {
      infoVenta: ref(props.infoVenta),
      infoUsuario: ref(props.infoUsuario),
      montoTotal: ref(parseInt(props.infoVenta.total).toLocaleString()),
    };
  },
};
</script>

<style lang="sass" scoped>
.my-card
    width: min(500px, 60vh)
</style>