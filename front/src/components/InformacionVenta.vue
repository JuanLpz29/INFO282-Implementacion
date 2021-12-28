<template>
  <q-card class="my-card" flat bordered>
    <q-card-section horizontal>
      <q-item class="col">
        <q-item-section q-pa-md style="text-align: center">
          <q-item-label>
            Estado:
            <span class="text-bold"> {{ infoVenta.estado }} </span>
          </q-item-label>
          <q-item-label>
            Fecha:
            <span class="text-bold"> {{ fecha }} </span>
          </q-item-label>
          <q-item-label>
            Hora:
            <span class="text-bold"> {{ hora }} </span>
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item v-if="infoVenta.estado == 'Pagada'" class="col">
        <q-item-section q-pa-md style="text-align: center">
          <q-item-label>
            Medio de pago:
            <span class="text-bold"> {{ infoVenta.medioDePago }} </span>
          </q-item-label>
          <q-item-label>
            Documento emitido:
            <span class="text-bold"> (falta en el schema) </span>
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item bordered class="col" style="padding-left: 5vh">
        <q-item-section avatar q-pa-sm>
          <q-avatar>
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
        <q-item-label class="text-bold text-subtitle1">
          Monto total: ${{ montoTotal }}</q-item-label
        >
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
    console.log(props.infoVenta);
    console.log(props.infoUsuario);
    const dt = props.infoVenta.fecha;
    const dtParsed = new Date(Date.parse(dt + "Z")).toLocaleString("es-CL");
    let fecha, hora;
    [fecha, hora] = dtParsed.split(" ");
    return {
      fecha,
      hora,
      infoVenta: props.infoVenta,
      infoUsuario: props.infoUsuario,
      montoTotal: parseInt(props.infoVenta.total).toLocaleString(),
    };
  },
};
</script>

<style lang="sass" scoped>
.my-card
    width: 100%
</style>