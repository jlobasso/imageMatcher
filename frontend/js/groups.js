var getGroups = () => {

    fetch('status/status.json?' + Math.random() + '=' + Math.random())
        .then((response) => response.json())
        .then((status) => {
            statusInfo.innerHTML = `Completado: ${Math.floor((status.absoluteComputed / (status.running.of * status.comparing.of)) * 100)}%
                                    Recorriendo ${status.running.current} 
                                    de ${status.running.of} 
                                    comparando con ${status.comparing.current} 
                                    de ${status.comparing.of}`
            cantAnalizadas = status.comparing.of * status.running.of
        }

        )

}