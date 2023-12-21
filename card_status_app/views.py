import csv
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Card, CardEvent
from datetime import datetime

# getting the card's status: By passing either or both (card_id and mb number)
@require_http_methods(["GET"])

def get_card_status(request):
    phone_number = request.GET.get('phone_number')
    card_id = request.GET.get('card_id')

    if not phone_number and not card_id:
        return JsonResponse({'error': 'Provide either phone_number or card_id in the request.'}, status=400)

    try:
        if phone_number:
            card = get_object_or_404(Card, user_phone_number=phone_number)
        else:
            card = get_object_or_404(Card, card_id=card_id)

        card_events = CardEvent.objects.filter(card=card).order_by('timestamp')
        current_status = process_card_events(card_events)
        
        return JsonResponse({'card_status': current_status})
    
    except Http404:
        return JsonResponse({'error': 'Card not found.'}, status=404)

# Getting latest's status
def process_card_events(events):
    for event in events:
        if event.event_type == 'pickup':
            current_status = 'Picked up by courier partner'
        elif event.event_type == 'delivery_exception':
            current_status = f"Delivery exception: {event.comment}"
        elif event.event_type == 'delivered':
            current_status = 'Delivered'
        elif event.event_type == 'returned':
            current_status = 'Returned to us'
    
    return current_status


@require_http_methods(["GET"])

# Loading details into DB
def load_card_data(request):
    try:
        pickup_file_path = 'data/Pickup.csv'
        delivery_exceptions_file_path = 'data/Delivery_exceptions.csv'
        delivered_file_path = 'data/Delivered.csv'
        returned_file_path = 'data/Returned.csv'

        pickup_file = open(pickup_file_path, 'r')
        delivery_exceptions_file = open(delivery_exceptions_file_path, 'r')
        delivered_file = open(delivered_file_path, 'r')
        returned_file = open(returned_file_path, 'r')

        import_card_data(pickup_file, 'pickup')
        import_card_data(delivery_exceptions_file, 'delivery_exception')
        import_card_data(delivered_file, 'delivered')
        import_card_data(returned_file, 'returned')

        pickup_file.close()
        delivery_exceptions_file.close()
        delivered_file.close()
        returned_file.close()

        return JsonResponse({'message': 'Data loaded successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Store particular File data into
def import_card_data(file, event_type):
    reader = csv.DictReader(file)
    for row in reader:
        current_card_id = row['Card ID']
        current_phone_number = row.get('User Mobile') or row.get('User contact')

        card, created = Card.objects.get_or_create(
            card_id=current_card_id,
            defaults={'user_phone_number': current_phone_number.replace('"', '').replace('-', '')}
        )

        if not created:
            if card.user_phone_number != current_phone_number.replace('"', '').replace('-', ''):
                card.user_phone_number = current_phone_number.replace('"', '').replace('-', '')
                card.save()

        timestamp_str = row['Timestamp']
        formats_to_try = ["%Y-%m-%dT%H:%M:%SZ", "%d-%m-%Y %I:%M%p", "%d-%m-%Y %H:%M", "%d-%m-%Y %I:%M %p"]
        
        if event_type == "pickup":
            timestamp = datetime.strptime(timestamp_str, formats_to_try[3])
            
        elif event_type == "delivery_exception":
            timestamp = datetime.strptime(timestamp_str, formats_to_try[2])
            
        elif event_type == "returned":
            timestamp = datetime.strptime(timestamp_str, formats_to_try[1])
            
        else:
            timestamp = datetime.strptime(timestamp_str, formats_to_try[0])
            
        comment = row.get('Comment', '')

        CardEvent.objects.create(
            card=card,
            event_type=event_type,
            timestamp=timestamp,
            comment=comment
        )
