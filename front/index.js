// GET REQUEST 


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