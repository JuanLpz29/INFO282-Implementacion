import LayoutOne from '../layouts/LayoutOne.vue'
import ComprasLayout from '../layouts/ComprasLayout.vue'
import ProductosLayout from '../layouts/ProductosLayout.vue'
import VentasLayout from '../layouts/VentasLayout.vue'

import VerCompras from '../pages/VerCompras.vue'
import SubirCompra from '../pages/SubirCompra.vue'
import Ventas from '../pages/Ventas.vue'
import VerVentas from '../pages/VerVentas.vue'
import VerProductos from '../pages/VerProductos.vue'
import NuevoProducto from '../pages/NuevoProducto.vue'
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
                    path: 'new',
                    component: NuevoProducto
                },
                {
                    path: 'ver',
                    component: VerProductos
                },
                ]
            },
            {
                path: 'ventas',
                component: VentasLayout,
                children: [{
                    path: 'ver',
                    component: Ventas
                },
                {
                    path: 'listado',
                    component: VerVentas
                }]
            },
            {
                path: '/',
                component: LandingNanachi
            },
        ]
    },

]
export default routes