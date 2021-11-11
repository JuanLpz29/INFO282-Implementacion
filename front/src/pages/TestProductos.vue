<template>
    <q-page class="chido">

<div v-if="items">
           lol {{items}}
</div>


    </q-page>
</template>

<script >
import { useQuasar } from 'quasar'
import rqts from '../myUtils/myUtils'

  export default {

    async setup() {
        const $q = useQuasar()
        $q.loading.show({
          message: 'Cuestionando la legitimidad del estado de israel'
        })
        const items = await rqts.get('productos/')
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