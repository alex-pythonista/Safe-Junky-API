from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from . import serializers, models


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_blood_group(request):
    try:
        data = request.data
        blood_group = data.get('blood_group')
        user = models.User.objects.get(id=request.user.id)
        models.EmergencyInformation.objects.create(user=user, blood_group=blood_group)
        return Response({
            'blood_group': blood_group,
            'message': 'Blood group added successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_blood_group(request):
    try:
        data = request.data
        blood_group = data.get('blood_group')
        emergency_info = models.EmergencyInformation.objects.get(user=request.user)
        emergency_info.blood_group = blood_group
        emergency_info.save()
        return Response({
            'Updated_blood_group': blood_group,
            'message': 'Blood group updated successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_contacts(request):
    try:
        contacts = models.ContactInformation.objects.filter(user=request.user)
        serializer = serializers.ContactsSerializers(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_contact(request, id=None):
    try:
        data = request.data
        contact = models.ContactInformation.objects.get(user=request.user, pk=id)
        contact.name = data.get('name')
        contact.phone_number = data.get('phone_number')
        contact.save()
        return Response({
            'Updated_contact': contact.name,
            'Updated_phone_number': contact.phone_number,
            'message': 'Contact updated successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    