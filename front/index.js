// parte de su servidor zorrito 
function guardarValores() {

    // aqui guarda el metodo de agrupacion en un string
    var metodoAgrup = document.getElementById("metodo-agrup").value;
    // y aqui los valores de los slider
    var valores = {};

    var inputs = document.getElementsByClassName('drag_bar');
    
    
    for (var i = 0; i < inputs.length; i++) {
        var nombre = inputs[i].getAttribute('name');
        var valor = inputs[i].value;
        valores[nombre] = valor;
    }

    // Aquí puedes hacer lo que desees con el objeto de valores
    console.log(valores + metodoAgrup); 
 
    // Restaurar los valores a sus valores iniciales
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = 3;
    }
}




// GET REQUEST 
// parte de Cam
const DOMAIN = "http://localhost:"
const PORT = 5000

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

