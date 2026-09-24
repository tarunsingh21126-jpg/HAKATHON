"""
PackBack Demo Data Seeder
Run with: python seed.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'packback.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from datetime import timedelta, date
import random

from apps.users.models import User, SellerProfile
from apps.containers.models import Container
from apps.orders.models import Order
from apps.returns.models import Return, DropOffLocation
from apps.deposits.models import Deposit
from apps.rewards.models import Reward

print("🌱 Seeding PackBack demo data...")

# Clear existing data
print("  Clearing existing data...")
Reward.objects.all().delete()
Deposit.objects.all().delete()
Return.objects.all().delete()
Order.objects.all().delete()
Container.objects.all().delete()
DropOffLocation.objects.all().delete()
User.objects.all().delete()

# ─── ADMIN ───────────────────────────────────────────────────────────────────
admin = User.objects.create_superuser(
    email='admin@packback.app',
    password='admin123',
    name='PackBack Admin',
)
print(f"  ✓ Admin: admin@packback.app / admin123")

# ─── SELLERS ─────────────────────────────────────────────────────────────────
seller_data = [
    ('greenleaf@packback.app', 'GreenLeaf Organics', 'B-12, Green Market, Bengaluru'),
    ('freshmart@packback.app', 'FreshMart Daily', 'Shop 4, Koramangala, Bengaluru'),
    ('techbox@packback.app', 'TechBox India', '3rd Floor, Indiranagar, Bengaluru'),
]

sellers = []
seller_users = []
for i, (email, biz, addr) in enumerate(seller_data):
    u = User.objects.create_user(
        email=email, password='seller123', name=biz.split()[0] + ' Owner', role='seller'
    )
    sp = SellerProfile.objects.create(user=u, business_name=biz, business_address=addr, status='active')
    sellers.append(sp)
    seller_users.append(u)
    print(f"  ✓ Seller: {email} / seller123")

# ─── CUSTOMERS ───────────────────────────────────────────────────────────────
customer_data = [
    ('tarun@example.com', 'Tarun Sharma', '+91 9876543210'),
    ('priya@example.com', 'Priya Nair', '+91 9876543211'),
    ('arjun@example.com', 'Arjun Mehta', '+91 9876543212'),
    ('sneha@example.com', 'Sneha Patel', '+91 9876543213'),
    ('rohit@example.com', 'Rohit Kumar', '+91 9876543214'),
]

customers = []
for email, name, phone in customer_data:
    u = User.objects.create_user(
        email=email, password='customer123', name=name, phone=phone, role='customer'
    )
    customers.append(u)
    print(f"  ✓ Customer: {email} / customer123")

# ─── DROP-OFF LOCATIONS ───────────────────────────────────────────────────────
dropoff_data = [
    ('PackBack Hub — Koramangala', '5th Block, Koramangala, Bengaluru', 'Bengaluru'),
    ('PackBack Hub — Indiranagar', '100 Feet Road, Indiranagar, Bengaluru', 'Bengaluru'),
    ('PackBack Hub — HSR Layout', 'Sector 6, HSR Layout, Bengaluru', 'Bengaluru'),
    ('PackBack Hub — Jayanagar', '4th Block, Jayanagar, Bengaluru', 'Bengaluru'),
]

dropoffs = []
for name, addr, city in dropoff_data:
    d = DropOffLocation.objects.create(name=name, address=addr, city=city, is_active=True)
    dropoffs.append(d)
print(f"  ✓ {len(dropoffs)} drop-off locations created")

# ─── CONTAINERS ──────────────────────────────────────────────────────────────
statuses = ['available', 'available', 'available', 'delivered', 'return_requested', 'cleaning', 'damaged']
containers = []
for i in range(60):
    seller = sellers[i % len(sellers)]
    status = statuses[i % len(statuses)]
    c = Container(
        seller=seller,
        status=status,
        deposit_amount=100.00,
        usage_count=random.randint(0, 15),
        condition='good' if status != 'damaged' else 'damaged',
    )
    c.save()
    containers.append(c)

print(f"  ✓ {len(containers)} containers created (with QR codes)")

# ─── ORDERS & DEPOSITS ───────────────────────────────────────────────────────
delivered_containers = [c for c in containers if c.status == 'delivered']
for i, container in enumerate(delivered_containers):
    customer = customers[i % len(customers)]
    order = Order(
        seller=container.seller,
        customer=customer,
        container=container,
        customer_address='123 Sample Street, Bengaluru',
        delivery_status='delivered',
        delivered_at=timezone.now() - timedelta(days=random.randint(1, 7)),
    )
    order.save()
    container.current_customer = customer
    container.save()
    Deposit.objects.create(
        customer=customer,
        container=container,
        amount=100.00,
        status='held',
    )

# Some completed orders with refunded deposits
for i in range(15):
    customer = customers[i % len(customers)]
    available_c = [c for c in containers if c.status == 'available' and c.usage_count > 0]
    if not available_c:
        continue
    c = available_c[i % len(available_c)]
    order = Order(
        seller=c.seller,
        customer=customer,
        container=c,
        customer_address='456 Demo Lane, Bengaluru',
        delivery_status='delivered',
        delivered_at=timezone.now() - timedelta(days=random.randint(10, 30)),
    )
    order.save()
    Deposit.objects.create(
        customer=customer,
        container=c,
        amount=100.00,
        status='refunded',
        refunded_at=timezone.now() - timedelta(days=random.randint(1, 10)),
    )

print(f"  ✓ Orders and deposits seeded")

# ─── RETURNS ─────────────────────────────────────────────────────────────────
return_requested = [c for c in containers if c.status == 'return_requested']
for i, c in enumerate(return_requested):
    customer = customers[i % len(customers)]
    c.current_customer = customer
    c.save()
    Return.objects.create(
        container=c,
        customer=customer,
        method='pickup' if i % 2 == 0 else 'dropoff',
        pickup_address='123 Sample Street, Bengaluru' if i % 2 == 0 else '',
        pickup_date=date.today() + timedelta(days=1),
        dropoff_location=dropoffs[i % len(dropoffs)] if i % 2 != 0 else None,
        status='requested',
    )

# Some completed returns
for i in range(20):
    customer = customers[i % len(customers)]
    c = containers[i]
    Return.objects.create(
        container=c,
        customer=customer,
        method='pickup' if i % 2 == 0 else 'dropoff',
        pickup_address='789 Return Ave, Bengaluru',
        status='completed',
        requested_at=timezone.now() - timedelta(days=random.randint(5, 20)),
        completed_at=timezone.now() - timedelta(days=random.randint(1, 5)),
    )

print(f"  ✓ Returns seeded")

# ─── REWARDS ─────────────────────────────────────────────────────────────────
for customer in customers:
    for j in range(random.randint(3, 8)):
        Reward.objects.create(
            customer=customer,
            points=50,
            transaction_type='earned',
            description=f'Return of container #{j+1}',
            created_at=timezone.now() - timedelta(days=random.randint(1, 60)),
        )
    if random.random() > 0.5:
        Reward.objects.create(
            customer=customer,
            points=-100,
            transaction_type='redeemed',
            description='₹20 coupon redeemed',
        )

print(f"  ✓ Rewards seeded")

print("\n✅ Seeding complete!")
print("\n  🔑 Login credentials:")
print("     Admin:    admin@packback.app    / admin123")
print("     Seller:   greenleaf@packback.app / seller123")
print("     Customer: tarun@example.com     / customer123")
print("\n  🌐 Start servers:")
print("     Backend:  python manage.py runserver")
print("     Frontend: cd ../frontend && npm run dev")
