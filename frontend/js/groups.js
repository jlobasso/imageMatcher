var getGroups = async () => {

    return await fetch(conf.urlBackend + 'groups')
        .then((res) => res.json())
        
}

var updateGroupsSelects = async () => {

    const gropus = await getGroups();
    
    const storageA = document.getElementById("storageA")
    const storageB = document.getElementById("storageB")

    gropus.forEach(g=>{
        const optA = document.createElement("option");
        optA.value = g.group;
        optA.textContent = g.group;

        const optB = document.createElement("option");
        optB.value = g.group;
        optB.textContent = g.group;
        
        storageA.appendChild(optA);
        storageB.appendChild(optB);
    })

}