from django.core.management.base import BaseCommand
from django.utils import timezone
from lands.models import Land
from bookings.models import PriceSetting
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample camping plots and pricing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...\n')
        
        # Create price setting
        price_setting, created = PriceSetting.objects.get_or_create(
            is_active=True,
            defaults={
                'price_per_night': Decimal('50.00'),
                'effective_from': timezone.now().date()
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created price setting: $50/night'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Price setting already exists'))
        
        # Sample camping plots
        sample_lands = [
            {
                'name': 'Lakeside Plot A',
                'description': 'Beautiful plot right by the lake with stunning sunset views. Perfect for families who love water activities and fishing.',
                'size': Decimal('150.00'),
                'capacity': 6,
                'amenities': 'Electricity, Water, Fire Pit, Picnic Table, BBQ Grill, Lake Access',
                'status': 'available'
            },
            {
                'name': 'Forest View Plot B',
                'description': 'Secluded spot surrounded by tall pines. Ideal for those seeking peace and privacy in nature.',
                'size': Decimal('120.00'),
                'capacity': 4,
                'amenities': 'Electricity, Water, Fire Pit, Hammock Posts',
                'status': 'available'
            },
            {
                'name': 'Mountain Ridge Plot C',
                'description': 'Elevated position with panoramic mountain views. Wake up to breathtaking sunrises.',
                'size': Decimal('180.00'),
                'capacity': 8,
                'amenities': 'Electricity, Water, Fire Pit, Picnic Table, BBQ Grill, Observation Deck',
                'status': 'available'
            },
            {
                'name': 'Riverside Plot D',
                'description': 'Situated along the gentle flowing river. Fall asleep to the soothing sounds of running water.',
                'size': Decimal('140.00'),
                'capacity': 5,
                'amenities': 'Electricity, Water, Fire Pit, River Access, Fishing Dock',
                'status': 'available'
            },
            {
                'name': 'Meadow Plot E',
                'description': 'Open meadow plot with wildflowers and plenty of sunshine. Great for stargazing at night.',
                'size': Decimal('200.00'),
                'capacity': 10,
                'amenities': 'Electricity, Water, Fire Pit, Picnic Table, BBQ Grill, Large Parking',
                'status': 'available'
            },
            {
                'name': 'Hilltop Plot F',
                'description': 'Private hilltop location with 360-degree views. Perfect for photographers and nature lovers.',
                'size': Decimal('130.00'),
                'capacity': 4,
                'amenities': 'Electricity, Water, Fire Pit, Bench Seating',
                'status': 'available'
            },
            {
                'name': 'Creekside Plot G',
                'description': 'Cozy plot next to a babbling creek. Shaded area perfect for summer camping.',
                'size': Decimal('110.00'),
                'capacity': 4,
                'amenities': 'Electricity, Water, Fire Pit, Creek Access, Shade Trees',
                'status': 'available'
            },
            {
                'name': 'Valley Plot H',
                'description': 'Nestled in a protected valley, sheltered from wind. Peaceful and quiet location.',
                'size': Decimal('160.00'),
                'capacity': 6,
                'amenities': 'Electricity, Water, Fire Pit, Picnic Table, BBQ Grill',
                'status': 'available'
            },
            {
                'name': 'Sunset Point Plot I',
                'description': 'Premium spot known for the most spectacular sunset views in the area.',
                'size': Decimal('170.00'),
                'capacity': 6,
                'amenities': 'Electricity, Water, Fire Pit, Picnic Table, Viewing Platform',
                'status': 'available'
            },
            {
                'name': 'Pioneer Plot J',
                'description': 'More rustic experience while still having essential amenities. For adventurous campers.',
                'size': Decimal('100.00'),
                'capacity': 3,
                'amenities': 'Water, Fire Pit, Basic Shelter',
                'status': 'available'
            },
        ]
        
        created_count = 0
        for land_data in sample_lands:
            land, created = Land.objects.get_or_create(
                name=land_data['name'],
                defaults=land_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {land.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Already exists: {land.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {created_count} new camping plots'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total camping plots in database: {Land.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data creation complete!'))
