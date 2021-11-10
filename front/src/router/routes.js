import LayoutOne from '../layouts/LayoutOne.vue'
import ComprasLayout from '../layouts/ComprasLayout.vue'
import ProductosLayout from '../layouts/ProductosLayout.vue'
import GoogleLayout from '../layouts/GoogleLayout.vue'

import VerCompras from '../pages/VerCompras.vue'
import SubirCompra from '../pages/SubirCompra.vue'
import Ventas from '../pages/Ventas.vue'
import VerProductos from '../pages/VerProductos.vue'
import TestProductos from '../pages/TestProductos.vue'
import TablaProductos from '../pages/TablaProductos.vue'
import LandingNanachi from '../pages/LandingNanachi.vue'

const routes = [
    {
        path: '/app',
        component: LayoutOne,
        // hey, it has children routes and User has <router-view> in it;
        // It is really a Layout then!
        children: [
            {
                path: 'compras', // here it is, route /compras
                component: ComprasLayout,
                children: [{
                    path: 'ver',
                    component: VerCompras
                },
                {
                    path: 'subir',
                    component: SubirCompra
                }]

            },
            {
                path: 'productos',
                component: ProductosLayout,
                children: [{
                    path: 'ver',
                    component: VerProductos
                },
                {
                    path: 'tabla',
                    component: TablaProductos
                },
                {
                    path: 'testing',
                    component: TestProductos
                }
                ]
            },
            {
                path: 'ventas',
                component: Ventas
            },
            {
                path: '/',
                component: LandingNanachi
            },
            {
                path: '/app/poto',
                component: GoogleLayout
            }
        ]
    },

]
export default routes