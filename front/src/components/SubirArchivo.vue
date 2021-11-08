<template>
    <q-page class="chido">

            {{ info }}

            {{ productos }}

    </q-page>
</template>


<script>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios';

export default {
    props: {
        archivo: Object
    },
  async setup (props) {
    async function upload(formdata) {
        const response = await axios.post('http://127.0.0.1:5000/compras/upload', formdata)
        return response.data;
    }
    const $q = useQuasar()
    $q.loading.show({
          message: 'Esperando las notas de redes...'
    })
    const formData = new FormData();
    formData.append('file', props.archivo);
    const response = await upload(formData)
    $q.loading.hide()
    const info = response.info
    const productos = response.productos
    console.log(productos)
    return{
        info,
        productos
    }
  } 
}
</script>
