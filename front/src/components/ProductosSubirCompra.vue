<template>
  <q-page style="min-height: 0; padding-top: 25">
    <!-- <div class="q-pa-md"> -->
    <q-table
      title="Productos de la Compra"
      :rows="items"
      :columns="mycolumns"
      :filter="filter"
      row-key="name"
      binary-state-sort
      separator="horizontal"
      v-model:pagination="pagination"
      :rows-per-page-options="[0]"
      style="table-layout: fixed"
      wrap-cells
      class="text-primary"
      v-model="myrows"
      @update:model-value="modelUpdated"
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

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="nombre" :props="props">
            {{ props.row.nombre }}
            <q-popup-edit v-model="props.row.nombre">
              <q-input
                v-model="props.row.nombre"
                dense
                type="textarea"
                autofocus
                counter
              />
            </q-popup-edit>
          </q-td>

          <q-td key="precioUnitario" :props="props">
            ${{ props.row.precioUnitario.toLocaleString() }}
          </q-td>

          <q-td key="stock" :props="props">
            {{ props.row.stock }}
            <span v-if="props.row.formato"> {{ props.row.formato }}</span>
            <!-- <q-popup-edit
              v-model="props.row.stock"
              :validate="(val) => val > 0"
              :cover="false"
              :offset="[-10, -10]"
            >
              <template v-slot="scope">

                <q-input
                  autofocus
                  dense
                  v-model="scope.value"
                  :model-value="scope.value"
                  hint="Cantidad a ingresar"
                  :rules="[
                    (val) =>
                      scope.validate(scope.value) ||
                      'Debe ingresar una cantidad mayor que cero',
                  ]"
                >

                  <template v-slot:after>
                    <q-btn
                      flat
                      dense
                      color="negative"
                      icon="cancel"
                      @click.stop="scope.cancel"
                    />

                    <q-btn
                      flat
                      dense
                      color="positive"
                      icon="check_circle"
                      @click.stop="scope.set"
                      :disable="
                        scope.validate(scope.value) === false ||
                        scope.initialValue === scope.value
                      "
                    />
                  </template>
                </q-input>

              </template>
            </q-popup-edit> -->
          </q-td>

          <q-td key="valorItem" :props="props">
            ${{ props.row.valorItem.toLocaleString() }}
          </q-td>

          <q-td key="precioVenta" :props="props">
            <q-badge color="light-blue-3">
              ${{ props.row.precioVenta.toLocaleString() }}
              <q-popup-edit
                v-model="props.row.precioVenta"
                :validate="(val) => val > 0"
                :cover="false"
                :offset="[-10, -10]"
              >
                <template v-slot="scope">
                  <q-input
                    autofocus
                    dense
                    v-model="scope.value"
                    :model-value="scope.value"
                    hint="Ingrese precio de venta"
                    :rules="[
                      (val) =>
                        scope.validate(scope.value) ||
                        'Debe ingresar un precio mayor que cero',
                    ]"
                  >
                    <template v-slot:after>
                      <q-btn
                        flat
                        dense
                        color="negative"
                        icon="cancel"
                        @click.stop="scope.cancel"
                      />

                      <q-btn
                        flat
                        dense
                        color="positive"
                        icon="check_circle"
                        @click.stop="scope.set"
                        :disable="
                          scope.validate(scope.value) === false ||
                          scope.initialValue === scope.value
                        "
                      />
                    </template>
                  </q-input>
                </template>
              </q-popup-edit>
            </q-badge>
          </q-td>

          <q-td key="descripcion" :props="props">
            <div class="text-pre-wrap">{{ props.row.descripcion }}</div>
            <q-popup-edit v-model="props.row.descripcion">
              <q-input
                type="textarea"
                v-model="props.row.descripcion"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <!-- </div> -->
  </q-page>
</template>

<script>
import { ref } from "vue";

const mycolumns = [
  {
    name: "nombre",
    required: true,
    label: "Nombre",
    align: "left",
    field: (row) => row.nombre,
    format: (val) => `${val}`,
    sortable: true,
    style: "width: 35vh",
    headerStyle: "width: 35vh",
  },

  {
    name: "precioUnitario",
    align: "center",
    label: "Precio Unitario",
    field: "precioUnitario",
    format: (val) => `${parseInt(val).toLocaleString()}`,
    sortable: true,
    style: "width: 12vh",
    headerStyle: "width: 12vh",
    align: "center",
  },
  {
    name: "stock",
    label: "Cantidad",
    field: "stock",
    sortable: true,
    style: "width: 7vh",
    headerStyle: "width: 7vh",
    align: "center",
  },
  {
    name: "valorItem",
    align: "center",
    label: "Valor Item",
    field: "valorItem",
    format: (val) => `${parseInt(val).toLocaleString()}`,
    sortable: true,
    style: "width: 12vh",
    headerStyle: "width: 12vh",
    align: "center",
  },

  {
    name: "precioVenta",
    align: "center",
    label: "Precio de venta",
    field: "precioVenta",
    sortable: true,
    style: "width: 12vh",
    headerStyle: "width: 12vh",
    align: "center",
  },

  {
    name: "descripcion",
    label: "Descripcion",
    field: "descripcion",
    style: "width: 40vh",
    headerStyle: "width: 40vh",
    align: "left",
  },
];

export default {
  props: {
    items: Array,
  },
  setup(props) {
    // expose to template
    return {
      mycolumns,
      myrows: ref(props.items),
      separator: ref("vertical"),
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 5,
      }),
      modelUpdated(value) {
        console.log("XD", value);
      },
    };
  },
};
</script>
