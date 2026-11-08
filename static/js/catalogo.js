"use strict";
const catalogoRoot = document.getElementById("catalogo-app");
if (catalogoRoot) {
  Vue.createApp({
    delimiters: ["${", "}"],
    data: () => ({ plantas: [], categorias: [], q: "", categoria: "", disponibles: false, loading: true, error: "" }),
    async mounted() {
      try { this.categorias = await Raiz.request("/categorias"); }
      catch (error) { this.error = error.message; this.loading = false; return; }
      const params = new URLSearchParams(window.location.search);
      const category = this.categorias.find(c => c.nombre === params.get("categoria"));
      this.categoria = category ? category.id : (params.get("categoria_id") || "");
      await this.cargar();
    },
    methods: {
      money: Raiz.money,
      limpiar() { this.q = ""; this.categoria = ""; this.disponibles = false; this.cargar(); },
      async cargar() {
        this.loading = true; this.error = "";
        const params = new URLSearchParams({ q: this.q, categoria_id: this.categoria });
        if (this.disponibles) params.set("disponibles", "1");
        if (catalogoRoot.dataset.featured) params.set("destacadas", "1");
        try { this.plantas = await Raiz.request(`/plantas?${params}`); }
        catch (error) { this.error = error.message; this.plantas = []; }
        finally { this.loading = false; }
      },
    },
  }).mount(catalogoRoot);
}
const detalleRoot = document.getElementById("detalle-app");
if (detalleRoot) {
  Vue.createApp({
    delimiters: ["${", "}"],
    data: () => ({ planta: null, loading: true, error: "" }),
    async mounted() {
      try { this.planta = await Raiz.request(`/plantas/${detalleRoot.dataset.id}`); document.title = `${this.planta.nombre} · Raíz Celeste`; }
      catch (error) { this.error = error.message; }
      finally { this.loading = false; }
    },
    methods: { money: Raiz.money },
  }).mount(detalleRoot);
}
