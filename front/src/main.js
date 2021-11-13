// FILE: main.js

import { createApp } from 'vue'
import { Quasar, Loading, Notify } from 'quasar'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

// Assumes your root component is App.vue
// and placed in same folder as main.js
import App from './App.vue'
import axios from 'axios'
import routes from './router/routes'
import { createRouter, createWebHashHistory } from 'vue-router'
const myApp = createApp(App)

const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

// Assumes you have a <div id="app"></div> in your index.html
myApp.use(Quasar, {
    plugins: { Loading, Notify }, // import Quasar plugins and add here
})

myApp.config.globalProperties.$http = axios
myApp.use(router)
myApp.mount('#app')