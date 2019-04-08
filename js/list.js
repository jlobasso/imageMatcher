const submit = document.getElementById("submit")
const statusInfo = document.getElementById("status");
const mainContainer = document.getElementById("main-container")
const statusContainer = document.getElementById("status-container")
var cantImagesToCompare = 0;

var getStatus = () => {

    fetch('status.json?' + Math.random() + '=' + Math.random())
        .then((response) => response.json())
        .then((status) => {
            statusInfo.innerHTML = `Completado: ${Math.floor((status.absoluteComputed / (status.running.of * status.comparing.of)) * 100)}%
                                    Recorriendo ${status.running.current} 
                                    de ${status.running.of} 
                                    comparando con ${status.comparing.current} 
                                    de ${status.comparing.of}`
        }


        )

}

var time = {start: null, finish: null, total: null}

var dataArticle = {}

submit.addEventListener("click", async () => {

    time.start = new Date();

    const textarea = document.getElementById("Json")
    const json = JSON.parse(textarea.value);
    // const json = await fetch('./js/livesearchShort.json')
    //     .then(function (response) {
    //         return response.json();
    //     })

    var previousResults = document.getElementsByClassName('div-block-2');
    while (previousResults[0]) {
        previousResults[0].parentNode.removeChild(previousResults[0]);
    }

    var resumenResultado = document.getElementById("resumen-resultado");
    resumenResultado.style.display = "none";

    const statusContainer = document.getElementById("status-container")
    statusContainer.style.display = "block"

    var statusInterval = setInterval(() => {
        getStatus()
    }, 1000);
    

    let id = 0;
    var imagenes = [];
    json.forEach(a => {
        if ('images' in a && a.images.length > 0) {
            a.images.forEach((img, i) => {
                if ('url' in img) {
                    imagenes.push({
                        id: a.id,
                        // title: a.title, 
                        image: img.url,
                        position: i,
                    })
                dataArticle[a.id] = a.title
                }
            })
        }
    });

    // /** OJO QUE ESTOY RECORTANDO EL ARRAY!!!! */
    // imagenes = imagenes.slice(0, 6);

    cantImagesToCompare = imagenes.length;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/process', true);

    //Send the proper header information along with the request
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.onreadystatechange = function () { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            clearInterval(statusInterval)
                    
            time.finish = new Date();
            time.total = ((time.finish - time.start)/1000/60).toFixed(2) + " min";
            
            // console.log(time)


            drawResults(this.response)
        }
    }

    let minMatchCount = +document.getElementById("min-match-count").value;
    let scale = +document.getElementById("scale").value;
    let sensibility = +document.getElementById("sensibility").value / 100;
    var minPercentMatch = +document.getElementById("min-percent-match").value;
    let compareCategory = document.getElementById("compare-category").value

    data = {
        'imagenes': imagenes,
        'min_match_count': minMatchCount,
        'scale': scale,
        'sensibility': sensibility,
        'min_percent_match': minPercentMatch,
        "compare_category": compareCategory
    };

    xhr.send(JSON.stringify(data));

    function encode_utf8(s) {
        return unescape(encodeURIComponent(s));
    } ('\u4e0a\u6d77')
})


drawResults = (data) => {

    // console.log(data);

    data = JSON.parse(data);

    let totalQuantity = 0;

    let images = [];

    data.matches.forEach(e => {
        e.forEach(img => {
            images.push(img)
        })
    })

    images = images.sort((a, b) => {

        if (parseFloat(a.percentage) < parseFloat(b.percentage)) {
            return 1;
        }
        if (parseFloat(a.percentage) > parseFloat(b.percentage)) {
            return -1;
        }

        return 0;
    })

    images.forEach(imgMatch => {

        totalQuantity++;       

        var container = document.createElement("div");
        container.classList.add("div-block-2");

        var title = document.createElement("div");
        title.classList.add("title");

        var article = document.createElement("div");
        article.classList.add("mlid");

        var row = document.createElement("div");
        row.classList.add("w-row");

        var text = document.createElement("div");
        text.classList.add("text-block-2")

        var img1 = document.createElement("img");

        var img2 = document.createElement("img");


        title.innerHTML = dataArticle[imgMatch.article_id]
        article.innerHTML = "ML ID: "+imgMatch.article_id;


        container.appendChild(title)
        container.appendChild(article)

        var col1 = document.createElement("div");
        col1.classList.add("w-col");
        col1.classList.add("w-col-6");

        var col2 = document.createElement("div");
        col2.classList.add("w-col");
        col2.classList.add("w-col-6");

        var title1 = document.createElement("div");
        var title2 = document.createElement("div");

        let imageNameURL = imgMatch.image_url.split('/')
        title1.innerHTML = "Imagen del anuncio: <br>"+imageNameURL[imageNameURL.length -1];

        img1.src = imgMatch.image_url
        col1.appendChild(img1)
        col1.appendChild(title1)
        row.appendChild(col1)

        let imageNameRepo = imgMatch.image_repo.split('/')
        title2.innerHTML = "Imagen catálogo marca: <br>"+imageNameRepo[imageNameRepo.length -1];

        img2.src = imgMatch.image_repo
        col2.appendChild(img2)
        col2.appendChild(title2)
        row.appendChild(col2)


        var percentage = document.createElement("div");
        percentage.innerHTML = parseFloat(imgMatch.percentage).toFixed(2) + "%";
        percentage.classList.add("percentage");


        row.appendChild(percentage); 

        container.appendChild(row)


        mainContainer.appendChild(container);
    })


    var resumenResultado = document.getElementById("resumen-resultado");

    var minPercentMatch = +document.getElementById("min-percent-match").value;

    const statusInfo = document.getElementById("status");

    resumenResultado.innerHTML = `
    Resultados con macheos mayores al ${minPercentMatch}%: ${totalQuantity} <br>
    Cantidad de imagenes analizadas: ${cantImagesToCompare}<br>
    Tiempo de Proceso: ${time.total}`;
    
    // Cantidad de publicaciones analizadas: ${cantImagesToCompare}<br>
    // Repositorio donde Macheo la imagen: ${imgMatch.image_repo} <br>

    resumenResultado.style.display = "block";




}