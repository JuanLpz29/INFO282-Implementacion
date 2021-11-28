<template>
  <div class="q-pa-md">
    <q-table
      title="Compras"
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
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <template v-if="col.name !== 'detalles'">
              {{ col.value }}
            </template>
            <template v-else>
              <q-btn
                unelevated
                icon="zoom_in"
                @click="showDetails(props.row)"
              ></q-btn>
            </template>
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="fixed" full-width>
      <q-card>
        <q-card-section>
          <div class="text-h6">Detalles de la compra</div>
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 70vh" class="scroll">
          <suspense>
            <template #default>
              <detalles-compra :idCompra="idCompra" />
            </template>
            <template #fallback>
              <div>Loading...</div>
            </template>
          </suspense>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn
            flat
            label="Cerrar"
            color="dark"
            v-close-popup
            :v-model="(details = !details)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { ref } from "vue";
import { useQuasar } from "quasar";
import rqts from "../myUtils/myUtils";
import DetallesCompra from "../components/DetallesCompra.vue";

const columns = [
  {
    name: "idCompra",
    required: true,
    label: "Id de la Compra",
    align: "center",
    field: "idCompra",
    sortable: true,
    headerStyle: "width: 10vh",
  },
  {
    name: "idProveedor",
    align: "center",
    label: "Id del proveedor",
    field: "idProveedor",
    sortable: true,
  },
  {
    name: "tipoDocumento",
    align: "center",
    label: "Tipo del Documento",
    field: "tipoDocumento",
    sortable: true,
  },
  {
    name: "montoTotal",
    align: "center",
    label: "Monto Total de la compra",
    field: "montoTotal",
    sortable: true,
  },
  {
    name: "fecha",
    align: "center",
    label: "Fecha de la compra",
    field: "fecha",
    sortable: true,
  },
  {
    name: "montoNeto",
    align: "center",
    label: "monto Neto de la compra",
    field: "montoNeto",
    sortable: true,
  },
  {
    name: "detalles",
    align: "center",
    label: "Ver detalles",
    // field: "",
  },
];

export default {
  components: { DetallesCompra },
  async setup() {
    const $q = useQuasar();
    $q.loading.show({
      message: "Cargandoo...",
    });
    const items = await rqts.get("compras/").catch((e) => {
      console.log(e);
    });
    $q.loading.hide();
    if (typeof items == "undefined") {
      console.log("XDDDDDDD");
    }
    console.log(items);

    function showDetails(row) {
      this.fixed = true;
      this.idCompra = row.idCompra;
      this.details = true;
      console.log(this.idCompra);
    }

    return {
      columns,
      items,
      filter: ref(""),
      pagination: ref({
        rowsPerPage: 10,
      }),
      showDetails,
      fixed: ref(false),
      msg: ref(""),
      details: ref(false),
      idCompra: ref(null),
    };
  },
};
</script>
