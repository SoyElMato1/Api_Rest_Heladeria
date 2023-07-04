from http.client import HTTPResponse
from django.http import JsonResponse
from rest_framework.response import Response
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from rest_framework import status, generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
import requests
from datetime import datetime

# ---------------------- METODO LOGIN ----------------------------------------------
@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        usuario_data = JSONParser().parse(request)
        
        usuario = authenticate(username=usuario_data['username'], password=usuario_data['password'])
        if usuario is None:
            return JsonResponse({"data": "null", "message": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        elif check_password(usuario_data['password'], usuario.password):
            token, created = Token.objects.get_or_create(user=usuario)
            if created:
                creado, carrito = Carrito.objects.get_or_create(id_usuario=usuario)
                return JsonResponse({"data": token.key, "message": "Usuario autenticado"}, status=status.HTTP_200_OK)

            token.delete()
            token = Token.objects.create(user=usuario)
            return JsonResponse({"data": token.key, "message": "Usuario autenticado"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"data": "null", "message": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
    

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

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    if request.method == 'GET':
        try:
            tokenUrl = request.GET.get('token')
            token = Token.objects.filter(key=tokenUrl).first()
            if token:
                usuario = token.user
                sessions = Session.objects.filter(expire_date__gte= datetime.now())
                if sessions.exists():
                    for session in sessions:
                        session_data = session.get_decoded()
                        if usuario.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                logout(request= request)
                mensaje_session = "Sesión cerrada"
                mensaje_token = "Token eliminado"

                message = {
                    'session': mensaje_session,
                    'token': mensaje_token
                }
                return Response({
                    'status': 'OK',
                    'message': 'Sesión cerrada correctamente',
                    'messages': message
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'ERROR',
                'message': 'No existe ningun usuario con esas credenciales'
            }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({"errirs": "Error al cerrar sesión"}, status=status.HTTP_409_CONFLICT)

# ---------------------- METODO DE CARRITO ----------------------------------------------
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def listar_carrito(request, id):
    if request.method == 'GET':
        try:
            carrito = Carrito.objects.get(id_usuario=id)
        except Carrito.DoesNotExist:
            return JsonResponse({"data": "null", "message": "No existe el carrito"}, status=status.HTTP_404_NOT_FOUND)

        carrito_serializer = CarritoSerializer(carrito)
        return JsonResponse({"data": carrito_serializer.data, "message": "Carrito encontrado"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def agregar_carrito(request):
    if request.method == 'POST':
        carrito_data = JSONParser().parse(request)
        carrito_serializer = AgregarCarritoSerializer(data=carrito_data)
        if carrito_serializer.is_valid():
            carrito_serializer.save()
            return JsonResponse({"data": carrito_serializer.data, "message": "Producto agregado al carrito"}, status=status.HTTP_201_CREATED)
        return JsonResponse(carrito_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def eliminar_carritoitem(request):
    if request.method == 'POST':
        carritoitem_data = JSONParser().parse(request)
        carritoitem_serializer = RestarCarritoSerializer(data=carritoitem_data)
        if carritoitem_serializer.is_valid():
            carritoitem_serializer.save()
            return JsonResponse({"data": carritoitem_serializer.data, "message": "Se elimino una unidad del producto seleccionado"}, status=status.HTTP_200_OK)
        return JsonResponse(carritoitem_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def ListarCompras(request):
    if request.method == 'GET':
        try:
            compras = Compra.objects.all()
        except Compra.DoesNotExist:
            return JsonResponse({"data": "null", "message": "No existen compras"}, status=status.HTTP_404_NOT_FOUND)

        compras_serializer = CompraSerializer(compras, many=True)
        return JsonResponse({"data": compras_serializer.data, "message": "Compras encontradas"}, status=status.HTTP_200_OK)

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
            return Response({"data" : serializer.data, "message": "Compra añadida"}, status.HTTP_201_CREATED)
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

# ---------------------- METODO DE Pedido ----------------------------------------------
@csrf_exempt
@api_view(['GET'])
def listarPedido(request):
    if request.method == 'GET':
        pedido = Pedido.objects.all()
        serializer = PedidoSerializer(pedido, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay pedidos registrados"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Bodeguero": serializer.data}, status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def listarpedidofactura(request, id:int):
    if request.method == 'GET':
        pedido = Pedido.objects.filter(numero_factura=id)
        serializer = PedidoSerializer(pedido, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay pedidos registrados con esta factura"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Bodeguero": serializer.data}, status.HTTP_200_OK)

class ActualizarEstadoPedido(generics.UpdateAPIView):
    serializer_class = ActualizarPedidoSerializer
    def get_object(self, id:int):
        try:
            pedido = Pedido.objects.get(id_pedido = id)
        except Pedido.DoesNotExist:
            return None
        return pedido
    def put(self, request, id:int, format=None):
        pedido = self.get_object(id)
        if pedido is None:
            return Response(
                {
                    "status": "Not Found", 
                    "message": "Pedido no Encontrado"
                    }, status=status.HTTP_404_NOT_FOUND)
        try:
            request.data["condicion"]
        except KeyError:
            return Response({"status": "Bad Request","errors": {
                "condicion": [
                    "Es te campo es requerido"
                ]
            }}, status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(pedido, data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "Bad Request", 
                    "errors": serializer.errors
                    }, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {
                "status": "Update", 
                "message": "La condicion del pedido a sido actualizado con exito"
                }, status.HTTP_200_OK)

# ---------------------- METODO DE Factura ----------------------------------------------
@csrf_exempt
@api_view(['GET'])
def listarFactura(request):
    if request.method == 'GET':
        factura = Factura.objects.all()
        serializer = FacturaSerializer(factura, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay facturas registradas"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Facturas": serializer.data}, status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def listarFacturaProveedor(request, id:int):
    if request.method == 'GET':
        factura = Factura.objects.filter(codigo_proveedor=id)
        serializer = FacturaSerializer(factura, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay facturas registradas con ese proveedor"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Facturas": serializer.data}, status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def CrearFactura(request):
    if request.method == 'POST':
        factura_data = JSONParser().parse(request)
        factura_serializer = CrearFacturaSerializer(data=factura_data)
        if factura_serializer.is_valid():
            factura_serializer.save()
            return JsonResponse({"data": factura_serializer.data, "message": "Factura creada" }, status=status.HTTP_201_CREATED)
        return JsonResponse(factura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------- METODO DE Guia ----------------------------------------------
@csrf_exempt
@api_view(['GET'])
def listarGuia(request):
    if request.method == 'GET':
        guia = Guiadedespacho.objects.all()
        serializer = GuiaSerializer(guia, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay guias registradas"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Guias": serializer.data}, status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def listarGuiaSucursal(request, id:int):
    if request.method == 'GET':
        guia = Guiadedespacho.objects.filter(codigo_sucursal=id)
        serializer = GuiaSerializer(guia, many=True)
        if not len(serializer.data):
            return Response({"messege": "No hay guias registradas con esa sucursal"}, status.HTTP_204_NO_CONTENT)
        return Response({"status": "ok","Guias": serializer.data}, status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def CrearGuia(request):
    if request.method == 'POST':
        guia_data = JSONParser().parse(request)
        guia_serializer = GuiadespachoSerializer(data=guia_data)
        if guia_serializer.is_valid():
            guia_serializer.save()
            return JsonResponse({"data": guia_serializer.data, "message": "Guia creada" }, status=status.HTTP_201_CREATED)
        return JsonResponse(guia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['PUT'])
def ActualizarEstadoGuia(request, id:int):
    try:
        guia = Guiadedespacho.objects.get(codigo_guia=id)
    except guia.DoesNotExist:
        return JsonResponse({'message': 'Guia no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        guia_data = JSONParser().parse(request)
        guia_serializer = ActualizarEstadoGuiaSerializer(guia, data=guia_data)
        if not guia_serializer.is_valid():
            return Response({
                "status": "Bad request",
                "errors": guia_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        guia_serializer.save()
        return Response({
            "status": "Actualizado",
            "data": guia_serializer.data,
            "message": "Guia actualizada con exito"
        }, status=status.HTTP_200_OK)
    
# ---------------------- METODO DE Transbank ----------------------------------------------
def header_request_transbank():
    headers = {
                "Authorization": "Token",
                "Tbk-Api-Key-Id": "597055555532",
                "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Referrer-Policy': 'origin-when-cross-origin',
                } 
    return headers

@csrf_exempt
@api_view(['POST'])
def crearTransbank(request):
    if request.method == 'POST':
        trans = JSONParser().parse(request)
        trans_serializer = CrearTransbank(data = trans)
        if trans_serializer.is_valid():
            url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
            headers = header_request_transbank()
            response = requests.post(url, json = trans.data, headers=headers)
            response_json = response.json()
            return Response({'message':'Transbank creado exitosamente', 'data': response_json }, status=status.HTTP_200_OK)
        return Response(trans.errors, status=status.HTTP_400_BAD_REQUEST)


class crearTransbank(generics.CreateAPIView):
    serializer_class = CrearTransbank
    def post(self, request):
        trans = self.get_serializer(data=request.data)
        if trans.is_valid():
            url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
            headers = header_request_transbank()
            response = requests.post(url, json = trans.data, headers=headers)
            response_json = response.json()
            return Response({'message':'Transbank creado exitosamente', 'data': response_json }, status=status.HTTP_200_OK)
        return Response(trans.errors, status=status.HTTP_400_BAD_REQUEST)
    
class confirmarTransbank(generics.CreateAPIView):
    def get(self,request, token:str):
        headers = header_request_transbank()
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        response = requests.put(url, headers=headers)
        response_json = response.json()
        return Response({'message':'Transbank confirmado exitosamente', 'data': response_json }, status=status.HTTP_200_OK)
    
class anularTransbank(generics.CreateAPIView):
    serializer_class = anularTransbank
    def post(self, request,token:str):
        trans = self.get_serializer(data=request.data)
        if trans.is_valid():
            url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
            headers = header_request_transbank()
            response = requests.post(url, json = trans.data, headers=headers)
            response_json = response.json()
            return Response({'message':'Transbank anulado exitosamente', 'data': response_json }, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
