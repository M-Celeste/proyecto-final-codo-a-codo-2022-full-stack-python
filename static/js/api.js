"use strict";
window.Raiz = {
  async request(path, options = {}) {
    const response = await fetch(`/api${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...options.headers },
    });
    if (response.status === 204) return null;
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "No se pudo completar la operación.");
    return data;
  },
  money(value) {
    return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" }).format(value);
  },
};
