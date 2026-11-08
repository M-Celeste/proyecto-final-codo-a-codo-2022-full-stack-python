"use strict";
const contactForm = document.getElementById("contacto-form");
contactForm.addEventListener("submit", event => {
  event.preventDefault();
  const name = contactForm.elements.nombre;
  const message = contactForm.elements.mensaje;
  name.setCustomValidity(name.value.trim().length < 2 ? "Ingresá tu nombre." : "");
  message.setCustomValidity(message.value.trim().length < 10 ? "Ingresá al menos diez caracteres." : "");
  contactForm.classList.add("was-validated");
  const result = document.getElementById("contacto-resultado");
  if (!contactForm.checkValidity()) {
    result.textContent = "Revisá los campos indicados.";
    contactForm.querySelector(":invalid").focus();
    return;
  }
  result.textContent = "Consulta validada correctamente. Demostración: no se envió ningún correo.";
});
