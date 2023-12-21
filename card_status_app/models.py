from django.db import models

# model for card
class Card(models.Model):
    card_id = models.CharField(max_length=50, unique=True)
    user_phone_number = models.CharField(max_length=12)

#model of Card event, storing event_type, etc details
class CardEvent(models.Model):
    EVENT_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery_exception', 'Delivery Exception'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
