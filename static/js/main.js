const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const textarea = document.querySelectorAll('#formulario textarea');

const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    telefono: /^\d{7,14}$/, // 7 a 14 numeros.
    mail: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    asunto: /^.{1,50}$/, // 1 a 50 digitos.
    descripcion: /^.{1,500}$/, // 1 a 500 digitos.
}

const campos = {
    nombre: false,
    apellido: false,
    telefono: false,
    mail: false,
    asunto: false,
    descripcion: false
}

const validarFormulario = (e) => {
    switch(e.target.name){
        case "nombre":
            validarCampo(expresiones.nombre, e.target, 'nombre');
        break;
        case "apellido":
            validarCampo(expresiones.apellido, e.target, 'apellido');
        break;
        case "telefono":
            validarCampo(expresiones.telefono, e.target, 'telefono');
        break;
        case "mail":
            validarCampo(expresiones.mail, e.target, 'mail');
        break;
        case "asunto":
            validarCampo(expresiones.asunto, e.target, 'asunto');
        break;        
        case "descripcion":
            validarCampo(expresiones.descripcion, e.target, 'descripcion');
        break;        
    }
}

const validarCampo = (expresion, input, campo) => {
    if(expresion.test(input.value)){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-check');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-xmark');
        document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
        campos[campo] = true;
    } else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto')
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-xmark');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-check');
        document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
        campos[campo] = false;
    }
};

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

textarea.forEach((textarea) => {
    textarea.addEventListener('keyup', validarFormulario);
    textarea.addEventListener('blur', validarFormulario);
});





