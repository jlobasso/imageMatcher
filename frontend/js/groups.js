const storageA = document.getElementById("storageA")
const storageB = document.getElementById("storageB")
const categories = document.getElementById("category")
const totalImagesC = document.getElementById("totalImages")

var consolidatedGroups = [];

var getGroups = async () => {

    return await fetch(conf.urlBackend + 'groups')
        .then((res) => res.json())

}

var updateGroupsSelects = async () => {

    const groups = await getGroups();

    consolidatedGroups = groups;
    
    storageA.innerHTML = "";
    storageB.innerHTML = "";

    const optA0 = document.createElement("option");
    optA0.value = 0;
    optA0.textContent = "Seleccione...";
    const optB0 = document.createElement("option");
    optB0.value = 0;
    optB0.textContent = "Seleccione...";
        
    storageA.appendChild(optA0);
    storageB.appendChild(optB0);

    groups.forEach((g,i)=> {


        const optA = document.createElement("option");
        optA.value = g.group;
        optA.textContent = g.group
        // if(!i) optA.setAttribute('selected', true);

        const optB = document.createElement("option");
        optB.value = g.group;
        optB.textContent = g.group;
        // if(!i) optB.setAttribute('selected', true);

        storageA.appendChild(optA);
        storageB.appendChild(optB);
    })

}


storageA.addEventListener('change', () => {
    calculateIntersectionCategories()
})
storageB.addEventListener('change', () => {
    calculateIntersectionCategories()
})

const calculateIntersectionCategories = () => {
    const stgA = storageA.options[storageA.selectedIndex].value;
    const stgB = storageB.options[storageB.selectedIndex].value;

    if(!stgA || !stgB) return;

    totalImages = 0;

    intersectedCategories = [];
    map = [];
    cant = {}
    consolidatedGroups.forEach((e, i) => {

        if (e.group === stgA) {

            e.predictionsWeight.forEach(p => {
                Object.keys(p).forEach((c, i) => {
                    if (map.includes(c)) {
                        let q = parseInt(cant[c]) + parseInt(p[c])
                        totalImages += q;
                        intersectedCategories.push(c+ ": " + q);
                    }
                    else {
                        map.push(c);
                        cant[c] = p[c]
                        // console.log(p[c])
                    }

                });
            })


        }

        if (e.group === stgB) {

            e.predictionsWeight.forEach(p => {
                Object.keys(p).forEach((c, i) => {
                    if (map.includes(c)) {
                        let q = parseInt(cant[c]) + parseInt(p[c]);
                        totalImages += q;
                        intersectedCategories.push(c+ ": " + q);
                    }
                    else {
                        map.push(c);
                        cant[c] = p[c]
                    }

                });
            })


        }

    })
        
    updateSelectIntersectedCategories(intersectedCategories, totalImages)

}


const updateSelectIntersectedCategories = (intersectedCategories) => {

    categories.innerHTML = "";
    categories.size = intersectedCategories.length;
    totalImagesC.innerHTML = "Total: "+totalImages
    // if(!intersectedCategories.lenght){
    //     const optC0 = document.createElement("option");
    //     optC0.value = 0;
    //     optC0.textContent = "Seleccione...";
    
    //     categories.appendChild(optC0);
    // }


    intersectedCategories.forEach(g => {

        const opt = document.createElement("option");
        opt.value = g;
        opt.textContent = g

        categories.appendChild(opt);
    })

}