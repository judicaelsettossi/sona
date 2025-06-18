from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger('sona')

# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            occasion = request.POST.get('occasion')
            histoire = request.POST.get('story')
            style = request.POST.get('musical_style')
            voix = request.POST.get('voice_type')
            paroles = request.POST.get('lyrics')
            express = request.POST.get('express_delivery')
            pdf = request.POST.get('lyrics_pdf')
            video = request.POST.get('lyrics_video')
            email = request.POST.get('email')
            telephone = request.POST.get('phone')

            logger.info(f"Tentative d'envoi d'email pour une nouvelle commande - Occasion: {occasion}")

            # Stocker les informations dans une session
            request.session['user_data'] = {
                'occasion': occasion,
                'histoire': histoire,
                'style': style,
                'voix': voix,
                'paroles': paroles,
                'express': express,
                'pdf': pdf,
                'video': video,
                'email': email,
                'telephone': telephone,
            }

+            # Calcul du total
            base_price = 11.43
            total = base_price
            if express:
                total += 5
            if pdf:
                total += 5
            if video:
                total += 5

            # Message pour l'administrateur (sonareamusique@gmail.com)
            admin_message = f"""NOUVELLE COMMANDE SONAREA
=========================

DÉTAILS DE LA COMMANDE :
-----------------------
Occasion : {occasion}
Histoire : {histoire}
Style musical : {style}
Type de voix : {voix}
Paroles : {paroles}

OPTIONS CHOISIES :
-----------------
Livraison express : {'Oui (+5£)' if express else 'Non'}
Paroles en PDF : {'Oui (+5£)' if pdf else 'Non'}
Vidéo avec paroles : {'Oui (+5£)' if video else 'Non'}

DÉTAIL DES PRIX :
---------------
Prix de base : 11,43£
{'Livraison express : +5,00£' if express else ''}
{'Paroles en PDF : +5,00£' if pdf else ''}
{'Vidéo avec paroles : +5,00£' if video else ''}
Total à payer : {total:.2f}£

COORDONNÉES DU CLIENT :
----------------------
Email : {email}
Téléphone : {telephone}

Lien PayPal du client : https://www.paypal.com/paypalme/votrelien
"""

            # Envoi de l'email à sonareamusique@gmail.com
            logger.info("Envoi de l'email de commande à sonareamusique@gmail.com")
            send_mail(
                f'NOUVELLE COMMANDE SONAREA - {occasion}',
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                ['sonareamusique@gmail.com'],  # Email de réception des commandes
                fail_silently=False,
            )
            logger.info("Email de commande envoyé avec succès")

            # Message pour le client
            client_message = f"""Merci pour votre commande sur Sonarea !

DÉTAILS DE VOTRE COMMANDE :
--------------------------
Occasion : {occasion}
Style musical : {style}
Type de voix : {voix}

OPTIONS CHOISIES :
-----------------
Livraison express : {'Oui (+5£)' if express else 'Non'}
Paroles en PDF : {'Oui (+5£)' if pdf else 'Non'}
Vidéo avec paroles : {'Oui (+5£)' if video else 'Non'}

DÉTAIL DES PRIX :
---------------
Prix de base : 11,43£
{'Livraison express : +5,00£' if express else ''}
{'Paroles en PDF : +5,00£' if pdf else ''}
{'Vidéo avec paroles : +5,00£' if video else ''}
Total à payer : {total:.2f}£

PROCHAINES ÉTAPES :
------------------
1. Effectuez le paiement via PayPal : https://www.paypal.com/paypalme/votrelien
2. Notre équipe commencera à travailler sur votre chanson
3. Vous recevrez un email de confirmation

Si vous avez des questions, n'hésitez pas à nous contacter à sonareamusique@gmail.com

Cordialement,
L'équipe Sonarea"""

            # Envoi de l'email de confirmation au client
            logger.info(f"Envoi de l'email de confirmation au client: {email}")
            send_mail(
                'Confirmation de votre commande Sonarea',
                client_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Email du client
                fail_silently=False,
            )
            logger.info("Email de confirmation envoyé avec succès")

            # Redirection vers la page de commandes
            return HttpResponseRedirect(reverse('sona:commands'))

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi des emails: {str(e)}", exc_info=True)
            error_message = f"Une erreur est survenue lors de l'envoi des emails. Détails techniques: {str(e)}"
            return HttpResponse(error_message)

    # Si ce n'est pas une requête POST, afficher le formulaire
    return render(request, 'sona/index.html')

def commands(request):
    user_data = request.session.get('user_data', {})
    return render(request, 'sona/commands.html', {'user_data': user_data})

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'Ceci est un email de test envoyé depuis Django.',
            'sonareamusique@gmail.com',
            ['stevanngwa@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("Email envoyé avec succès.")
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")

def test_sendgrid_email(request):
    try:
        send_mail(
            'Sujet de test',
            'Ceci est un message envoyé via SendGrid.',
            'sonareamusique@gmail.com',
            ['stevanngwa@exemple.com'],
            fail_silently=False,
        )
        return HttpResponse("Email envoyé avec succès.")
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")

def payment(request):
    # Récupérer les données de la session
    user_data = request.session.get('user_data', {})
    
    # Définir les liens de paiement et leurs prix
    payment_links = {
        'default': {
            'link': 'https://pay.lygosapp.com/link/2c2b253b-7305-4c8e-9427-f26296948509',
            'price': 7300
        },
        'option1': {
            'link': 'https://pay.lygosapp.com/link/39182172-9b6b-4b61-84f8-2c5de1073f6a',
            'price': 10500
        },
        'option2': {
            'link': 'https://pay.lygosapp.com/link/c1830016-7d69-4806-a99b-aa0619b7b98a',
            'price': 13800
        },
        'option3': {
            'link': 'https://pay.lygosapp.com/link/c3afab7b-9480-4c1f-b227-6a264b891e74',
            'price': 17050
        }
    }
    
    # Compter le nombre d'options sélectionnées en convertissant les valeurs en booléens
    options_count = sum([
        1 if user_data.get('express') == 'on' else 0,
        1 if user_data.get('pdf') == 'on' else 0,
        1 if user_data.get('video') == 'on' else 0
    ])
    
    # Sélectionner le lien et le prix appropriés
    if options_count == 0:
        selected_payment = payment_links['default']
    elif options_count == 1:
        selected_payment = payment_links['option1']
    elif options_count == 2:
        selected_payment = payment_links['option2']
    else:
        selected_payment = payment_links['option3']

    context = {
        'user_data': user_data,
        'total_price': selected_payment['price'],
        'payment_link': selected_payment['link'],
        'options_count': options_count
    }
    return render(request, 'sona/payment.html', context)

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stripe_token = data.get('stripeToken')
            amount = data.get('amount')

            # Ici, vous pouvez ajouter la logique de traitement Stripe
            # Pour l'instant, nous simulons un succès
            return JsonResponse({
                'success': True,
                'message': 'Paiement traité avec succès'
            })
        except Exception as e:
            logger.error(f"Erreur lors du traitement du paiement: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def payment_success(request):
    return render(request, 'sona/payment_success.html')
