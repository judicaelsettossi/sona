// Gestion du formulaire
document.addEventListener('DOMContentLoaded', function() {
    // Sélection des éléments
    const startNowBtn = document.getElementById('start-now-btn');
    const openFormBtn = document.getElementById('open-form-btn');
    const formOverlay = document.getElementById('song-form-overlay');
    const closeFormBtn = document.getElementById('close-form-btn');
    const songForm = document.getElementById('song-form');
    const choixInput = document.getElementById('choix');

    // Fonction pour ouvrir le formulaire
    function openForm(occasion = '') {
        if (occasion) {
            choixInput.value = occasion;
        }
        formOverlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    // Afficher le formulaire au clic sur "Commencer maintenant"
    startNowBtn.addEventListener('click', function(e) {
        e.preventDefault();
        openForm();
    });

    // Afficher le formulaire au clic sur "Créez votre chanson"
    openFormBtn.addEventListener('click', function(e) {
        e.preventDefault();
        openForm();
    });

    // Afficher le formulaire avec occasion pré-remplie depuis les cartes
    document.querySelectorAll('[data-choix]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const occasion = this.getAttribute('data-choix');
            openForm(occasion);
        });
    });

    // Fermer le formulaire
    closeFormBtn.addEventListener('click', function() {
        formOverlay.classList.add('hidden');
        document.body.style.overflow = 'auto';
        // Réinitialiser le formulaire
        songForm.reset();
    });

    // Fermer en cliquant en dehors du formulaire
    formOverlay.addEventListener('click', function(e) {
        if (e.target === formOverlay) {
            formOverlay.classList.add('hidden');
            document.body.style.overflow = 'auto';
            // Réinitialiser le formulaire
            songForm.reset();
        }
    });

    // Gestion de la soumission du formulaire
    songForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Formulaire soumis');
        
        // Récupération des données du formulaire
        const formData = {
            occasion: document.getElementById('choix').value,
            histoire: document.getElementById('histoire').value,
            style: document.getElementById('stylemusical').value,
            voix: document.getElementById('genre').value,
            paroles: document.getElementById('paroles').value,
            options: {
                livraisonExpress: document.getElementById('livraison-express').checked,
                parolesPDF: document.getElementById('paroles-pdf').checked,
                videoParoles: document.getElementById('video-paroles').checked
            },
            contact: {
                email: document.getElementById('email').value,
                telephone: document.getElementById('telephone').value
            }
        };

        console.log('Données du formulaire à envoyer:', formData);

        // Envoi des données au serveur
        fetch('/submit-song-request/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            console.log('Réponse reçue:', response);
            return response.json();
        })
        .then(data => {
            console.log('Données reçues:', data);
            if (data.status === 'success') {
                alert(data.message);
                formOverlay.classList.add('hidden');
                document.body.style.overflow = 'auto';
                songForm.reset();
            } else {
                alert('Erreur : ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erreur lors de l\'envoi:', error);
            alert('Une erreur est survenue lors de l\'envoi du formulaire.');
        });
    });

    // Gestion de la FAQ
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            // Fermer toutes les autres questions
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            // Basculer l'état de la question cliquée
            item.classList.toggle('active');
        });
    });
    // Animation au scroll pour la FAQ
    const observerOptions = {
        threshold: 0.1
    };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    faqItems.forEach(item => {
        observer.observe(item);
    });
});
// Gestion du formulaire d'avis
document.addEventListener('DOMContentLoaded', function() {
    const openReviewBtn = document.getElementById('open-review-form-btn');
    const reviewFormContainer = document.getElementById('review-form-container');
    const reviewForm = document.getElementById('review-form');
    // Afficher le formulaire d'avis
    openReviewBtn.addEventListener('click', function() {
        reviewFormContainer.classList.toggle('hidden');
    });
    // Soumission du formulaire d'avis
    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('review-name').value;
        const rating = document.querySelector('input[name="rating"]:checked').value;
        const text = document.getElementById('review-text').value;
        // Ici vous pouvez envoyer l'avis à votre backend
        console.log('Nouvel avis:', { name, rating, text });
        // Afficher un message de confirmation
        alert('Merci pour votre avis !');
        // Réinitialiser et masquer le formulaire
        reviewForm.reset();
        reviewFormContainer.classList.add('hidden');
    });
});
// Gestion du menu burger
document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.getElementById('burger-menu');
    const mainNav = document.getElementById('main-nav');
    const navLinks = mainNav.querySelectorAll('a');
    burgerMenu.addEventListener('click', function() {
        burgerMenu.classList.toggle('active');
        mainNav.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });
    // Fermer le menu quand on clique sur un lien
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            burgerMenu.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
        });
    });
    // Fermer le menu quand on clique en dehors
    document.addEventListener('click', function(e) {
        if (!mainNav.contains(e.target) && !burgerMenu.contains(e.target)) {
            burgerMenu.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
});
// Gestion du formulaire premium
document.addEventListener('DOMContentLoaded', function() {
    const premiumLinks = document.querySelectorAll('.premium-link');
    const premiumFormOverlay = document.getElementById('premium-form-overlay');
    const closePremiumFormBtn = document.getElementById('close-premium-form-btn');
    const premiumForm = document.getElementById('premium-form');
    // Ouvrir le formulaire premium
    premiumLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            premiumFormOverlay.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        });
    });
    // Fermer le formulaire premium
    closePremiumFormBtn.addEventListener('click', function() {
        premiumFormOverlay.classList.add('hidden');
        document.body.style.overflow = 'auto';
    });
    // Fermer en cliquant en dehors
    premiumFormOverlay.addEventListener('click', function(e) {
        if (e.target === premiumFormOverlay) {
            premiumFormOverlay.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    });
    // Gestion de la soumission du formulaire premium
    premiumForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // Ici vous pouvez ajouter la logique de traitement du formulaire
        console.log('Formulaire premium soumis');
        premiumFormOverlay.classList.add('hidden');
        document.body.style.overflow = 'auto';
    });
});