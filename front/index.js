function guardarValores() {
    var inputs = document.getElementsByClassName('drag_bar');
    var valores = {};
    
    for (var i = 0; i < inputs.length; i++) {
        var nombre = inputs[i].getAttribute('name');
        var valor = inputs[i].value;
        valores[nombre] = valor;
    }
    
    console.log(valores); // Aquí puedes hacer lo que desees con el objeto de valores
    
    // También puedes enviar los valores a través de una petición AJAX si lo deseas
    
    // Restaurar los valores a sus valores iniciales
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = 1;
    }
}