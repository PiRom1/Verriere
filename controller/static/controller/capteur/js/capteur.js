document.addEventListener('DOMContentLoaded', function () {

    const capteur_temperature = document.getElementById('capteur-temperature');
    const capteur_humidite = document.getElementById('capteur-humidite');
    const capteur_button = document.getElementById('get-capteur-mesure');
    const capteur_id = capteur_button.getAttribute('capteur-id');

    capteur_button.addEventListener("click", function() {

        fetch("/capteur/get_temperature_humidite", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: JSON.stringify({ capteur_id: capteur_id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Mesures prises !')
                capteur_temperature.innerHTML = `${data.data.temperature}°C`;
                capteur_humidite.innerHTML = `${data.data.humidite}%`;
            }
        })
    });
        


});