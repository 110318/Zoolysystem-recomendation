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
const PORT = 5001

//RESOURCES
const RESOURCE = "nombres"
const POST_ROUTE = "post_endpoint"
const RECOMMEND_ROUTE = "recommend"

//ELEMENTS 
const listContainer = document.querySelector('.names-list');
const recommendationDiv = document.querySelector('#recommendation')
const slidersContainer = document.querySelector('.sliders');
const aggregationSelect = document.querySelector('#aggregation-select')

const weights = {
    "Cola esponjosa": 0,
    "Ojos redondos": 0,
    "Pelaje corto": 0,
    "Plumas": 0,
    "Osico alargado": 0,
    "Orejas puntiagudas": 0,
    "Pezunas": 0,
    "Pico": 0,
    "Manchas": 0,
    "Garras": 0,
    "Alas": 0,
    "Aletas": 0
}

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

//UPDATE WEIGHTS 
const updateWeights = () => {
    for (const feature in weights) {
        weights[feature] = document.getElementById(feature).value
    }
}







fetch(`${DOMAIN}${PORT}/${RESOURCE}`)
    .then(raw => raw.json())
    .then(response => console.log(response))
    .catch(e => console.log(e))





//Get recommendation from KNN
    const getRecommendation = async () => {
        try {
            updateWeights()
    
            const kNeighbors = document.getElementById('k_neighbors').value
            const aggregationMethod = document.getElementById('aggregation_method').value
    
            const response = await fetch(`${DOMAIN}${PORT}/${RECOMMEND_ROUTE}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    node: 0,
                    weights,
                    k_neighbors: kNeighbors,
                    aggregation_method: aggregationMethod
                })
            });
    
            const data = await response.json();
    
            recommendationDiv.innerText = `Recommended Animal: ${data.recommendation}`;
            populateNameList(data.neighbors);
        } catch (error) {
            console.log(error);
        }
    }


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
                body: JSON.stringify({
                'Nombres': 'Sarah',
            
            
            
            })
            }
        );

        const response = await raw.json();
        console.log(response)

    } catch (error) {
        console.log(error,'efe')
    }
}

// const recommendButton = document.getElementById('recommendButton')
// recommendButton.addEventListener('click', getRecommendation)




getMain();
postEndpoint();

