from http.client import HTTPResponse
from django.http import JsonResponse
from rest_framework.response import Response
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

# ---------------------- METODO DE USUARIO ----------------------------------------------
@csrf_exempt
@api_view(['POST'])
def registro_usuario(request):
    if request.method == 'POST':
        usuario_data = JSONParser().parse(request)
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return JsonResponse({"data": usuario_serializer.data, "message": "Usuario creado" }, status=status.HTTP_201_CREATED)
        return JsonResponse(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------- METODO DE CARRITO ----------------------------------------------
class CarritoUsuarioView(generics.RetrieveAPIView):
    serializer_class = CarritoSerializer

    def get_object(self, id:int):
        try:
            carrito = Carrito.objects.get(id_usuario=id)
        except Carrito.DoesNotExist:
            raise Http404
        return carrito

    def get(self, request, id:int, format=None):
        carrito = self.get_object(id)
        serializer = self.get_serializer(carrito)
        return Response(serializer.data, status.HTTP_200_OK)

class CrearCarritoView(generics.CreateAPIView):

    serializer_class = CarritoSerializer
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class AgregarCarritoView(generics.CreateAPIView):
    serializer_class = AgregarCarritoSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Agregado al carrito con exito"}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class RestarCarritoItemView(generics.CreateAPIView):
    serializer_class = RestarCarritoSerializer
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Se resto el producto"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ListarCompra(generics.ListAPIView):
    def get(self, request, format=None):
        compra = Compra.objects.all()
        serializer = CompraSerializer(compra, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CrearCompra(generics.CreateAPIView):
    def get_object(self, id:int):
        try:
            producto = Producto.objects.get(codigo_producto= id)
        except Producto.DoesNotExist:
            return Http404
        return producto

    def post(self, request, format=None):
        serializer = CompraSerializer(data=request.data)
        if serializer.is_valid():
            id_carrito = request.data["id_carrito"]
            items_usuario = Items.objects.filter(id_carrito=id_carrito)
            for items in items_usuario:
                cantidad_item = items.cantidad
                producto_stock = items.producto.stock
                nuevo_stock = producto_stock - cantidad_item
                producto = self.get_object(items.producto.codigo_producto)
                producto.stock = nuevo_stock
                producto.save()
            serializer.save()
            limpiar_carrito(id_carrito)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

def limpiar_carrito(id_carrito:int):
    items_usuario = Items.objects.filter(id_carrito=id_carrito)
    for items in items_usuario:
        items.delete()

# ---------------------- METODO DE BODEGA ----------------------------------------------
@csrf_exempt
@api_view(['GET', 'POST'])
def listar_bodega(request):
    if request.method == 'GET':
        bodega = Bodega.objects.all()
        serializer = BodegaSerializer(bodega, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'POST':
        bodega_data = JSONParser().parse(request)
        bodega_serializer = BodegaSerializer(data=bodega_data)
        if bodega_serializer.is_valid():
            bodega_serializer.save()
            return JsonResponse({"data": bodega_serializer.data, "message": "Bodega creada" }, status=status.HTTP_201_CREATED)
        return JsonResponse(bodega_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def detalle_bodega(request, id:int):
    try:
        bodega = Bodega.objects.get(codigo_bodega=id)
    except Bodega.DoesNotExist:
        return JsonResponse({'message': 'Bodega no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        bodega_serializer = BodegaSerializer(bodega)
        return JsonResponse({"data": bodega_serializer.data, "message": "Bodega encontrada"}, status=status.HTTP_200_OK)
    
@csrf_exempt
@api_view(['POST'])
def CrearProdbodega(request):
    if request.method == 'POST':
        bodega_data = JSONParser().parse(request)
        bodega_serializer = CrearStockBodegaSerializer(data=bodega_data)
        if bodega_serializer.is_valid():
            bodega_serializer.save()
            return JsonResponse({"data": bodega_serializer.data, "message": "Detalle de Bodega creada" }, status=status.HTTP_201_CREATED)
        return JsonResponse(bodega_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class listar_prodbodega(generics.ListAPIView):
    serializer_class = StockBodegaSerializer
    permission_classes = [AllowAny]

    def get_object(self, id:int):
            bodega = Bodega.objects.get(codigo_bodega=id)
            return bodega
    
    def get(self, request, id:int, format=None):
        hola = DetalleBodega.objects.filter(codigo_bodega=id)
        serializer = self.serializer_class(hola, many=True)
        if not len(serializer.data):
            return Response({"message": "No hay productos en esta bodega"}, status.HTTP_404_NOT_FOUND)
        bodega = self.get_object(id)
        return Response({"status": "OK",
                        "Bodega": bodega.nombre_bodega,
                        "Capacidad": bodega.capacidad,
                        "Capacidad Ocupada": bodega.capacidad_ocupada,
                        "Productos": serializer.data
                        }, status.HTTP_200_OK)

class ListarStockBodegaFilterView(generics.ListAPIView):
    serializer_class = StockBodegaSerializer
    permission_classes = [AllowAny]

    def get(self, request, id:int, format=None):
        queryset = DetalleBodega.objects.filter(codigo_producto=id)
        serializer = self.serializer_class(queryset, many=True)
        if not len(serializer.data):
            return Response({"message": "No hay productos en esta bodega"}, status.HTTP_404_NOT_FOUND)
        stock_total = 0
        for producto in queryset:
            stock_total += producto.cantidad_producto
        return Response({"status": "OK",
                        "Stock Total": stock_total,
                        "Productos": serializer.data
                        }, status.HTTP_200_OK)