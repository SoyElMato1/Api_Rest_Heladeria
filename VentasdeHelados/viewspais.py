from django.http import JsonResponse
from .models import Comuna, Provincia, Region
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import RegionSerializer, ProvinciaSerializer, ComunaSerializer
from rest_framework import status
from rest_framework.parsers import JSONParser

#Region
@csrf_exempt
@api_view(['GET','POST'])
def getregion(request):
    if request.method == 'GET':
        regiones = Region.objects.all()
        regiones_serializers = RegionSerializer(regiones, many=True)
        return JsonResponse(regiones_serializers.data, safe=False)
    elif request.method == 'POST':
        regiones_data = JSONParser().parse(request)
        regiones_serializer = RegionSerializer(data = regiones_data)
        if regiones_serializer.is_valid():
            regiones_serializer.save()
            return JsonResponse({"data": regiones_serializer.data,
                                "status": "Created",
                                "message": "Se creo la region"}, status=status.HTTP_201_CREATED) 
        return JsonResponse(regiones_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_region(request, id):
    try: 
        region = Region.objects.get(codigo_region=id) 
    except Region.DoesNotExist: 
        return JsonResponse({'message': 'La region no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        region_serializer = RegionSerializer(region) 
        return JsonResponse(region_serializer.data) 
    elif request.method == 'PUT': 
        region_data = JSONParser().parse(request) 
        region_serializer = RegionSerializer(region, data=region_data) 
        if region_serializer.is_valid(): 
            region_serializer.save() 
            return JsonResponse(region_serializer.data) 
        return JsonResponse(region_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        region.delete() 
        return JsonResponse({'message': 'Region eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)
    
#Provincia
@csrf_exempt
@api_view(['GET','POST'])
def getprovincia(request):
    if request.method == 'GET':
        provincias = Provincia.objects.all()
        provincias_serializers = ProvinciaSerializer(provincias, many=True)
        return JsonResponse(provincias_serializers.data, safe=False)
    elif request.method == 'POST':
        provincias_data = JSONParser().parse(request)
        provincias_serializer = ProvinciaSerializer(data = provincias_data)
        if provincias_serializer.is_valid():
            provincias_serializer.save()
            return JsonResponse({"data": provincias_serializer.data,
                                "status": "Created",
                                "message": "Se creo la provincia"}, status=status.HTTP_201_CREATED) 
        return JsonResponse(provincias_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_provincia(request, id):
    try: 
        provincia = Provincia.objects.get(codigo_provincia=id) 
    except Provincia.DoesNotExist: 
        return JsonResponse({'message': 'La provincia no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        provincia_serializer = ProvinciaSerializer(provincia) 
        return JsonResponse(provincia_serializer.data) 
    elif request.method == 'PUT': 
        provincia_data = JSONParser().parse(request) 
        provincia_serializer = ProvinciaSerializer(provincia, data=provincia_data) 
        if provincia_serializer.is_valid(): 
            provincia_serializer.save() 
            return JsonResponse(provincia_serializer.data) 
        return JsonResponse(provincia_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        provincia.delete() 
        return JsonResponse({'message': 'Provincia eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)
    
#Comuna
@csrf_exempt
@api_view(['GET','POST'])
def getcomuna(request):
    if request.method == 'GET':
        comunas = Comuna.objects.all()
        comunas_serializers = ComunaSerializer(comunas, many=True)
        return JsonResponse(comunas_serializers.data, safe=False)
    elif request.method == 'POST':
        comunas_data = JSONParser().parse(request)
        comunas_serializer = ComunaSerializer(data = comunas_data)
        if comunas_serializer.is_valid():
            comunas_serializer.save()
            return JsonResponse({"data": comunas_serializer.data,
                                "status": "Created",
                                "message": "Se creo la provincia"}, status=status.HTTP_201_CREATED)
        return JsonResponse(comunas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_comuna(request, id):
    try: 
        comuna = Comuna.objects.get(codigo_comuna=id) 
    except Comuna.DoesNotExist: 
        return JsonResponse({'message': 'La comuna no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        comuna_serializer = ComunaSerializer(comuna) 
        return JsonResponse(comuna_serializer.data) 
    elif request.method == 'PUT': 
        comuna_data = JSONParser().parse(request) 
        comuna_serializer = ComunaSerializer(comuna, data=comuna_data) 
        if comuna_serializer.is_valid(): 
            comuna_serializer.save() 
            return JsonResponse(comuna_serializer.data) 
        return JsonResponse(comuna_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        comuna.delete() 
        return JsonResponse({'message': 'Comuna eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)
