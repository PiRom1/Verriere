document.addEventListener('DOMContentLoaded', function () {

    const ventilateur_switch = document.getElementById("ventilateur-switch");
    const ventilateur_etat = document.getElementById('ventilateur-etat');
    let url;

    ventilateur_switch.addEventListener("change", function() {
        
        const allume = ventilateur_switch.checked;

        if (allume) {
            url = '/ventilateur/allumer';
        }
        else {
            url = '/ventilateur/eteindre';
        }

        console.log('url : ', url)

        fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            body: JSON.stringify({ventilateur_id : ventilateur_switch.getAttribute('data-id')})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('état changé !')
                if (allume) {
                    ventilateur_etat.innerHTML = "Allumé";
                }
                else {
                    ventilateur_etat.innerHTML = "Éteint";
                }
            }
        })
    });
        


});