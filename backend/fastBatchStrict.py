from function.start import *

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher
   
def matchFastStrict(sessionId, minMatchCount, sensibility, minPercentMatch, storageA, storageB, categories):
    
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
    #ORB
    orb = cv2.ORB_create()

    #recorremos cada categoria A
    for categoriesA in cursorA:

        #---EXCEPTION---
        if len(categoriesA['images']) == 0:
            return {'matches': [], 'imagenes1': 0, 'imagenes2': 0, "status": "No hay imagenes de la categoria "+categoriesA['_id']}

        #recorremos cada imagen de cada categoria A
        for idxA in range(len(categoriesA['images'])):

            #ORB
            bestMatches = []        
            imageA = cv2.imread(pathA+categoriesA['images'][idxA]['imageName'], 0)
            kp1 = orb.detect(imageA,None)
            kp1, des1 = orb.compute(imageA, kp1)

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

                    kInageComputed = kInageComputed + 1

                    F = open(config['paths']['status-path']+"status.json","w+")
                    status = {
                                "sessionId": str(sessionId),
                                "method": "fastBatchStrict",
                                "absoluteComputed": str(kInageComputed),
                                "running":{
                                            "current":str(idxA+1), 
                                            "of":str(lengthA)
                                            },
                                "comparing":{
                                            "current":str(idxB+1), 
                                            "of":str(lengthB)
                                            }                     
                            }     

                    db.matchStatus.update({"sessionId":sessionId}, status, upsert=True)
                    F.write(json.dumps(status))
                    F.close()

                    imageB = cv2.imread(pathB+categoriesB['images'][idxB]['imageName'], 0)

                    #ORB
                    kp2 = orb.detect(imageB,None)
                    kp2, des2 = orb.compute(imageB, kp2)
                    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                    try:
                        matches = bf.match(des1,des2)                
                    except:                        
                        break               
                  

                    # Sort them in the order of their distance.
                    matches = sorted(matches, key = lambda x:x.distance)

                    good = []
                    for m in matches:
                        if m.distance < sensibility*100:
                                good.append(m)
            
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

    db.batchStats.insert({ "method":"fast", "totalMatches":totalMatches, "milisecondsElapsed": milisecondsElapsed, "oneMatch": milisecondsElapsed/totalMatches})      


    return {'matches': globalMatches, 'imagenesA': lengthA, 'imagenesB': lengthB, "milisecondsElapsed":milisecondsElapsed, "status":"OK"}

