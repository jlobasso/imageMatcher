const downloadButton = document.getElementById("download")

downloadButton.addEventListener("click", () => download())

const download = async () => {

    kindOfStorage = document.querySelector('#kindOfStorage input[name="kindOfStorage"]:checked').value;

    const storageName = document.querySelectorAll(`.storage #storage-name`)[0].value
    const storageData = JSON.parse(document.querySelectorAll(`.storage #data`)[0].value)

   console.log(`.storage #data`)

    var images = [];
    storageData.forEach(a => {

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

    const storeData = {
        kindOfStorage: kindOfStorage,
        storageName: storageName,
        storageData: images
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", conf.urlBackend + 'download', true);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.send(JSON.stringify(storeData));

}

