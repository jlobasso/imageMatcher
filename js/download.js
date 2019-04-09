const download = document.getElementById("download")

download.addEventListener("click", async () => {
    // const json = await fetch('./js/livesearch.json')
    //     .then(function (response) {
    //             return response.json();
    //         })
    const textarea = document.getElementById("Json")
    const json = JSON.parse(textarea.value);
        
            
            var imagenes = [];
            json.forEach(a => {
                if ('images' in a && a.images.length > 0) {
                    a.images.forEach((img, i) => {
                        if ('url' in img) {
                            imagenes.push({
                                id: a.id,
                                image: img.url,
                            })
                        }
                    })
                }
            });
            
    console.log(imagenes)        
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/download', true);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(JSON.stringify(imagenes));

    function encode_utf8(s) {
        return unescape(encodeURIComponent(s));
    } ('\u4e0a\u6d77')
})