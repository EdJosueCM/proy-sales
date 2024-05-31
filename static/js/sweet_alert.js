const DarkSwal = Swal.mixin({
    customClass: {
        popup: 'dark-popup',
        title: 'dark-title',
        text: 'dark-text',
        icon: 'dark-icon',
        confirmButton: 'btn-update',
        cancelButton: 'btn-cancel'
    },
    buttonsStyling: true // Desactiva los estilos por defecto de los botones
});

function mostrarError(mensaje) {
    DarkSwal.fire({
        icon: 'error',
        title: '<span class="error-title">¡Error!</span>',
        text: mensaje,
        confirmButtonText: 'Continuar'
    });
}

async function validarFormulario(event) {
    event.preventDefault(); // Detiene el envío del formulario
    const ruc = document.getElementById('id_ruc').value;
    const name = document.getElementById('id_name').value;
    const phone = document.getElementById('id_phone').value;
    try {
        if (!Validaciones.esCedulaValida(ruc)) {
            mostrarError('El formato del DNI es inválido. Por favor, inténtelo de nuevo.');
        } else if (!Validaciones.soloLetras(name)) {
            mostrarError('Formato de nombre incorrecto. Por favor, inténtelo de nuevo.');
        } else if (!Validaciones.soloNumeros(phone) || phone.length !== 10) {
            mostrarError('Celular incorrecto. Por favor, inténtelo de nuevo.');
        } else {
            DarkSwal.fire({
                title: '<span class="success-title">¡Éxito!</span>',
                text: 'Información válida. Enviando formulario...',
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                event.target.submit();
            });
        }
    } catch (error) {
        console.error('Error al validar el formulario:', error);
        mostrarError('Hubo un error al validar el formulario. Por favor, inténtelo de nuevo.');
    }
}