<template>
    <q-page class="chido">

           lol {{items}}

    </q-page>
</template>

<script >
import axios from 'axios'
import { useQuasar } from 'quasar'
//const apiUrl = 'http://127.0.0.1:5000/compras/'
//const items = await fetch(apiUrl).then(r => r.data)
// const items = axios.get(apiUrl).then(r => r.data)
//   import { ref, reactive } from 'vue'

  export default {

    async setup() {
        const $q = useQuasar()
        $q.loading.show({
          message: 'Quemando el arduino...'
        })
        const apiUrl = 'http://127.0.0.1:5000/compras/'
        const items = await axios.get(apiUrl).then(r => r.data)
                                .catch(e => 
                                        {console.log(e);
                                        $q.loading.hide()
                                        })
        console.log(items)
        $q.loading.hide()
      // expose to template
      return {
          items
      }
    }
  }
</script>