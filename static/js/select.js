// ====== Datos ======
const data = {
  "Tarapacá": ["Camiña", "Huara", "Pozo Almonte", "Iquique", "Pica", "Colchane", "Alto Hospicio"],
  "Antofagasta": ["Tocopilla", "Maria Elena", "Ollague", "Calama", "San Pedro Atacama", "Sierra Gorda", "Mejillones", "Antofagasta", "Taltal"],
  "Atacama": ["Diego de Almagro", "Chañaral", "Caldera", "Copiapo", "Tierra Amarilla", "Huasco", "Freirina", "Vallenar", "Alto del Carmen"],
  "Coquimbo": ["La Higuera", "La Serena", "Vicuña", "Paihuano", "Coquimbo", "Andacollo", "Rio Hurtado", "Ovalle", "Monte Patria", "Punitaqui", "Combarbala", "Mincha", "Illapel", "Salamanca", "Los Vilos"],
  "Valparaíso": ["Petorca", "Cabildo", "Papudo", "La Ligua", "Zapallar", "Putaendo", "Santa Maria", "San Felipe", "Pencahue", "Catemu", "Llay Llay", "Nogales", "La Calera", "Hijuelas", "La Cruz", "Quillota", "Olmue", "Limache", "Los Andes", "Rinconada", "Calle Larga", "San Esteban", "Puchuncavi", "Quintero", "Viña del Mar", "Villa Alemana", "Quilpue", "Valparaiso", "Juan Fernandez", "Casablanca", "Concon", "Isla de Pascua", "Algarrobo", "El Quisco", "El Tabo", "Cartagena", "San Antonio", "Santo Domingo"],
  "Libertador Bernardo Ohiggins": ["Mostazal", "Codegua", "Graneros", "Machali", "Rancagua", "Olivar", "Doñihue", "Requinoa", "Coinco", "Coltauco", "Quinta Tilcoco", "Las Cabras", "Rengo", "Peumo", "Pichidegua", "Malloa", "San Vicente", "Navidad", "La Estrella", "Marchigue", "Pichilemu", "Litueche", "Paredones", "San Fernando", "Peralillo", "Placilla", "Chimbarongo", "Palmilla", "Nancagua", "Santa Cruz", "Pumanque", "Chepica", "Lolol"],
  "Maule": ["Teno", "Romeral", "Rauco", "Curico", "Sagrada Familia", "Hualañe", "Vichuquen", "Molina", "Licanten", "Rio Claro", "Curepto", "Pelarco", "Talca", "Pencahue", "San Clemente", "Constitucion", "Maule", "Empedrado", "San Rafael", "San Javier", "Colbun", "Villa Alegre", "Yerbas Buenas", "Linares", "Longavi", "Retiro", "Parral", "Chanco", "Pelluhue", "Cauquenes"],
  "Biobío": ["Tome", "Florida", "Penco", "Talcahuano", "Concepcion", "Hualqui", "Coronel", "Lota", "Santa Juana", "Chiguayante", "San Pedro de la Paz", "Hualpen", "Cabrero", "Yumbel", "Tucapel", "Antuco", "San Rosendo", "Laja", "Quilleco", "Los Angeles", "Nacimiento", "Negrete", "Santa Barbara", "Quilaco", "Mulchen", "Alto Bio Bio", "Arauco", "Curanilahue", "Los Alamos", "Lebu", "Cañete", "Contulmo", "Tirua"],
  "La Araucanía": ["Renaico", "Angol", "Collipulli", "Los Sauces", "Puren", "Ercilla", "Lumaco", "Victoria", "Traiguen", "Curacautin", "Lonquimay", "Perquenco", "Galvarino", "Lautaro", "Vilcun", "Temuco", "Carahue", "Melipeuco", "Nueva Imperial", "Puerto Saavedra", "Cunco", "Freire", "Pitrufquen", "Teodoro Schmidt", "Gorbea", "Pucon", "Villarrica", "Tolten", "Curarrehue", "Loncoche", "Padre Las Casas", "Cholchol"],
  "Los Lagos": ["San Pablo", "San Juan", "Osorno", "Puyehue", "Rio Negro", "Purranque", "Puerto Octay", "Frutillar", "Fresia", "Llanquihue", "Puerto Varas", "Los Muermos", "Puerto Montt", "Maullin", "Calbuco", "Cochamo", "Ancud", "Quemchi", "Dalcahue", "Curaco de Velez", "Castro", "Chonchi", "Queilen", "Quellon", "Quinchao", "Puqueldon", "Chaiten", "Futaleufu", "Palena", "Hualaihue"],
  "Aisén del General Carlos Ibáñez del Campo": ["Guaitecas", "Cisnes", "Aysen", "Coyhaique", "Lago Verde", "Rio Ibañez", "Chile Chico", "Cochrane", "Tortel", "O'Higins"],
  "Magallanes y la Antártica Chilena": ["Torres del Paine", "Puerto Natales", "Laguna Blanca", "San Gregorio", "Rio Verde", "Punta Arenas", "Porvenir", "Primavera", "Timaukel", "Antartica"],
  "Metropolitana de Santiago": ["Tiltil", "Colina", "Lampa", "Conchali", "Quilicura", "Renca", "Las Condes", "Pudahuel", "Quinta Normal", "Providencia", "Santiago", "La Reina", "Ñuñoa", "San Miguel", "Maipu", "La Cisterna", "La Florida", "La Granja", "Independencia", "Huechuraba", "Recoleta", "Vitacura", "Lo Barrenechea", "Macul", "Peñalolen", "San Joaquin", "La Pintana", "San Ramon", "El Bosque", "Pedro Aguirre Cerda", "Lo Espejo", "Estacion Central", "Cerrillos", "Lo Prado", "Cerro Navia", "San Jose de Maipo", "Puente Alto", "Pirque", "San Bernardo", "Calera de Tango", "Buin", "Paine", "Peñaflor", "Talagante", "El Monte", "Isla de Maipo", "Curacavi", "Maria Pinto", "Melipilla", "San Pedro", "Alhue", "Padre Hurtado"],
  "Los Ríos": ["Lanco", "Mariquina", "Panguipulli", "Mafil", "Valdivia", "Los Lagos", "Corral", "Paillaco", "Futrono", "Lago Ranco", "La Union", "Rio Bueno"],
  "Arica y Parinacota": ["Gral. Lagos", "Putre", "Arica", "Camarones"],
  "Ñuble": ["Cobquecura", "Ñiquen", "San Fabian", "San Carlos", "Quirihue", "Ninhue", "Trehuaco", "San Nicolas", "Coihueco", "Chillan", "Portezuelo", "Pinto", "Coelemu", "Bulnes", "San Ignacio", "Ranquil", "Quillon", "El Carmen", "Pemuco", "Yungay", "Chillan Viejo"]
};

const data2 = ["Whatsapp", "Telegram", "X", "Instagram", "Tiktok", "Otra"];
const data3 = ["Perro", "Gato"];
const data4 = ["Años", "Meses"];

const poblarRegiones = () => {
  const regionSelect = document.getElementById("select-regiones");
  regionSelect.innerHTML = '<option value="">Seleccione una Región</option>';
  for (const region in data) {
    const option = document.createElement("option");
    option.value = region;
    option.textContent = region;
    regionSelect.appendChild(option);
  }
};

const updateComuna = () => {
  const regionSelect = document.getElementById("select-regiones");
  const comunaSelect = document.getElementById("select-comunas");
  const selectedRegion = regionSelect.value;

  comunaSelect.innerHTML = '<option value="">Seleccione una Comuna</option>';

  if (data[selectedRegion]) {
    data[selectedRegion].forEach((comuna, index) => {
      const option = document.createElement("option");
      option.value = index;  
      option.textContent = comuna;
      comunaSelect.appendChild(option);
    });
  }

  changeArguments();
};


function changeArguments() {
  const comunaSelect = document.getElementById("select-comunas");
  const reasonLabel = document.querySelector("label[for='reason']");
  const reasonTextarea = document.getElementById("comments");

  if (!reasonLabel || !reasonTextarea || !comunaSelect) return;

  if (comunaSelect.value !== "") {
    reasonLabel.style.display = "block";
    reasonTextarea.style.display = "block";
  } else {
    reasonLabel.style.display = "none";
    reasonTextarea.style.display = "none";
  }
}

const poblarContacto = () => {
  const contactoSelect = document.getElementById("select-contacto");
  contactoSelect.innerHTML = '<option value="">Seleccione un medio</option>';
  data2.forEach((contacto) => {
    const option = document.createElement("option");
    option.value = contacto;
    option.textContent = contacto;
    contactoSelect.appendChild(option);
  });
};

function changeContacto() {
  const contactoSelect = document.getElementById("select-contacto");
  const contactLabel = document.querySelector("label[for='contact']");
  const contactInput = document.getElementById("contact");

  if (!contactLabel || !contactInput || !contactoSelect) return;

  if (contactoSelect.value !== "") {
    contactLabel.style.display = "block";
    contactInput.style.display = "block";
  } else {
    contactLabel.style.display = "none";
    contactInput.style.display = "none";
  }
}

const poblarTipo = () => {
  const tipoSelect = document.getElementById("select-tipo");
  tipoSelect.innerHTML = '<option value="">Seleccione un Tipo</option>';
  data3.forEach((tipo) => {
    const option = document.createElement("option");
    option.value = tipo;
    option.textContent = tipo;
    tipoSelect.appendChild(option);
  });
};

const poblarMedida = () => {
  const medidaSelect = document.getElementById("select-medida");
  medidaSelect.innerHTML = '<option value="">Seleccione unidad</option>';
  data4.forEach((medida) => {
    const option = document.createElement("option");
    option.value = medida;
    option.textContent = medida;
    medidaSelect.appendChild(option);
  });
};

window.addEventListener("load", () => {
  poblarRegiones();
  poblarContacto();
  poblarTipo();
  poblarMedida();

  changeArguments();
  changeContacto();

  document.getElementById("select-regiones").addEventListener("change", updateComuna);
  document.getElementById("select-comunas").addEventListener("change", changeArguments);
  document.getElementById("select-contacto").addEventListener("change", changeContacto);
});
