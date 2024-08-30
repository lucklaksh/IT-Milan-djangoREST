from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import viewsets, status
from .models import Milan, Responsibility, User, Address, Reports, CommonUser
from .serializers import MilanSerializer, ResponsibilitySerializer, UserSerializer, AddressSerializer, ReportsSerializer, CommonUserSerializer, MembersSerializer, RoleCountSerializer, CommonUserMembersSerializer, ViewProfileSerializer, CustomUserSerializer
from django.http import JsonResponse
from django.utils import timezone

from django.db.models import Count


@api_view(['GET'])
def index (request):
    courses={
        'course_naem': 'Python',
        'learn' : ['flask', 'Dango'],
    }
    return Response (courses)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            return JsonResponse({"user_id": user.id, "milan_id": user.milan.id}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@api_view(['GET'])
def members_view(request):
    user_id = request.GET.get('user_id') 
    try:
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
        milan_id = user.milan
        members = User.objects.filter(milan=milan_id)
        members_serialized = MembersSerializer(members, many=True)
        return JsonResponse(members_serialized.data, safe=False, status=200)
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

# all milan members belong to particular milan
@api_view(['GET'])
def milan_members_view(request):
    milan_id = request.GET.get('milan_id') 
    try:
        # user_id = int(user_id)
        # user = User.objects.get(id=user_id)
        # milan_id = user.milan
        members = User.objects.filter(milan=milan_id)
        members_serialized = MembersSerializer(members, many=True)
        return JsonResponse(members_serialized.data, safe=False, status=200)
    
    except Milan.DoesNotExist:
        return JsonResponse({"error": "Milan not found"}, status=404)

@api_view(['GET'])
def profile_view(request):
    user_id = request.GET.get('user_id')
    try:
        user_id = int(user_id)
        profile = User.objects.get(id=user_id) 
        profile_serialized = ViewProfileSerializer(profile)
        return JsonResponse(profile_serialized.data, safe=False, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@api_view(['GET'])
def address_view(request):
    user_id = request.GET.get('user_id')
    try:
        user_id = int(user_id)
        profile = Address.objects.filter(user=user_id) 
        profile_serialized = AddressSerializer(profile, many=True)
        return JsonResponse(profile_serialized.data, safe=False, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "Address not found"}, status=404)


@api_view(['GET'])
def roles_count_view(request):
    milan_id = request.query_params.get('milan_id')
    fromdate = request.query_params.get('fromdate')
    todate = request.query_params.get('todate')

    if not milan_id or not fromdate or not todate:
        return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date = timezone.datetime.strptime(fromdate, '%Y-%m-%d').date()
        to_date = timezone.datetime.strptime(todate, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter reports by milan_id and the date range
    reports = Reports.objects.filter(
        milan_id=milan_id,
        created_at__date__range=(from_date, to_date)
    )

    # Aggregate the count of roles grouped by date and role, and get related names
    role_counts = reports.values('created_at__date', 'role__role_name') \
                         .annotate(count=Count('id')) \
                         .order_by('created_at__date', 'role__role_name')

    # Group the names by date and role
    names_by_role = {}
    for report in reports:
        date = report.created_at.date().strftime('%Y-%m-%d')
        role_name = report.role.role_name

        # Check which name to use: either user or commonuser
        name = None
        if hasattr(report, 'user') and report.user is not None:
            name = report.user.name  # Assuming user model has a 'name' field
        elif hasattr(report, 'common_user') and report.common_user is not None:
            name = report.common_user.name  # Assuming commonuser model has a 'name' field

        if not name:
            # Skip this entry if no valid name is found
            continue

        if date not in names_by_role:
            names_by_role[date] = {}

        if role_name not in names_by_role[date]:
            names_by_role[date][role_name] = {"count": 0, "names": []}

        # Collect the names and increment the count
        names_by_role[date][role_name]["names"].append(name)

    # Combine count data and names for the response
    response_data = {}
    for entry in role_counts:
        date = entry['created_at__date'].strftime('%Y-%m-%d')  # Convert to string format
        role_name = entry['role__role_name']
        count = entry['count']

        if date not in response_data:
            response_data[date] = {}

        # Safely access names_by_role to avoid KeyError
        role_data = names_by_role.get(date, {}).get(role_name, {"names": []})

        response_data[date][role_name] = {
            "count": count,
            "names": role_data["names"]  # This will be an empty list if the key is missing
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def report_view(request):
    data = request.data
    milan_id = data.get('milan_id')
    users = data.get('users')
    commoners = data.get('commoners')
    date = data.get('date')
    try:
        day = timezone.datetime.strptime(date, '%Y-%m-%d').date() 
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    Reports.objects.filter(
            milan_id=milan_id,
            created_at__date=day
        ).delete()
     # Prepare lists for bulk creation
    report_entries = []

    # Process 'users' data
    for user_data in users:
        user_id = user_data.get('user_id')
        try:
            user = User.objects.get(id=user_id)  # Fetch the user object
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        
        report_entries.append(Reports(
            milan_id=milan_id,
            user=user,
            role=user.role,  # Automatically assign role from User model
            created_at=day,
            updated_at=timezone.now()
        ))
    
    # Process 'commoners' data
    for commoner_data in commoners:
        commoner_id = commoner_data.get('commoner_id')
        try:
            commoner = CommonUser.objects.get(id=commoner_id)  # Fetch the commoner object
        except CommonUser.DoesNotExist:
            return Response({"error": f"CommonUser with id {commoner_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        report_entries.append(Reports(
            milan_id=milan_id,
            common_user=commoner,
            role=commoner.role,  # Automatically assign role from CommonUser model
            created_at=day,
            updated_at=timezone.now()
        ))

    # Bulk create reports to optimize database operations
    Reports.objects.bulk_create(report_entries)
    return Response({"message": "Reports updated successfully."}, status=status.HTTP_200_OK)



@api_view(['GET'])
def commonuser_members_view(request):
    user_id = request.GET.get('user_id') 
    try:
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
        milan_id = user.milan
        members = CommonUser.objects.filter(milan=milan_id)
        members_serialized = CommonUserMembersSerializer(members, many=True)
        return JsonResponse(members_serialized.data, safe=False, status=200)
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@api_view(['POST'])
def register_user_view(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'User created and email sent'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def commonuser_milan_members_view(request):
    milan_id = request.GET.get('milan_id') 
    try:
        # user_id = int(user_id)
        # user = User.objects.get(id=user_id)
        # milan_id = user.milan
        commoners = CommonUser.objects.filter(milan=milan_id)
        commoners_serialized = CommonUserMembersSerializer(commoners, many=True)
        return JsonResponse(commoners_serialized.data, safe=False, status=200)
    
    except Milan.DoesNotExist:
        return JsonResponse({"error": "Milan not found"}, status=404)

class MilanViewSet(viewsets.ModelViewSet):
    queryset = Milan.objects.all()
    serializer_class = MilanSerializer

class ResponsibilityViewSet(viewsets.ModelViewSet):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

class CommonUserViewSet(viewsets.ModelViewSet):
    queryset = CommonUser.objects.all()
    serializer_class = CommonUserSerializer
