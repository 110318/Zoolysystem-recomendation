// parte de su servidor zorrito 
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




// GET REQUEST 
// parte de Cam
const DOMAIN = "http://localhost:"
const PORT = 5001

//RESOURCES
const RESOURCE = "nombres"
const POST_ROUTE = "post_endpoint"

//ELEMENTS 
const listContainer = document.querySelector('.names-list')
console.log(listContainer)


const populateNameList = (nameList) => {
    nameList.forEach(elemento => {
        console.log(elemento)
        //CREATE THE HTML ELEMENT
        const listItem = document.createElement('li');
        listItem.innerText = elemento;
        //ADD TO CONTAINER 
        listContainer.appendChild(listItem)
    });
}



fetch(`${DOMAIN}${PORT}/${RESOURCE}`)
    .then(raw => raw.json())
    .then(response => console.log(response))
    .catch(e => console.log(e))

const getMain = async () => {
    try {
        const raw = await fetch(`${DOMAIN}${PORT}/${RESOURCE} `)
        const response = await raw.json();
        populateNameList(response.Nombres)
    } catch (error) {
        console.log(error, 'efe')
    }
}

const postEndpoint = async () => {
    try {
        const raw = await fetch(
            `${DOMAIN}${PORT}/${POST_ROUTE} `,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({'Nombres': 'Sarah'})
            }
        );

        const response = await raw.json();
        console.log(response)

    } catch (error) {
        console.log(error,'efe')
    }
}
getMain();
postEndpoint();

