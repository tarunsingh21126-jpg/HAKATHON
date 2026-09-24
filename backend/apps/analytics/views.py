from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from apps.containers.models import Container
from apps.orders.models import Order
from apps.returns.models import Return
from apps.users.models import User, SellerProfile
from apps.deposits.models import Deposit


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_analytics(request):
    if request.user.role != 'admin':
        return Response({'error': 'Forbidden'}, status=403)

    total_containers = Container.objects.count()
    total_orders = Order.objects.count()
    total_returns = Return.objects.filter(status='completed').count()
    total_users = User.objects.filter(role='customer').count()
    total_sellers = SellerProfile.objects.count()
    held_deposits = Deposit.objects.filter(status='held').count()
    total_deposit_value = sum(
        d.amount for d in Deposit.objects.filter(status='held')
    )

    # Container status breakdown
    status_breakdown = {}
    for choice in Container.STATUS_CHOICES:
        status_breakdown[choice[0]] = Container.objects.filter(status=choice[0]).count()

    return_rate = (total_returns / total_orders * 100) if total_orders > 0 else 0

    return Response({
        'total_containers': total_containers,
        'total_orders': total_orders,
        'total_returns': total_returns,
        'total_users': total_users,
        'total_sellers': total_sellers,
        'held_deposits': held_deposits,
        'total_deposit_value': float(total_deposit_value),
        'return_rate': round(return_rate, 1),
        'container_status': status_breakdown,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_analytics(request):
    if request.user.role != 'seller' and request.user.role != 'admin':
        return Response({'error': 'Forbidden'}, status=403)

    if request.user.role == 'seller':
        seller = request.user.seller_profile
    else:
        seller_id = request.query_params.get('seller_id')
        seller = SellerProfile.objects.get(id=seller_id) if seller_id else None

    if not seller:
        return Response({'error': 'Seller not found'}, status=404)

    containers = Container.objects.filter(seller=seller)
    total = containers.count()
    available = containers.filter(status='available').count()
    in_use = containers.filter(status__in=['assigned', 'delivered']).count()
    in_return = containers.filter(status__in=['return_requested', 'pickup_assigned', 'collected']).count()
    damaged = containers.filter(status='damaged').count()

    orders = Order.objects.filter(seller=seller)
    total_orders = orders.count()
    returns = Return.objects.filter(container__seller=seller, status='completed')
    total_returns = returns.count()
    return_rate = (total_returns / total_orders * 100) if total_orders > 0 else 0
    avg_uses = containers.aggregate(
        avg=__import__('django.db.models', fromlist=['Avg']).Avg('usage_count')
    )['avg'] or 0

    return Response({
        'total_containers': total,
        'available': available,
        'in_use': in_use,
        'in_return': in_return,
        'damaged': damaged,
        'total_orders': total_orders,
        'total_returns': total_returns,
        'return_rate': round(return_rate, 1),
        'avg_uses_per_container': round(float(avg_uses), 1),
    })
