const download = document.getElementById("download")

download.addEventListener("click", async () => {
    // const json = await fetch('./livesearch.json')
    //     .then(function (response) {
    //         return response.json();
    //     })
    const textarea = document.getElementById("Json")
    const json = JSON.parse(textarea.value);

    const input = document.getElementById("storage")

    var images = [];
    json.forEach(a => {

        if ('images' in a && a.images.length > 0) {

            var obj = {}
            obj.articleId = a.id
            obj.title = a.title
            obj.link = a.link
            obj.sellerId = a.sellerId
            obj.categoryId = a.categoryId
            obj.images = []

            a.images.forEach((img, i) => {
                if ('url' in img) {
                    obj.images.push({
                        imageId: img.id,
                        url: img.url,
                    })
                }
            })
            images.push(obj)

        }
    });

    var xhr = new XMLHttpRequest();
    xhr.open("POST", conf.urlBackend+'download', true);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(JSON.stringify(images));
})