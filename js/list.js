const submit = document.getElementById("submit")
const statusInfo = document.getElementById("status");
const mainContainer = document.getElementById("main-container")

const container = document.createElement("div");
container.classList.add("div-block-2");

title = document.createElement("div");
title.classList.add("title");

article = document.createElement("div");
article.classList.add("mlid");

row = document.createElement("div");
row.classList.add("w-row");

text = document.createElement("div");
text.classList.add("text-block-2")

col1 = document.createElement("div");
col1.classList.add("w-col");
col1.classList.add("w-col-6");

col2 = document.createElement("div");
col2.classList.add("w-col");
col2.classList.add("w-col-6");


img =  document.createElement("img");
img.src = "";

{/* <div class="div-block-2">
        <div class="title">Joico Moisture Recovery Condicionador 300ml<br></div>
        <div class="mlid">ML ID: <strong class="bold-text">MLB1002251313</strong></div>
        <div class="w-row">
          <div class="w-col w-col-6"><img src="images/634434-MLB27004768567_032018-O.jpg" alt="" class="image-2">
            <div>Imagen del anuncio</div>
            <div class="text-block-2">https://mlb-s1-p.mlstatic.com/634434-MLB27004768567_032018-O.jpg</div>
          </div>
          <div class="w-col w-col-6"><img src="images/634434-MLB27004768567_032018-O.jpg" alt="" class="image-2">
            <div>Imagen catálogo marca</div>
            <div class="text-block-2">https://mlb-s1-p.mlstatic.com/634434-MLB27004768567_032018-O.jpg</div>
          </div>
        </div>
        <div class="div-block-3">
          <div>Match 8/10</div>
        </div>
      </div> */}

var getStatus = ()=>{

    fetch('status.json?' + Math.random() + '=' + Math.random())
        .then((response) => response.json())
        .then((status) => {
            statusInfo.innerHTML = `Completado: ${Math.floor((status.absoluteComputed / (status.running.of * status.comparing.of)) * 100)}%
                                    Recorriendo ${status.running.current} 
                                    de ${status.running.of} 
                                    comparando con ${status.comparing.current} 
                                    de ${status.comparing.of}`
            // if (Math.floor((status.absoluteComputed / (status.running.of * status.comparing.of)) * 100) === 100) {
            //     clearInterval();
            // }
        }


        )

}


submit.addEventListener("click", async function () {
    // const textarea = document.getElementById("Json")
    // const json = textarea.value;

    var statusInterval = setInterval(() => {
        getStatus()
    }, 1000);

    const json = await fetch('./js/livesearchShort.json')
        .then(function (response) {
            return response.json();
        })

    // console.log(json)
    let id = 0;
    let imagenes = [];
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
                }
            })
        }
    });

    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/process', true);

    //Send the proper header information along with the request
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.onreadystatechange = function () { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            clearInterval(statusInterval)

            container.appendChild(title)
            container.appendChild(article)
            
            var title1 = title;
            title1.innerHTML = "aaaaaaaaaaaaaacccccccccccccccccaaaaaaaaaaaaaaa"
            col1.appendChild(title1)
            col1.appendChild(image)
            row.appendChild(col1)

            var title2 = title;
            title2.innerHTML = "aaaaaaaaaaaaaacccccccccccccccccaaaaaaaaaaaaaaa"
            col2.appendChild(title2)
            col2.appendChild(image)
            row.appendChild(col2)
            
            container.appendChild(row)


            mainContainer.appendChild(container);
            
            console.log(this.response)
        }
    }
    
    data = {'imagenes': imagenes, 'min_match_count': 80, 'scale': 200, 'sensibility': 0.6, 'min_percent_match': 10};

    console.log(data)

    xhr.send(JSON.stringify(data));
    // xhr.send(imagenes);

    function encode_utf8(s) {
        return unescape(encodeURIComponent(s));
    } ('\u4e0a\u6d77')

    // console.log(imagenes)
})