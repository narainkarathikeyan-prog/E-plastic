from django.db import models
from django.utils import timezone


class PlasticType(models.Model):
    CATEGORY_CHOICES = [
        ('PET', 'PET - Polyethylene Terephthalate'),
        ('HDPE', 'HDPE - High-Density Polyethylene'),
        ('PVC', 'PVC - Polyvinyl Chloride'),
        ('LDPE', 'LDPE - Low-Density Polyethylene'),
        ('PP', 'PP - Polypropylene'),
        ('PS', 'PS - Polystyrene'),
        ('OTHER', 'Other Plastics'),
    ]
    code = models.CharField(max_length=10, choices=CATEGORY_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    recyclable = models.BooleanField(default=True)
    hazard_level = models.IntegerField(default=1)  # 1-5
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CollectionCenter(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    capacity_kg = models.FloatField(default=1000.0)
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class WasteSubmission(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('recycled', 'Recycled'),
        ('rejected', 'Rejected'),
    ]

    submitter_name = models.CharField(max_length=200)
    submitter_email = models.CharField(max_length=200)
    submitter_phone = models.CharField(max_length=20, blank=True)
    plastic_type = models.ForeignKey(PlasticType, on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    collection_center = models.ForeignKey(CollectionCenter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.submitter_name} - {self.weight_kg}kg"

    def save(self, *args, **kwargs):
        if self.weight_kg is not None:
            try:
                weight_as_number = float(self.weight_kg)
                calculated_points = int(weight_as_number * 10)
                if calculated_points > 9223372036854775807:
                    self.points_earned = 9223372036854775807
                else:
                    self.points_earned = calculated_points
            except (ValueError, TypeError):
                self.points_earned = 0
        else:
            self.points_earned = 0
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submitter_name} - {self.weight_kg}kg"


class RecyclingData(models.Model):
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    total_collected_kg = models.FloatField(default=0)
    total_recycled_kg = models.FloatField(default=0)
    co2_saved_kg = models.FloatField(default=0)
    energy_saved_kwh = models.FloatField(default=0)
    submissions_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['month', 'year']

    def __str__(self):
        return f"{self.month} {self.year}"


class DataMiningReport(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    insight = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    trend = models.CharField(max_length=20, default='stable')  # up, down, stable

    def __str__(self):
        return self.title
