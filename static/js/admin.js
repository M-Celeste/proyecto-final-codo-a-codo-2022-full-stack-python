"use strict";
const gestionRoot = document.getElementById("gestion-app");
if (gestionRoot) {
  const resource = gestionRoot.dataset.resource;
  Vue.createApp({
    delimiters: ["${", "}"],
    data: () => ({ items: [], loading: true, busy: false, error: "", mensaje: "", busqueda: "", categoria: { nombre: "", descripcion: "" } }),
    computed: { filtrados() { return this.items.filter(p => p.nombre.toLocaleLowerCase("es").includes(this.busqueda.toLocaleLowerCase("es"))); } },
    mounted() { this.cargar(); },
    methods: {
      money: Raiz.money,
      async cargar() {
        this.loading = true;
        try { this.items = await Raiz.request(`/${resource}`); }
        catch (error) { this.error = error.message; }
        finally { this.loading = false; }
      },
      async eliminar(item) {
        if (!confirm(`¿Eliminar «${item.nombre}»? Esta acción no se puede deshacer.`)) return;
        this.busy = true; this.error = ""; this.mensaje = "";
        try {
          await Raiz.request(`/${resource}/${item.id}`, { method: "DELETE" });
          this.mensaje = "Registro eliminado.";
          if (this.categoria.id === item.id) this.cancelarCategoria();
          await this.cargar();
        } catch (error) { this.error = error.message; }
        finally { this.busy = false; }
      },
      cancelarCategoria() { this.categoria = { nombre: "", descripcion: "" }; },
      async guardarCategoria() {
        this.busy = true; this.error = ""; this.mensaje = "";
        try {
          const id = this.categoria.id;
          await Raiz.request(`/categorias${id ? '/' + id : ''}`, { method: id ? "PUT" : "POST", body: JSON.stringify(this.categoria) });
          this.cancelarCategoria(); this.mensaje = "Categoría guardada."; await this.cargar();
        } catch (error) { this.error = error.message; }
        finally { this.busy = false; }
      },
    },
  }).mount(gestionRoot);
}
const plantaFormRoot = document.getElementById("planta-form-app");
if (plantaFormRoot) {
  Vue.createApp({
    delimiters: ["${", "}"],
    data: () => ({ categorias: [], loading: true, ready: false, busy: false, error: "", planta: { categoria_id: "", nombre: "", nombre_cientifico: "", descripcion: "", precio: "", stock: 0, imagen: "/static/img/planta.svg", luz: "", riego: "", destacada: false } }),
    async mounted() {
      try {
        this.categorias = await Raiz.request("/categorias");
        if (plantaFormRoot.dataset.id) {
          this.planta = await Raiz.request(`/plantas/${plantaFormRoot.dataset.id}`);
          this.planta.destacada = Boolean(this.planta.destacada);
        }
        this.ready = true;
      } catch (error) { this.error = error.message; }
      finally { this.loading = false; }
    },
    methods: {
      async guardar() {
        this.busy = true; this.error = "";
        try {
          const id = plantaFormRoot.dataset.id;
          await Raiz.request(`/plantas${id ? '/' + id : ''}`, { method: id ? "PUT" : "POST", body: JSON.stringify(this.planta) });
          window.location.assign("/admin/plantas");
        } catch (error) { this.error = error.message; }
        finally { this.busy = false; }
      },
    },
  }).mount(plantaFormRoot);
}
