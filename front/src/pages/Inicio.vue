<template>
  <div class="q-pa-md">
    <q-layout view="hHh Lpr lff" container style="height: 300px" class="shadow-2 rounded-borders">
      <q-header elevated class="bg-black">
        <q-toolbar>
          <q-btn flat @click="drawer = !drawer" round dense icon="menu" />
          <q-toolbar-title>Header</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="drawer"
        show-if-above
        :width="200"
        :breakpoint="500"
        bordered
        class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <q-list>

            <template v-for="(menuItem, index) in menuList" :key="index">
              <q-item clickable :active="menuItem.label === 'Outbox'" v-ripple>
                <q-item-section avatar>
                  <q-icon :name="menuItem.icon" />
                </q-item-section>
                <q-item-section>
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
              <q-separator :key="'sep' + index"  v-if="menuItem.separator" />
            </template>

          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <q-page padding>
        <suspense>
            <template #default>
            <compras-vue />
            </template>
            <template #fallback>
            <div>
                Loading...
            </div>
            </template>
        </suspense>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { ref } from 'vue'
import Compras from './VerCompras.vue'
const menuList = [
  {
    icon: 'inbox',
    label: 'Inbox',
    separator: true
  },
  {
    icon: 'send',
    label: 'Outbox',
    separator: false
  },
  {
    icon: 'delete',
    label: 'Trash',
    separator: false
  }
]
export default {
  setup () {
    return {
      drawer: ref(false),
      menuList
    }
  }
}
</script>