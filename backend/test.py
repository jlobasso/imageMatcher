from pymongo import MongoClient

conn = MongoClient()
db = conn.imageMatcher


cursorA = db['suspected-carloschanta'].aggregate([
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
                '$in': ['wig', 'web_site']
            }
        }
    }
    ])

#recorremos cada categoria A
for categoriesA in cursorA:
        print("A ---->",len(categoriesA['images']))
        # print(groupA['_id'])
        #recorremos cada imagen de cada categoria A
        for idxA in range(len(categoriesA['images'])): 

                cursorB = db['suspected-pepe12345'].aggregate([
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
                print("IMG---A ---->",idxA)
                #recorremos cada imagen de cada categoria B        
                for categoriesB in cursorB:
                        for idxB in range(len(categoriesB['images'])):
                                print("B ---->",idxB)