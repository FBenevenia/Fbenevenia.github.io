$(document).ready(main);

var contador = 1;
function main(){
    $('.menu_bar').click(function(){
        if(contador==1){
            $('nav').animate({left:'0'});
            contador=0;    
        } else {
            contador=1;
            $('nav').animate({left:'-100%'});
            }
    });

//para mostrar y ocultar submenu
    $('.submenu').click(function(){
        $(this).children('.children').slideToggle();
});
};

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

formulario.addEventListener('submit', (e) => {
    e.preventDefault();
    if(campos.nombre && campos.apellido && campos.mail && campos.telefono && campos.asunto && campos.descripcion){
        document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo') //ver si está bien//
        formulario.reset();
        document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo')
       
       setTimeout(() =>{
           document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo')
       }, 10000);
        document.querySelectorAll('.formulario__grupo-correcto').forEach((icono) => {
            icono.classList.remove('formulario__grupo-correcto')
        });
    } else {
        document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo')

    }
});//si llego, ver cómo hacer para que cuando registre 1 valor bien completado se vaya el mensaje de error y revisar q nunca envíe un formulario vacío//
