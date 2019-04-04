let data = {
    "matches": [
        [
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/718345-MLB25590675552_052017-O.jpg",
                "percentage": "18.75",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-336.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/718345-MLB25590675552_052017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/CEV_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/718345-MLB25590675552_052017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/MR_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/718345-MLB25590675552_052017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/BL_Shampoo_300ml.jpg"
            }
        ],
        [
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "20.0",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-336.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "12.5",
                "image_repo": "joico/Shampoo/Recortadas/CEV_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "12.5",
                "image_repo": "joico/Shampoo/Recortadas/MR_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "12.5",
                "image_repo": "joico/Shampoo/Recortadas/BL_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/img459.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/852351-MLB25953742797_092017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/KPak_Shampoo_300ml.jpg"
            }
        ],
        [
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/613914-MLB26136044268_102017-O.jpg",
                "percentage": "15.0",
                "image_repo": "joico/Shampoo/Recortadas/BL_Shampoo_300ml.jpg"
            },
            {
                "image_url": "http://mlb-s1-p.mlstatic.com/613914-MLB26136044268_102017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-336.jpg"
            }
        ],
        [
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/822484-MLB25607553484_052017-O.jpg",
                "percentage": "16.25",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-306.jpg"
            },
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/822484-MLB25607553484_052017-O.jpg",
                "percentage": "15.0",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-276.jpg"
            },
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/822484-MLB25607553484_052017-O.jpg",
                "percentage": "12.5",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-336.jpg"
            }
        ],
        [
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/799190-MLB25607556738_052017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-306.jpg"
            }
        ],
        [
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/889420-MLB26237604967_102017-O.jpg",
                "percentage": "12.5",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-276.jpg"
            },
            {
                "image_url": "http://mlb-s2-p.mlstatic.com/889420-MLB26237604967_102017-O.jpg",
                "percentage": "11.25",
                "image_repo": "joico/Shampoo/Recortadas/Portifolio_Joico_Grande_0001-0040-306.jpg"
            }
        ]
    ],
    "imagenes1": 40,
    "imagenes2": 79
}

images = [];

data.matches.forEach(e=>{
    e.forEach(img=>{
        images.push(img) 
    })
})

images = images.sort((a,b)=>{
    
    if (a.percentage < b.percentage) {
        return 1;
      }
      if (a.percentage > b.percentage) {
        return -1;
      }

      return 0;
})

console.log(images)

