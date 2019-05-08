const downloadButton = document.getElementById("download")
const downloadStatus = document.getElementById("download-status");
let cantDownloaded = 0

downloadButton.addEventListener("click", () => download())

var getDownloadStatus = (end = false) => {

    if (!end) {
        fetch(conf.urlBackend + 'download-status?sessionId=' + conf.sessionId)
            .then((response) => response.json())
            .then((status) => {
                if(!status.count){
                    downloadStatus.innerHTML = ""
                }else{
                    downloadStatus.innerHTML = `Completado: ${parseInt(status.correctInsert) + parseInt(status.errorInsert)} de ${status.count} 
                    Con error de inserción ${status.errorInsert}`
                } 

            }

            )
    }
    else {
        fetch(conf.urlBackend + 'download-status?sessionId=' + conf.sessionId)
            .then((response) => response.json())
            .then((status) => {
                downloadStatus.innerHTML = `Completado: ${parseInt(status.correctInsert) + parseInt(status.errorInsert || 0)} de ${status.count} 
                Con error de inserción ${status.errorInsert} 
                Tiempo total de descarga: ${status.timeDownload} Seg.
                Tiempo total de categorización: ${status.timeCategorize} Seg. 
                `
            }

            )
    }

}

const download = async () => {

    downloadStatus.innerHTML = "";

    kindOfStorage = document.querySelector('#kindOfStorage input[name="kindOfStorage"]:checked').value;

    const storageName = document.querySelectorAll(`.storage #storage-name`)[0].value
    const storageData = JSON.parse(document.querySelectorAll(`.storage #data`)[0].value)

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
        sessionId: conf.sessionId,
        kindOfStorage: kindOfStorage,
        storageName: storageName,
        storageData: images
    }

    var downloadStatusInterval = setInterval(() => {
        getDownloadStatus()
    }, 1000);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", conf.urlBackend + 'download', true);
    xhr.setRequestHeader("Content-Type", "text/plain");

    xhr.onreadystatechange = function () {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            setTimeout(() => {
                clearInterval(downloadStatusInterval);
                getDownloadStatus(true);
            }, 2000)

        }
    }

    xhr.send(JSON.stringify(storeData));

}

