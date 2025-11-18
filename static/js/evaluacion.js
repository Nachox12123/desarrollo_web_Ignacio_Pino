let avisoActual = null;

function evaluarAviso(avisoId) {
    avisoActual = avisoId;
    const modal = document.getElementById('modal-evaluacion');
    modal.style.display = 'block';
    document.getElementById('mensaje-evaluacion').innerHTML = '';
}

async function enviarEvaluacion(nota) {
    if (!avisoActual) {
        mostrarMensaje('Error: No se ha seleccionado un aviso', 'error');
        return;
    }
    
    try {
        const modal = document.querySelector('.modal-content');
        modal.classList.add('loading');
        
        const response = await fetch('/api/evaluaciones', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                aviso_id: avisoActual,
                nota: nota
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const celdaNota = document.getElementById(`nota-${avisoActual}`);
            if (celdaNota) {
                celdaNota.textContent = data.nuevo_promedio;
                celdaNota.style.backgroundColor = '#2ecc71';
                celdaNota.style.color = 'white';
                celdaNota.style.transition = 'all 0.5s ease';
                
                setTimeout(() => {
                    celdaNota.style.backgroundColor = '';
                    celdaNota.style.color = '';
                }, 1000);
            }
            
            mostrarMensaje(data.mensaje, 'exito');
            
            setTimeout(() => {
                cerrarModal();
            }, 1500);
            
        } else {
            mostrarMensaje(data.error || 'Error al enviar evaluación', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje('Error de conexión. Inténtalo de nuevo.', 'error');
    } finally {
        const modal = document.querySelector('.modal-content');
        modal.classList.remove('loading');
    }
}

function mostrarMensaje(mensaje, tipo) {
    const divMensaje = document.getElementById('mensaje-evaluacion');
    divMensaje.textContent = mensaje;
    divMensaje.className = `mensaje ${tipo}`;
}

function cerrarModal() {
    const modal = document.getElementById('modal-evaluacion');
    modal.style.display = 'none';
    avisoActual = null;
    document.getElementById('mensaje-evaluacion').innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.onclick = cerrarModal;
    }
    
    const modal = document.getElementById('modal-evaluacion');
    if (modal) {
        modal.onclick = function(event) {
            if (event.target === modal) {
                cerrarModal();
            }
        };
    }
    
    // Event delegation for evaluate buttons using data attributes
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('evaluar-btn')) {
            const avisoId = event.target.getAttribute('data-aviso-id');
            if (avisoId) {
                evaluarAviso(parseInt(avisoId));
            }
        }
    });
    
    const ratingButtons = document.querySelectorAll('.rating-btn');
    ratingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nota = parseInt(this.getAttribute('data-nota'));
            enviarEvaluacion(nota);
        });
    });
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            cerrarModal();
        }
    });
});

function validarNota(nota) {
    const numeroNota = parseInt(nota);
    return !isNaN(numeroNota) && numeroNota >= 1 && numeroNota <= 7;
}