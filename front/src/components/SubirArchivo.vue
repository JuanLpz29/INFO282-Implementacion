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
import rqts from '../myUtils/myUtils'

export default {
    props: {
        archivo: Object
    },
  async setup (props) {
    const $q = useQuasar()
    $q.loading.show({
          message: 'Esperando las notas de redes...'
    })
    const formData = new FormData();
    formData.append('file', props.archivo);

    const response = await rqts.post('compras/upload',
                                  formData).catch((e) => {
                                                    console.log(e);
                                                        });
    $q.loading.hide()
    console.log(response);
    let info
    let productos
    if (typeof response !== 'undefined'){
        info = response.info
        productos = response.productos
    }
    console.log(productos)
    console.log(info)

    return{
        info,
        productos
    }
  } 
}
</script>
