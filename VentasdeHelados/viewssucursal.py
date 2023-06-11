from django.http import JsonResponse
from .models import Sucursal, Trabajador, Cargo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import SucursalSerializer, TrabajadorSerializer, CargoSerializer
from rest_framework import status
from rest_framework.parsers import JSONParser

#Sucursal
@csrf_exempt
@api_view(['GET','POST'])
def getsucursal(request):
    if request.method == 'GET':
        sucursales = Sucursal.objects.all()
        sucursales_serializers = SucursalSerializer(sucursales, many=True)
        return JsonResponse(sucursales_serializers.data, safe=False)
    elif request.method == 'POST':
        sucursales_data = JSONParser().parse(request)
        sucursales_serializer = SucursalSerializer(data = sucursales_data)
        if sucursales_serializer.is_valid():
            sucursales_serializer.save()
            return JsonResponse(sucursales_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(sucursales_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_sucursal(request, id):
    try: 
        sucursal = Sucursal.objects.get(codigo_sucursal=id) 
    except Sucursal.DoesNotExist: 
        return JsonResponse({'message': 'La sucursal no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        sucursal_serializer = SucursalSerializer(sucursal) 
        return JsonResponse(sucursal_serializer.data) 
    elif request.method == 'PUT': 
        sucursal_data = JSONParser().parse(request) 
        sucursal_serializer = SucursalSerializer(sucursal, data=sucursal_data) 
        if sucursal_serializer.is_valid(): 
            sucursal_serializer.save() 
            return JsonResponse(sucursal_serializer.data) 
        return JsonResponse(sucursal_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        sucursal.delete() 
        return JsonResponse({'message': 'Sucursal eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)
    
#Trabajador
@csrf_exempt
@api_view(['GET', 'POST'])
def getTrabajador(request):
    if request.method == 'GET':
        trabajador = Trabajador.objects.all()
        trabajador_serializer = TrabajadorSerializer(trabajador, many=True)
        return JsonResponse(trabajador_serializer.data, safe=False)
    elif request.method == 'POST':
        trabajador_data = JSONParser().parse(request)
        trabajador_serializer = TrabajadorSerializer(data=trabajador_data)
        if trabajador_serializer.is_valid():
            trabajador_serializer.save()
            return JsonResponse(trabajador_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(trabajador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_trabajador(request, id):
    try:
        trabajador = Trabajador.objects.get(rut_trabajador=id)
    except Trabajador.DoesNotExist:
        return JsonResponse({'message': 'El trabajador no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        trabajador_serializer = TrabajadorSerializer(trabajador)
        return JsonResponse(trabajador_serializer.data)
    elif request.method == 'PUT':
        trabajador_data = JSONParser().parse(request)
        trabajador_serializer = TrabajadorSerializer(trabajador, data=trabajador_data)
        if trabajador_serializer.is_valid():
            trabajador_serializer.save()
            return JsonResponse(trabajador_serializer.data)
        return JsonResponse(trabajador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        trabajador.delete()
        return JsonResponse({'message': 'Trabajador eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Cargo
@csrf_exempt
@api_view(['GET', 'POST'])
def getcargo(request):
    if request.method == 'GET':
        cargos = Cargo.objects.all()
        cargos_serializer = CargoSerializer(cargos, many=True)
        return JsonResponse(cargos_serializer.data, safe=False)
    elif request.method == 'POST':
        cargos_data = JSONParser().parse(request)
        cargos_serializer = CargoSerializer(data=cargos_data)
        if cargos_serializer.is_valid():
            cargos_serializer.save()
            return JsonResponse(cargos_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(cargos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_cargo(request, id):
    try: 
        cargo = Cargo.objects.get(codigo_cargo=id) 
    except Cargo.DoesNotExist: 
        return JsonResponse({'message': 'El cargo no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        cargo_serializer = CargoSerializer(cargo) 
        return JsonResponse(cargo_serializer.data) 
    elif request.method == 'PUT': 
        cargo_data = JSONParser().parse(request) 
        cargo_serializer = CargoSerializer(cargo, data=cargo_data) 
        if cargo_serializer.is_valid(): 
            cargo_serializer.save() 
            return JsonResponse(cargo_serializer.data) 
        return JsonResponse(cargo_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        cargo.delete() 
        return JsonResponse({'message': 'Cargo eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)