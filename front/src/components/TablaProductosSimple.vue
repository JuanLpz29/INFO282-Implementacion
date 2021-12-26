<template>
  <!-- <q-page style="min-height: 0vh; padding-left: 0px"> -->
  <div>
    <q-table
      title="Productos"
      :rows="items"
      :columns="columns"
      row-key="name"
      :filter="filter"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      class="text-primary"
    >
      <template v-slot:top-right>
        <div class="bg-white rounded-borders">
          <q-input
            borderless
            dense
            debounce="300"
            v-model="filter"
            placeholder="Filtrar"
            style="margin-left: 8px"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </template>
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
    </q-table>
    <!-- </q-page> -->
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    items: Array,
    columns: Array,
  },

  setup(props) {
    const columns = props.columns;
    return {
      columns,
      items: ref(props.items),
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 5,
      }),
    };
  },
};
</script>
