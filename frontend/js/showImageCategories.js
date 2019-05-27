const mostrarCategorias = document.getElementById("mostrar-categorias")

mostrarCategorias.addEventListener("click", async () => {

    var previousResults = document.getElementsByClassName('div-block-2');
    while (previousResults[0]) {
        previousResults[0].parentNode.removeChild(previousResults[0]);
    }

    var resumenResultado = document.getElementById("resultado-category-storage-x");
    // resumenResultado.style.display = "none";

    let storageX = document.getElementById("storage-x").value
    let selected = document.querySelectorAll('#category-storage-x option:checked');
    let categoriesStorage = Array.from(selected).map(el => el.value);
    
    fetch(conf.urlBackend+'show-images-categories?storageX='+storageX+'&categoriesStorageX='+categoriesStorage)
    
    .then((response) => response.json())
    .then((result) => {

            console.log(result)

            resumenResultado.innerHTML = `${Object(result.imageName)} 
                                            categories:  ${result.categories}`

        }
    )

})
