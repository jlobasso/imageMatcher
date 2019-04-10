let categories = {'fountain_pen': 1, 'lens_cap': 1, 'chain': 6, 'laptop': 1, 'ballpoint': 1, 'analog_clock': 3, 'Crock_Pot': 1, 'brassiere':1, 'web_site': 27, 'menu': 4, 'broom': 1, 'stopwatch': 7, 'carton': 2, 'whiskey_jug': 1, 'vase': 5, 'whistle': 5, 'lighter': 4, 'abacus': 2, 'lab_coat': 1, 'pretzel': 3, 'perfume': 12, 'comic_book': 1, 'beer_glass': 1, 'typewriter_keyboard': 1, 'packet': 6, 'pill_bottle': 12, 'hair_spray': 468, 'candle': 2, 'loudspeaker': 1, 'lipstick': 20, 'lotion': 362, 'Band_Aid': 10, 'baseball': 7, 'saltshaker': 1, 'water_bottle': 31, "carpenter's_kit": 1, 'plane': 1, 'jersey': 3, 'wig': 9, 'can_opener': 7, 'caldron': 1, 'puck': 10, 'hook': 1, 'rubber_eraser': 1, 'syringe': 2, 'confectionery': 1, 'punching_bag': 1, 'moving_van': 4, 'cocktail_shaker': 1, 'envelope': 2, 'bottlecap': 1, 'bucket': 3, 'Petri_dish': 1, 'bow_tie': 1, 'bikini': 1, 'coffee_mug': 1, 'Yorkshire_terrier': 2, 'plastic_bag': 1, 'doormat': 7, 'ping-pong_ball': 1, 'handkerchief': 5, 'sunscreen': 125,'street_sign': 2, 'screw': 1, 'space_heater': 2, 'hand_blower': 3, 'magnetic_compass': 1, 'panpipe': 4, 'water_jug': 2, 'miniskirt': 1, 'toilet_tissue': 1, 'honeycomb': 1, 'wall_clock': 1, 'ashcan': 4, 'binoculars': 2, 'notebook': 1, 'measuring_cup': 5, 'brass': 2, 'safety_pin': 4, 'wine_bottle': 1, 'home_theater': 1, 'face_powder': 37, 'book_jacket': 9, 'switch': 1, 'barrel': 2, 'modem': 2, 'oil_filter': 21}


let categoriesPreSort = [];

// for(let cat in categories){
//     let tempObj = {}
//     tempObj[cat] = categories[cat] 
//     categoriesPreSort.push(tempObj)
// }

for (var cat in categories) {
    categoriesPreSort.push([cat, categories[cat]]);
}

let categorySorted = categoriesPreSort.sort(function(a, b) {
    return b[1] - a[1];
})

console.log(categorySorted)


let sum = 0;
//sum up n first categories
for(let i = 0; i<3; i++ ){
    // console.log(categorySorted[i][1])
     sum += categorySorted[i][1]
}

console.log(sum)