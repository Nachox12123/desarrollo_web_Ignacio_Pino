// ---- VALIDACIONES ----
const validateName = (name) => name && name.trim().length >= 3 && name.trim().length <= 200;
const validateEmail = (email) => {
  if (!email) return false;
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,}$/;
  return re.test(email) && email.length <= 100;
};
const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return true;
  let re = /^\+569\d{8}$/;
  return re.test(phoneNumber);
};
const validateSelect = (value) => value && value !== "";
const validateContact = (contact) => contact && contact.length >= 4 && contact.length <= 50;
const validateCantidad = (cantidad) => cantidad && parseInt(cantidad) >= 1;
const validateEdad = (edad) => edad !== "" && parseInt(edad) >= 0;
const validateEntrega = (fecha) => {
  if (!fecha) return false;
  let now = new Date();
  let entrega = new Date(fecha);
  return entrega.getTime() - now.getTime() >= 3 * 60 * 60 * 1000;
};
const validateDescripcion = (desc) => !desc || desc.length <= 500;
const validateFiles = (files) => {
  if (!files || files.length < 1 || files.length > 5) return false;
  for (const file of files) {
    if (!file.type.startsWith("image/")) return false;
  }
  return true;
};

// ---- VALIDAR FORMULARIO ----
const validateForm = () => {
  let myForm = document.forms["myForm"];

  let invalidInputs = [];
  let isValid = true;
  const setInvalid = (name) => { invalidInputs.push(name); isValid = false; };

  if (!validateSelect(myForm["select-regiones"].value)) setInvalid("Región");
  if (!validateSelect(myForm["select-comunas"].value)) setInvalid("Comuna");
  if (!validateName(myForm["nombre"].value)) setInvalid("Nombre");
  if (!validateEmail(myForm["email"].value)) setInvalid("Email");
  if (!validatePhoneNumber(myForm["phone"].value)) setInvalid("Teléfono");
  if (!validateSelect(myForm["select-contacto"].value)) setInvalid("Forma de contacto");
  if (!validateContact(myForm["contact"].value)) setInvalid("ID o URL de contacto");
  if (!validateSelect(myForm["select-tipo"].value)) setInvalid("Tipo de mascota");
  if (!validateCantidad(myForm["cantidad"].value)) setInvalid("Cantidad");
  if (!validateEdad(myForm["edad"].value)) setInvalid("Edad");
  if (!validateSelect(myForm["select-medida"].value)) setInvalid("Unidad de medida edad");
  if (!validateEntrega(myForm["entrega"].value)) setInvalid("Fecha de entrega");
  if (!validateDescripcion(myForm["descripcion"].value)) setInvalid("Descripción");
  
  
  let fotos = document.querySelectorAll(".foto-input");
  let allFiles = [];
  fotos.forEach(f => { if (f.files.length > 0) allFiles.push(...f.files); });
  if (allFiles.length < 1 || allFiles.length > 5) setInvalid("Fotos");

  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    invalidInputs.forEach((input) => {
      let li = document.createElement("li");
      li.innerText = input;
      validationListElem.append(li);
    });
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";
    validationBox.hidden = false;
    return false;
  } else {
    validationMessageElem.innerText = "¡Formulario válido!";
    validationListElem.textContent = "";
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";
    validationBox.hidden = false;
    return true;
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const fotosContainer = document.getElementById("fotos-container");
  const addPhotoBtn = document.getElementById("add-photo-btn");

  addPhotoBtn.addEventListener("click", () => {
    const fotos = fotosContainer.querySelectorAll(".foto-input");
    if (fotos.length >= 5) {
      alert("Solo se permiten hasta 5 fotos.");
      return;
    }
    const newInput = document.createElement("input");
    newInput.type = "file";
    newInput.name = "files";
    newInput.accept = "image/*";
    newInput.classList.add("foto-input");
    fotosContainer.appendChild(newInput);
  });

  const submitBtn = document.getElementById("submit-btn");
  document.getElementById("myForm").addEventListener("submit", function(e) {
    // Validación del formulario
    if (!validateForm()) {
        e.preventDefault(); // evita enviar si hay errores
        return;
    }

    // Confirmación antes de enviar
    let seguro = confirm("¿Está seguro que desea agregar este aviso de adopción?");
    if (!seguro) {
        e.preventDefault(); // evita enviar si el usuario cancela
        return;
    }

    // Alerta antes de enviar
    alert("Hemos recibido la información de adopción, muchas gracias y suerte!");
    // El formulario se enviará automáticamente a Flask después de esta alerta
});

});
