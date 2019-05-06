const submit = document.getElementById("submit")
const statusInfo = document.getElementById("status");
const mainContainer = document.getElementById("main-container")
const statusContainer = document.getElementById("status-container")
const sessionId = conf.sessionId
var cantImagesToCompare = 0;
var cantAnalizadas = 0;

var getStatus = () => {

    fetch('status/status.json?' + Math.random() + '=' + Math.random())
        .then((response) => response.json())
        .then((status) => {
            statusInfo.innerHTML = `Completado: ${Math.floor((status.absoluteComputed / (status.running.of * status.comparing.of)) * 100)}%
                                    Recorriendo ${status.running.current} 
                                    de ${status.running.of} 
                                    comparando con ${status.comparing.current} 
                                    de ${status.comparing.of}`
            cantAnalizadas = status.comparing.of * status.running.of
        }

        )

}

var time = { start: null, finish: null, total: null }

var dataArticle = {}

submit.addEventListener("click", async () => {

    time.start = new Date();
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
    
    let categoryStrict = document.getElementById("categoryStrict").value
    let process = document.getElementById("process").value
 
    kindOfBatchProcess = process+"-"+categoryStrict;


    var xhr = new XMLHttpRequest();
    xhr.open("POST", conf.urlBackend+kindOfBatchProcess, true);

    //Send the proper header information along with the request
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.onreadystatechange = function () { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            time.finish = new Date();
            time.total = ((time.finish - time.start) / 1000 / 60).toFixed(2) + " min";
            drawResults(this.response)
            setTimeout(() => { clearInterval(statusInterval) }, 2000)

        }
    }

    let minMatchCount = +document.getElementById("min-match-count").value;
    let sensibility = +document.getElementById("sensibility").value / 100;
    var minPercentMatch = +document.getElementById("min-percent-match").value;
    let storageA = document.getElementById("storageA").value
    let storageB = document.getElementById("storageB").value
    let selected = document.querySelectorAll('#category option:checked');
    let values = Array.from(selected).map(el => el.value);

    data = {
        "sessionId":sessionId,
        'min_match_count': minMatchCount,
        'sensibility': sensibility,
        'min_percent_match': minPercentMatch,
        "storageA": storageA,
        "storageB": storageB,
        "categories":values
    };

    xhr.send(JSON.stringify(data));

    function encode_utf8(s) {
        return unescape(encodeURIComponent(s));
    } ('\u4e0a\u6d77')
})


drawResults = (data) => {
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
        
        var match = document.createElement("div");
        match.classList.add("match");

        var article = document.createElement("div");
        article.classList.add("mlid");

        var row = document.createElement("div");
        row.classList.add("w-row");

        var text = document.createElement("div");
        text.classList.add("text-block-2")

        var img1 = document.createElement("img");

        var img2 = document.createElement("img");


        let minMatchCount = +document.getElementById("min-match-count").value;
        let sensibility = +document.getElementById("sensibility").value / 100;
        var minPercentMatch = +document.getElementById("min-percent-match").value
        let process = document.getElementById("process").value


        title.innerHTML = imgMatch.title_a;

        var urlMmatch = `match=${'match-'+process.split('-')[1]}`
        urlMmatch += `&url1=${imgMatch.image_path_a}`
        urlMmatch += `&url2=${imgMatch.image_path_b}`
        urlMmatch += `&min_match_count=${minMatchCount}`
        urlMmatch += `&sensibility=${sensibility}`
        urlMmatch += `&min_percent_match=${minPercentMatch}`

        var matchLink = document.createElement("a")
        matchLink.innerHTML = "CHECK"
        matchLink.href = "match.html?" + urlMmatch
        matchLink.target = "_blank"
        match.appendChild(matchLink)
        
        article.innerHTML = "ML ID: " + imgMatch.article_id_a;

        container.appendChild(title)
        container.appendChild(match)
        container.appendChild(article)

        var col1 = document.createElement("div");
        col1.classList.add("w-col");
        col1.classList.add("w-col-6");

        var col2 = document.createElement("div");
        col2.classList.add("w-col");
        col2.classList.add("w-col-6");

        var title1 = document.createElement("div");
        var title2 = document.createElement("div");
        var category1 = document.createElement("div");
        var category2 = document.createElement("div");

        title1.innerHTML = "Imagen del anuncio: <br>" + imgMatch.image_name_a;
        category1.innerHTML = "Categoria: " + imgMatch.category_a;
        
        img1.src = imgMatch.image_path_a
        col1.appendChild(img1)
        col1.appendChild(title1)
        col1.appendChild(category1)
        row.appendChild(col1)
        
        title2.innerHTML = "Imagen catálogo marca: <br>" + imgMatch.image_name_b;
        category2.innerHTML = "Categoria: " + imgMatch.category_b;

        img2.src = imgMatch.image_path_b
        col2.appendChild(img2)
        col2.appendChild(title2)
        col2.appendChild(category2)
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
    Cantidad Macheos analizadas: ${cantAnalizadas}<br>
    Tiempo de Proceso: ${time.total}`;

    resumenResultado.style.display = "block";




}