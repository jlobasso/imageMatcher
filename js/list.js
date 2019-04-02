const submit = document.getElementById("submit")

submit.addEventListener("click", async function () {
    // const textarea = document.getElementById("Json")
    // const json = textarea.value;

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
            console.log(this.response)
        }
    }

    xhr.send(JSON.stringify(imagenes));
    // xhr.send(imagenes);


    function encode_utf8( s ){
        return unescape( encodeURIComponent( s ) );
    }( '\u4e0a\u6d77' )

    // console.log(imagenes)
})