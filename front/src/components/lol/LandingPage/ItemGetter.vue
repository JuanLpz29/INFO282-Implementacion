<template>
    <div id="v-model-select" class="demo">
    <select v-model="selected" @change="onChange()">
        <option disabled value="">seleccionar tabla</option>
        <option>productos</option>
        <option>compras</option>
    </select>
    <span>Selected: {{ selected }}</span>
    </div>
</template>

<script>
export default {
  data () {
    return {
      items: null,
      selected: ''
    }
  },
  methods: {
    onChange () {
      this.$emit('clicked', this.selected)
    }
  }
}
</script>
