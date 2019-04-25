const storageA = document.getElementById("storageA")
const storageB = document.getElementById("storageB")
const categories = document.getElementById("category")

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


    intersectedCategories = [];
    map = [];
    consolidatedGroups.forEach((e, i) => {

        if (e.group === stgA) {

            e.predictionsWeight.forEach(p => {
                Object.keys(p).forEach((c, i) => {
                    if (map.includes(c)) {
                        intersectedCategories.push(c);
                    }
                    else {
                        map.push(c);
                    }

                });
            })


        }

        if (e.group === stgB) {

            e.predictionsWeight.forEach(p => {
                Object.keys(p).forEach((c, i) => {
                    if (map.includes(c)) {
                        intersectedCategories.push(c);
                    }
                    else {
                        map.push(c);
                    }

                });
            })


        }

    })

    updateSelectIntersectedCategories(intersectedCategories)

}


const updateSelectIntersectedCategories = (intersectedCategories) => {

    categories.innerHTML = "";

    intersectedCategories.forEach(g => {

        const opt = document.createElement("option");
        opt.value = g;
        opt.textContent = g

        categories.appendChild(opt);
    })

}