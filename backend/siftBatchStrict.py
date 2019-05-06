from function.start import * 

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher
   
def matchSiftStrict(minMatchCount, sensibility, minPercentMatch, storageA, storageB, categories):
    
    timeA = datetime.datetime.now()
    pathA = config['paths']['storage-full-path']+storageA+'/'
    pathB = config['paths']['storage-full-path']+storageB+'/'
    lengthA = db[storageA].find({ 'category': {'$in': categories}}).count()
    lengthB = db[storageB].find({ 'category': {'$in': categories}}).count()
    
    cursorA = db[storageA].aggregate([
    {
        '$group':
        {
            '_id': '$category',
            'images': { '$push': '$$ROOT' },
            'count': { '$sum': 1 }
        }
    },
    {
        '$match': {
            '_id': {
                '$in': categories
            }
        }
    }
    ])

    globalMatches = []
    kInageComputed = 0


    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    sift = cv2.xfeatures2d.SIFT_create()

    #recorremos cada categoria A
    for categoriesA in cursorA:
        #---EXCEPTION---
        if len(categoriesA['images']) == 0:
            return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes de la categoria "+categoriesA['_id']}

        #recorremos cada imagen de cada categoria A
        for idxA in range(len(categoriesA['images'])):
            # print(imgA['imageName'].encode("ascii", "ignore").decode("ascii"))
            bestMatches = []        
            imageA = cv2.imread(pathA+categoriesA['images'][idxA]['imageName'], 0)
            kp1, des1 = sift.detectAndCompute(imageA, None) 

            cursorB = db[storageB].aggregate([
                        {
                                '$group':
                                {
                                '_id': '$category',
                                'images': { '$push': '$$ROOT' },
                                'count': { '$sum': 1 }
                                }
                        },
                        {
                                '$match': {
                                '_id': categoriesA['_id'] 
                                }
                        }
                        ])

            #recorremos cada categoria B        
            for categoriesB in cursorB:

                #---EXCEPTION---
                if range(len(categoriesB['images'])) == 0:
                    return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status":"No hay imagenes de la categoria "+categoriesB['_id']}

                #recorremos cada imagen de cada categoria B
                for idxB in range(len(categoriesB['images'])):
                    # print(idxB)
                    kInageComputed = kInageComputed + 1

                    F = open(config['paths']['status-path']+"status.json","w+")
                    status = {
                                "absoluteComputed": str(kInageComputed),
                                "running":{
                                            "current":str(idxA), 
                                            "of":str(lengthA)
                                            },
                                "comparing":{
                                            "current":str(idxB), 
                                            "of":str(lengthB)
                                            }                     
                            }            
                    F.write(json.dumps(status))
                    F.close()

                    imageB = cv2.imread(pathB+categoriesB['images'][idxB]['imageName'], 0)
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
                                'article_id_a': categoriesA['images'][idxA]['articleId'],
                                'title_a': categoriesA['images'][idxA]['title'],
                                'image_path_a': config['paths']['storage-path']+storageA+'/'+categoriesA['images'][idxA]['imageName'], 
                                'category_a': categoriesA['_id'],
                                'image_name_a': categoriesA['images'][idxA]['imageName'], 
                                'article_id_b': categoriesB['images'][idxB]['articleId'],
                                'title_b': categoriesB['images'][idxB]['title'],
                                'image_path_b': config['paths']['storage-path']+storageB+'/'+categoriesB['images'][idxB]['imageName'],
                                'image_name_b': categoriesB['images'][idxB]['imageName'], 
                                'category_b': categoriesB['_id'],
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

    totalMatches = kInageComputed

    db.batchStats.insert({ 
        "method":"sift", 
        "totalMatches":totalMatches, 
        "milisecondsElapsed": milisecondsElapsed, 
        "oneMatch": milisecondsElapsed/totalMatches
        })      

    return {'matches': globalMatches, 'imagenesA': lengthA, 'imagenesB': lengthB, "milisecondsElapsed":milisecondsElapsed, "status":"OK"}
