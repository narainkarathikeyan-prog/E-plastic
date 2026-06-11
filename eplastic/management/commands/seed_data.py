import random
from django.core.management.base import BaseCommand
from eplastic.models import PlasticType, CollectionCenter, WasteSubmission, DataMiningReport


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Plastic types
        plastics = [
            ('PET', 'Polyethylene Terephthalate', True, 2, 'Used in water bottles and food containers'),
            ('HDPE', 'High-Density Polyethylene', True, 1, 'Used in milk jugs and detergent bottles'),
            ('PVC', 'Polyvinyl Chloride', False, 4, 'Used in pipes and cable insulation'),
            ('LDPE', 'Low-Density Polyethylene', True, 2, 'Used in plastic bags and squeezable bottles'),
            ('PP', 'Polypropylene', True, 1, 'Used in yogurt containers and bottle caps'),
            ('PS', 'Polystyrene', False, 3, 'Used in foam cups and disposable cutlery'),
            ('OTHER', 'Other Plastics', False, 3, 'Mixed or unclassified plastics'),
        ]
        for code, name, recyclable, hazard, desc in plastics:
            PlasticType.objects.get_or_create(code=code, defaults={
                'name': name, 'recyclable': recyclable, 'hazard_level': hazard, 'description': desc
            })

        # Collection centers
        centers_data = [
            ('EcoRecycle Hub - Bengaluru', 'Bengaluru', 'Karnataka', 'Koramangala, Bengaluru - 560034', '+91-9876543210', 5000, 12.9352, 77.6245),
            ('Green Waste Center - Chennai', 'Chennai', 'Tamil Nadu', 'Anna Nagar, Chennai - 600040', '+91-9876543211', 3000, 13.0827, 80.2707),
            ('Plastic Collect - Mumbai', 'Mumbai', 'Maharashtra', 'Andheri West, Mumbai - 400058', '+91-9876543212', 8000, 19.1136, 72.8697),
            ('Recycle Point - Delhi', 'Delhi', 'Delhi', 'Connaught Place, New Delhi - 110001', '+91-9876543213', 6000, 28.6315, 77.2167),
            ('EWaste Hub - Hyderabad', 'Hyderabad', 'Telangana', 'Hitech City, Hyderabad - 500081', '+91-9876543214', 4000, 17.4435, 78.3772),
            ('CleanEarth - Pune', 'Pune', 'Maharashtra', 'Kothrud, Pune - 411038', '+91-9876543215', 2500, 18.5074, 73.8077),
        ]
        centers = []
        for name, city, state, addr, contact, cap, lat, lng in centers_data:
            c, _ = CollectionCenter.objects.get_or_create(name=name, defaults={
                'city': city, 'state': state, 'address': addr,
                'contact': contact, 'capacity_kg': cap, 'latitude': lat, 'longitude': lng
            })
            centers.append(c)

        # Sample submissions
        names = ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Rao', 'Vijay Nair',
                 'Ananya Singh', 'Ravi Menon', 'Deepa Gupta', 'Arjun Das', 'Kavya Reddy']
        statuses = ['pending', 'collected', 'processing', 'recycled', 'recycled']
        plastic_types = list(PlasticType.objects.all())

        if WasteSubmission.objects.count() < 30:
            for i in range(40):
                name = random.choice(names)
                WasteSubmission.objects.create(
                    submitter_name=name,
                    submitter_email=f"{name.lower().replace(' ', '.')}@example.com",
                    submitter_phone=f"+91-{random.randint(7000000000, 9999999999)}",
                    plastic_type=random.choice(plastic_types),
                    weight_kg=round(random.uniform(0.5, 50.0), 2),
                    collection_center=random.choice(centers),
                    status=random.choice(statuses),
                    description=f"E-waste plastic collected from household/office"
                )

        # Data mining reports
        reports = [
            ('PET Dominance Pattern', 'Pattern Mining', 'PET plastics constitute 38% of all submissions, indicating widespread single-use bottle disposal. Targeted collection drives at events could yield 2x more PET recovery.', 'up'),
            ('Urban Concentration Analysis', 'Geographic Analysis', 'Over 70% of submissions originate from tier-1 cities. Rural outreach programs could significantly expand collection volumes.', 'stable'),
            ('Seasonal Weight Variation', 'Time Series Analysis', 'Average submission weight peaks in January-February and July-August, correlating with festival seasons and increased consumer activity.', 'up'),
            ('Recycling Efficiency Score', 'Efficiency Metrics', 'Current recycling rate stands at 67%. With improved sorting algorithms and center capacity, efficiency could reach 85% within 6 months.', 'up'),
            ('Hazardous Plastic Risk Alert', 'Risk Analysis', 'PVC submissions have increased 15% this quarter. Enhanced handling protocols and specialized processing required.', 'down'),
        ]
        for title, cat, insight, trend in reports:
            DataMiningReport.objects.get_or_create(title=title, defaults={
                'category': cat,
                'description': f'Data mining analysis on {cat.lower()}',
                'insight': insight,
                'trend': trend
            })

        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))
