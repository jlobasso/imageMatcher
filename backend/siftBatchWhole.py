
from function.start import * 

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher
   
def matchSiftWhole(minMatchCount, sensibility, minPercentMatch, storageA, storageB, categories):
    timeA = datetime.datetime.now()
    
    imagesA = db[storageA].find({ 'category': {'$in': categories}})
    pathA = config['paths']['storage-full-path']+storageA+'/'

    imagesB = db[storageB].find({ 'category': {'$in': categories}})
    pathB = config['paths']['storage-full-path']+storageB+'/'
     
    lenA = imagesA.count()    
    lenB = imagesB.count()

    globalMatches = []
    kInageComputed = 0
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    sift = cv2.xfeatures2d.SIFT_create()



    if lenA == 0:
        return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes en "+pathA}
    if lenB == 0:
        return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes en "+pathB}    
 
    for imgA in imagesA:
        # print(imgA['imageName'].encode("ascii", "ignore").decode("ascii"))
        bestMatches = []        
        imageA = cv2.imread(pathA+imgA['imageName'], 0)
        kp1, des1 = sift.detectAndCompute(imageA, None)   

        # recorre las imagenes originales del repo local
        imagesB = db[storageB].find({ 'category': {'$in': categories}})
        for imgB in imagesB:
            # print(imgB['imageName'].encode("ascii", "ignore").decode("ascii"))
            kInageComputed = kInageComputed + 1
            
            F = open(config['paths']['status-path']+"status.json","w+")

            status = {
                        "absoluteComputed": str(kInageComputed),
                        "running":{
                                    "current":str(1), 
                                    "of":str(lenA)
                                    },
                        "comparing":{
                                    "current":str(1), 
                                    "of":str(lenB)
                                    }                     
                    }            
            F.write(json.dumps(status))
            F.close()

     




            imageB = cv2.imread(pathB+imgB['imageName'], 0)                              
            kp2, des2 = sift.detectAndCompute(imageB, None)

            try: 
                matches = flann.knnMatch(des1, des2, k=2)  
                matches = sorted(matches, key = lambda x:x[1].distance)         
            except:
                break
                print(imgA['imageName'].encode("ascii", "ignore").decode("ascii"))
                print(imgB['imageName'].encode("ascii", "ignore").decode("ascii"))                
                  
            good = []
            for m, n in matches:
                if m.distance < sensibility*n.distance:
                    good.append(m)            
                  
            # good = []
            # for m, n in matches:
            #     if n.distance >= float(params.get('sensibility'))*n.distance:
            #         good.append(n)   
                  
            if float(len(good)/minMatchCount*100) > float(minPercentMatch):
                bestMatches.append(
                    {
                        'article_id_a': imgA['articleId'],
                        'title_a': imgA['title'],
                        'image_path_a': config['paths']['storage-path']+storageA+'/'+imgA['imageName'], 
                        'image_name_a': imgA['imageName'], 
                        'article_id_b': imgB['articleId'],
                        'title_b': imgB['title'],
                        'image_path_b': config['paths']['storage-path']+storageB+'/'+imgB['imageName'],
                        'image_name_b': imgB['imageName'], 
                        'percentage': str(len(good)/minMatchCount*100),

                    })

            imagenRecorridas = +1

            def extract(json):
                try:
                    return float(json['percentage'])
                except KeyError:
                    return 0

            bestMatches.sort(key=extract, reverse=True)
            
        if len(bestMatches) > 0:
            globalMatches.append(bestMatches)

    timeB = datetime.datetime.now()
    delta = timeB - timeA 
    milisecondsElapsed = int(delta.total_seconds() * 1000)

    totalMatches = lenA * lenB

    db.batchStats.insert({ "method":"sift", "totalMatches":totalMatches, "milisecondsElapsed": milisecondsElapsed, "oneMatch": milisecondsElapsed/totalMatches})      

    return {'matches': globalMatches, 'imagenesA': lenA, 'imagenesB': lenB, "milisecondsElapsed":milisecondsElapsed, "status":"OK"}

