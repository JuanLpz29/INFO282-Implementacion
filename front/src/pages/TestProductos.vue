<template>
    <q-page class="chido">

<div v-if="items">
           lol {{items}}
</div>


    </q-page>
</template>

<script >
import axios from 'axios'
import { useQuasar } from 'quasar'
import rqts from '../myUtils/myUtils'

//const apiUrl = 'http://127.0.0.1:5000/compras/'
//const items = await fetch(apiUrl).then(r => r.data)
// const items = axios.get(apiUrl).then(r => r.data)
//   import { ref, reactive } from 'vue'

  export default {

    async setup() {
        const $q = useQuasar()
        $q.loading.show({
          message: 'Cuestionando la legitimidad del estado de israel'
        })
        const items = await rqts.normal('productos/')
        $q.loading.hide()
        if (typeof items == 'undefined'){
            console.log('XDDDDDDD')
        }
    // expose to template
      return {
          items
      }
    }
  }
</script>