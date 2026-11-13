window.addEventListener('load', function () {

    const ventilateurs = JSON.parse(document.getElementById("ventilateurs").textContent);
    const capteurs = JSON.parse(document.getElementById("capteurs").textContent);

    const verriere = document.getElementById('img-verriere');

    // Mêmes seuil que les @media de base.css (téléphone en portrait)
    const MOBILE = window.matchMedia('(max-width: 700px)');

    const NB_ETAGES = 4;
    const RATIO_CAPTEUR = 670 / 375;      // hauteur / largeur de capteur.png
    const HAUTEUR_ENCART_MOBILE = 48;     // encart de mesures sous le capteur (téléphone)

    // Ventilateur : image fixe (éteint) ; allumé, un rotor animé par une planche de 36 frames (un tour complet) : voir base.css
    const IMAGE_VENTILATEUR = '/static/controller/img/ventilateur.png';
    const PLANCHE_ROTOR = '/static/controller/img/ventilateurs/rotation.png';

    // Décode la planche dès le chargement : sinon le premier tour peut clignoter
    const planche = new Image();
    planche.src = PLANCHE_ROTOR;
    planche.decode().catch(() => {});

    // Éléments créés une seule fois, puis repositionnés par positionner() (chargement, rotation du téléphone, redimensionnement)
    const ventilos_places = [];   // {item, interrupteur, etage}
    const capteurs_places = [];   // {item, encart, etage}

    function creer_item(src, avec_rotor = false) {
        // Crée un capteur/ventilateur : l'image, et pour un ventilateur le rotor animé par-dessus.
        const item = document.createElement('div');
        item.className = 'sw-item';  // centrage sur y + effet de survol : voir base.css

        const img = document.createElement('img');
        img.src = src;
        img.className = 'sw-item__frame';
        item.appendChild(img);

        if (avec_rotor) {
            const rotor = document.createElement('div');
            rotor.className = 'sw-item__rotor';
            item.appendChild(rotor);
        }

        document.body.appendChild(item);
        return item;
    }

    function creer_switch_input(est_allume) {
        // Crée un switch on/off. Renvoie [label, checkbox]
        // (écouter 'change' sur la checkbox ; input.checked = état voulu).
        const label = document.createElement('label');
        label.className = 'sw-switch';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.className = 'sw-switch__input';
        input.checked = Boolean(est_allume);

        const piste = document.createElement('span');
        piste.className = 'sw-switch__piste';

        label.append(input, piste);
        document.body.appendChild(label);
        return [label, input];
    }

    function creer_encart_mesures(temperature, humidite) {
        // Crée un petit encart "carnet de croquis" (temp + humidité)
        const encart = document.createElement('div');
        encart.className = 'sw-encart';

        const format = (valeur, unite) => valeur === null ? '–' : `${valeur.toFixed(1)}${unite}`;

        const ligne = (icone, texte) => {
            const div = document.createElement('div');
            div.className = 'sw-encart__ligne';
            // Les symboles SVG (#icone-thermometre, #icone-goutte) sont définis dans index.html
            div.innerHTML = `<svg class="sw-encart__icone"><use href="#${icone}"></use></svg>`;
            const valeur = document.createElement('span');
            valeur.className = 'sw-encart__valeur';
            valeur.textContent = texte;
            div.append(valeur);
            return div;
        };

        encart.append(ligne('icone-thermometre', format(temperature, '°C')), ligne('icone-goutte', format(humidite, '%')));
        document.body.appendChild(encart);
        return encart;
    }

    function positionner() {
        // Place ventilateurs (à droite) et capteurs (à gauche) en face de leurs étages.
        // Ordinateur : capteur à gauche avec l'encart à sa gauche. Téléphone : l'encart passe sous le capteur.
        const mobile = MOBILE.matches;
        const rect = verriere.getBoundingClientRect();

        // Coordonnées de la page (et non de la fenêtre) : on ajoute le défilement.
        const imgLeft = rect.left + window.scrollX;
        const imgTop = rect.top + window.scrollY;

        // L'image a des marges transparentes : on calibre sur le meuble lui-même (fractions de l'image).
        const meubleLeft = imgLeft + rect.width * 0.22;
        const meubleRight = imgLeft + rect.width * 0.78;
        const meubleTop = imgTop + rect.height * 0.09;
        const meubleHeight = rect.height * 0.82;
        const hauteurEtage = meubleHeight / NB_ETAGES;

        const largeurVentilo = rect.width / (mobile ? 9 : 8);
        const largeurCapteur = rect.width / (mobile ? 12 : 8);
        const ecart = rect.width / (mobile ? 60 : 30);  // espace entre le meuble et les images

        // y = milieu de l'étage (1 = en bas)
        const milieu_etage = etage => meubleTop + meubleHeight - (etage - 0.5) * hauteurEtage;

        ventilos_places.forEach(({item, interrupteur, etage}) => {
            const y = milieu_etage(etage);
            const x = meubleRight + ecart;  // x = bord gauche de l'image
            item.style.left = x + 'px';
            item.style.top = y + 'px';
            item.style.width = largeurVentilo + 'px';
            interrupteur.style.left = x + 'px';
            interrupteur.style.top = (y + largeurVentilo * 0.55 + 8) + 'px';  // sous l'image du ventilateur
            interrupteur.style.width = largeurVentilo + 'px';
        });

        capteurs_places.forEach(({item, encart, etage}) => {
            const y = milieu_etage(etage);
            const x = meubleLeft - ecart - largeurCapteur;  // à gauche on retire la largeur de l'image
            item.style.left = x + 'px';
            item.style.width = largeurCapteur + 'px';

            if (mobile) {
                // Capteur puis encart dessous, le bloc centré sur l'étage, alignés à droite contre le meuble
                const hauteurCapteur = largeurCapteur * RATIO_CAPTEUR;
                const haut = y - (hauteurCapteur + 4 + HAUTEUR_ENCART_MOBILE) / 2;
                item.style.top = (haut + hauteurCapteur / 2) + 'px';  // l'item est centré sur son top
                encart.style.left = (meubleLeft - ecart) + 'px';
                encart.style.top = (haut + hauteurCapteur + 4) + 'px';
            } else {
                item.style.top = y + 'px';
                encart.style.left = (x - ecart) + 'px';
                encart.style.top = y + 'px';
            }
        });
    }

    ventilateurs.forEach(ventilateur => {

        let item = creer_item(IMAGE_VENTILATEUR, true);
        item.addEventListener('click', function() {
            window.location.href = `/ventilateur/${ventilateur.ventilateur.id}`;
        })
        let [interrupteur, switch_input] = creer_switch_input(ventilateur.etat);
        ventilos_places.push({item, interrupteur, etage: ventilateur.ventilateur.etage});

        // 'allume' : l'animation est lancée (et reste, pour garder la frame en cours à l'arrêt)
        // 'arret' : l'animation est mise en pause sur la frame affichée
        if (switch_input.checked) {
            item.classList.add('sw-item--allume');
        }

        switch_input.addEventListener('change', function() {

            if (switch_input.checked) {
                item.classList.add('sw-item--allume');
            }
            item.classList.toggle('sw-item--arret', !switch_input.checked);

            const url = switch_input.checked ? '/ventilateur/allumer' : '/ventilateur/eteindre';

            fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            body: JSON.stringify({ventilateur_id : ventilateur.ventilateur.id})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('état changé !')
                }
            })

        })

    })

    capteurs.forEach(capteur => {
        let item = creer_item('/static/controller/img/capteur.png');
        item.addEventListener('click', function() {
            window.location.href = `/capteur/${capteur.capteur.id}`;
        })
        const encart = creer_encart_mesures(capteur.temperature, capteur.humidite);
        capteurs_places.push({item, encart, etage: capteur.capteur.etage});
    })

    positionner();

    // Rotation du téléphone / redimensionnement : on repositionne (sans recréer les éléments)
    let minuterie;
    window.addEventListener('resize', function() {
        clearTimeout(minuterie);
        minuterie = setTimeout(positionner, 150);
    });

});