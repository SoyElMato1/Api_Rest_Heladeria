from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.parsers import JSONParser
# imports soap
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel
from spyne.model.complex import Iterable

#SABOR
@csrf_exempt
@api_view(['GET', 'POST'])
def getsabor(request):
    """
    Lista de Sabores, o crea un nuevo sabor.
    """
    if request.method == 'GET':
        sabores = Sabor.objects.all()
        sabores_serializer = SaborSerializer(sabores, many=True)
        return JsonResponse(sabores_serializer.data, safe=False)
    elif request.method == 'POST':
        sabores_data = JSONParser().parse(request)
        sabores_serializer = SaborSerializer(data=sabores_data)
        if sabores_serializer.is_valid():
            sabores_serializer.save()
            return JsonResponse(sabores_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(sabores_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_sabor(request, id):
    """
    Recupera, actualiza o elimina un sabor.
    """
    try: 
        sabor = Sabor.objects.get(id_sabor=id) 
    except Sabor.DoesNotExist: 
        return JsonResponse({'message': 'El sabor no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        sabor_serializer = SaborSerializer(sabor) 
        return JsonResponse(sabor_serializer.data) 
    elif request.method == 'PUT': 
        sabor_data = JSONParser().parse(request) 
        sabor_serializer = SaborSerializer(sabor, data=sabor_data) 
        if sabor_serializer.is_valid(): 
            sabor_serializer.save() 
            return JsonResponse(sabor_serializer.data) 
        return JsonResponse(sabor_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        sabor.delete() 
        return JsonResponse({'message': 'Sabor eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#TAMANO
@csrf_exempt
@api_view(['GET', 'POST'])
def gettamano(request):
    if request.method == 'GET':
        tamanos = Tamano.objects.all()
        tamanos_serializer = TamanoSerializer(tamanos, many=True)
        return JsonResponse(tamanos_serializer.data, safe=False)
    elif request.method == 'POST':
        tamanos_data = JSONParser().parse(request)
        tamanos_serializer = TamanoSerializer(data=tamanos_data)
        if tamanos_serializer.is_valid():
            tamanos_serializer.save()
            return JsonResponse(tamanos_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tamanos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_tamano(request, id):
    """
    Recupera, actualiza o elimina un tamano.
    """
    try: 
        tamano = Tamano.objects.get(id_tamano=id) 
    except Tamano.DoesNotExist: 
        return JsonResponse({'message': 'El tamano no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        tamano_serializer = TamanoSerializer(tamano) 
        return JsonResponse(tamano_serializer.data) 
    elif request.method == 'PUT': 
        tamano_data = JSONParser().parse(request) 
        tamano_serializer = TamanoSerializer(tamano, data=tamano_data) 
        if tamano_serializer.is_valid(): 
            tamano_serializer.save() 
            return JsonResponse(tamano_serializer.data) 
        return JsonResponse(tamano_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        tamano.delete() 
        return JsonResponse({'message': 'Tamano eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Estado de Producto
@csrf_exempt
@api_view(['GET', 'POST'])
def getestadoproducto(request):
    if request.method == 'GET':
        estados = Estado_Producto.objects.all()
        estados_serializer = EstadoProductoSerializer(estados, many=True)
        return JsonResponse(estados_serializer.data, safe=False)
    elif request.method == 'POST':
        estados_data = JSONParser().parse(request)
        estados_serializer = EstadoProductoSerializer(data=estados_data)
        if estados_serializer.is_valid():
            estados_serializer.save()
            return JsonResponse(estados_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(estados_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_estadoproducto(request, id):
    """
    Recupera, actualiza o elimina un estado de producto.
    """
    try: 
        estado = Estado_Producto.objects.get(id_estado=id) 
    except Estado_Producto.DoesNotExist: 
        return JsonResponse({'message': 'El estado de producto no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        estado_serializer = EstadoProductoSerializer(estado) 
        return JsonResponse(estado_serializer.data) 
    elif request.method == 'PUT': 
        estado_data = JSONParser().parse(request) 
        estado_serializer = EstadoProductoSerializer(estado, data=estado_data) 
        if estado_serializer.is_valid(): 
            estado_serializer.save() 
            return JsonResponse(estado_serializer.data) 
        return JsonResponse(estado_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        estado.delete() 
        return JsonResponse({'message': 'Estado de producto eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Producto
@csrf_exempt
@api_view(['GET', 'POST'])
def getProducto(request):
    if request.method == 'GET':
        producto = Producto.objects.all()
        producto_serializer = ProductoSerializer(producto, many=True)
        return JsonResponse(producto_serializer.data, safe=False)
    elif request.method == 'POST':
        producto_data = JSONParser().parse(request)
        producto_serializer = ProductoSerializer(data=producto_data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return JsonResponse(producto_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_producto(request, id):
    try:
        producto = Producto.objects.get(codigo_producto=id)
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'El producto no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        producto_serializer = ProductoSerializer(producto)
        return JsonResponse(producto_serializer.data)
    elif request.method == 'PUT':
        producto_data = JSONParser().parse(request)
        producto_serializer = ProductoSerializer(producto, data=producto_data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return JsonResponse(producto_serializer.data)
        return JsonResponse(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        producto.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Proveedor
@csrf_exempt
@api_view(['GET', 'POST'])
def getproveedor(request):
    if request.method == 'GET':
        proveedores = Proveedor.objects.all()
        proveedores_serializer = ProveedorSerializer(proveedores, many=True)
        return JsonResponse(proveedores_serializer.data, safe=False)
    elif request.method == 'POST':
        proveedores_data = JSONParser().parse(request)
        proveedores_serializer = ProveedorSerializer(data=proveedores_data)
        if proveedores_serializer.is_valid():
            proveedores_serializer.save()
            return JsonResponse(proveedores_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(proveedores_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_proveedor(request, id):
    """
    Recupera, actualiza o elimina un proveedor.
    """
    try: 
        proveedor = Proveedor.objects.get(codigo_proveedor=id) 
    except Proveedor.DoesNotExist: 
        return JsonResponse({'message': 'El proveedor no existe'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        proveedor_serializer = ProveedorSerializer(proveedor) 
        return JsonResponse(proveedor_serializer.data) 
    elif request.method == 'PUT': 
        proveedor_data = JSONParser().parse(request) 
        proveedor_serializer = ProveedorSerializer(proveedor, data=proveedor_data) 
        if proveedor_serializer.is_valid(): 
            proveedor_serializer.save() 
            return JsonResponse(proveedor_serializer.data) 
        return JsonResponse(proveedor_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        proveedor.delete() 
        return JsonResponse({'message': 'Proveedor eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Cliente
@csrf_exempt
@api_view(['GET', 'POST'])
def getCliente(request):
    if request.method == 'GET':
        cliente = Cliente.objects.all()
        cliente_serializer = ClienteSerializer(cliente, many=True)
        return JsonResponse(cliente_serializer.data, safe=False)
    elif request.method == 'POST':
        cliente_data = JSONParser().parse(request)
        cliente_serializer = ClienteSerializer(data=cliente_data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return JsonResponse(cliente_serializer, status=status.HTTP_201_CREATED)
        return JsonResponse(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_cliente(request, id):
    try:
        cliente = Cliente.objects.get(rutcliente=id)
    except Cliente.DoesNotExist:
        return JsonResponse({'message': 'El cliente no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        cliente_serializer = ClienteSerializer(cliente)
        return JsonResponse(cliente_serializer.data)
    elif request.method == 'PUT':
        cliente_data = JSONParser().parse(request)
        cliente_serializer = ClienteSerializer(cliente, data=cliente_data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return JsonResponse(cliente_serializer.data)
        return JsonResponse(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Banco
@csrf_exempt
@api_view(['GET', 'POST'])
def getBanco(request):
    if request.method == 'GET':
        banco = Banco.objects.all()
        banco_serializer = BancoSerializer(banco, many=True)
        return JsonResponse(banco_serializer.data, safe=False)
    elif request.method == 'POST':
        banco_data = JSONParser().parse(request)
        banco_serializer = BancoSerializer(data=banco_data)
        if banco_serializer.is_valid():
            banco_serializer.save()
            return JsonResponse(banco_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(banco_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_banco(request, id):
    try:
        banco = Banco.objects.get(id_banco=id)
    except Banco.DoesNotExist:
        return JsonResponse({'message': 'El banco no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        banco_serializer = BancoSerializer(banco)
        return JsonResponse(banco_serializer.data)
    elif request.method == 'PUT':
        banco_data = JSONParser().parse(request)
        banco_serializer = BancoSerializer(banco, data=banco_data)
        if banco_serializer.is_valid():
            banco_serializer.save()
            return JsonResponse(banco_serializer.data)
        return JsonResponse(banco_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        banco.delete()
        return JsonResponse({'message': 'Banco eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Metodo_pago
@csrf_exempt
@api_view(['GET', 'POST'])
def getMetodo_pago(request):
    if request.method == 'GET':
        metodo_pago = Metodo_pago.objects.all()
        metodo_pago_serializer = Metodo_pagoSerializer(metodo_pago, many=True)
        return JsonResponse(metodo_pago_serializer.data, safe=False)
    elif request.method == 'POST':
        metodo_pago_data = JSONParser().parse(request)
        metodo_pago_serializer = Metodo_pagoSerializer(data=metodo_pago_data)
        if metodo_pago_serializer.is_valid():
            metodo_pago_serializer.save()
            return JsonResponse(metodo_pago_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(metodo_pago_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_metodo(request, id):
    try:
        metodo_pago = Metodo_pago.objects.get(id_metodo=id)
    except Metodo_pago.DoesNotExist:
        return JsonResponse({'message': 'El metodo de pago no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        metodo_pago_serializer = Metodo_pagoSerializer(metodo_pago)
        return JsonResponse(metodo_pago_serializer.data)
    elif request.method == 'PUT':
        metodo_pago_data = JSONParser().parse(request)
        metodo_pago_serializer = Metodo_pagoSerializer(metodo_pago, data=metodo_pago_data)
        if metodo_pago_serializer.is_valid():
            metodo_pago_serializer.save()
            return JsonResponse(metodo_pago_serializer.data)
        return JsonResponse(metodo_pago_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        metodo_pago.delete()
        return JsonResponse({'message': 'Metodo de pago eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Boleta
@csrf_exempt
@api_view(['GET', 'POST'])
def getBoleta(request):
    if request.method == 'GET':
        boleta = Boleta.objects.all()
        boleta_serializer = BoletaSerializer(boleta, many=True)
        return JsonResponse(boleta_serializer.data, safe=False)
    elif request.method == 'POST':
        boleta_data = JSONParser().parse(request)
        boleta_serializer = BoletaSerializer(data=boleta_data)
        if boleta_serializer.is_valid():
            boleta_serializer.save()
            return JsonResponse(boleta_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(boleta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_boleta(request, id):
    try:
        boleta = Boleta.objects.get(numero_boleta=id)
    except Boleta.DoesNotExist:
        return JsonResponse({'message': 'La boleta no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        boleta_serializer = BoletaSerializer(boleta)
        return JsonResponse(boleta_serializer.data)
    elif request.method == 'PUT':
        boleta_data = JSONParser().parse(request)
        boleta_serializer = BoletaSerializer(boleta, data=boleta_data)
        if boleta_serializer.is_valid():
            boleta_serializer.save()
            return JsonResponse(boleta_serializer.data)
        return JsonResponse(boleta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        boleta.delete()
        return JsonResponse({'message': 'Boleta eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)
    
#Detalle_Boleta
@csrf_exempt
@api_view(['GET', 'POST'])
def getDetalle_Boleta(request):
    if request.method == 'GET':
        detalle_boleta = Detalle_Boleta.objects.all()
        detalle_boleta_serializer = Detalle_BoletaSerializer(detalle_boleta, many=True)
        return JsonResponse(detalle_boleta_serializer.data, safe=False)
    elif request.method == 'POST':
        detalle_boleta_data = JSONParser().parse(request)
        detalle_boleta_serializer = Detalle_BoletaSerializer(data=detalle_boleta_data)
        if detalle_boleta_serializer.is_valid():
            detalle_boleta_serializer.save()
            return JsonResponse(detalle_boleta_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(detalle_boleta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_det_boleta(request, id):
    try:
        detalle_boleta = Detalle_Boleta.objects.get(id_det_bo=id)
    except Detalle_Boleta.DoesNotExist:
        return JsonResponse({'message': 'El detalle de la boleta no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        detalle_boleta_serializer = Detalle_BoletaSerializer(detalle_boleta)
        return JsonResponse(detalle_boleta_serializer.data)
    elif request.method == 'PUT':
        detalle_boleta_data = JSONParser().parse(request)
        detalle_boleta_serializer = Detalle_BoletaSerializer(detalle_boleta, data=detalle_boleta_data)
        if detalle_boleta_serializer.is_valid():
            detalle_boleta_serializer.save()
            return JsonResponse(detalle_boleta_serializer.data)
        return JsonResponse(detalle_boleta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        detalle_boleta.delete()
        return JsonResponse({'message': 'Detalle de la boleta eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Compra
@csrf_exempt
@api_view(['GET', 'POST'])
def getCompra(request):
    if request.method == 'GET':
        compre = Compra.objects.all()
        compre_serializer = CompraSerializer(compre, many=True)
        return JsonResponse(compre_serializer.data, safe=False)
    elif request.method == 'POST':
        compre_data = JSONParser().parse(request)
        compre_serializer = CompraSerializer(data=compre_data)
        if compre_serializer.is_valid():
            compre_serializer.save()
            return JsonResponse(compre_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(compre_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_compra(request, id):
    try:
        compre = Compra.objects.get(id_compra=id)
    except Compra.DoesNotExist:
        return JsonResponse({'message': 'La compra no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        compre_serializer = CompraSerializer(compre)
        return JsonResponse(compre_serializer.data)
    elif request.method == 'PUT':
        compre_data = JSONParser().parse(request)
        compre_serializer = CompraSerializer(compre, data=compre_data)
        if compre_serializer.is_valid():
            compre_serializer.save()
            return JsonResponse(compre_serializer.data)
        return JsonResponse(compre_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        compre.delete()
        return JsonResponse({'message': 'Compra eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Transferencia
@csrf_exempt
@api_view(['GET', 'POST'])
def getTrans(request):
    if request.method == 'GET':
        transferencia = Tranferencia.objects.all()
        transferencia_serializer = TranferenciaSerializer(transferencia, many=True)
        return JsonResponse(transferencia_serializer.data, safe=False)
    elif request.method == 'POST':
        transferencia_data = JSONParser().parse(request)
        transferencia_serializer = TranferenciaSerializer(data=transferencia_data)
        if transferencia_serializer.is_valid():
            transferencia_serializer.save()
            return JsonResponse(transferencia_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(transferencia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalleTransferencia(request, id):
    try:
        transferencia = Tranferencia.objects.get(codigo_transferencia=id)
    except Tranferencia.DoesNotExist:
        return JsonResponse({'message': 'La transferencia no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        transferencia_serializer = TranferenciaSerializer(transferencia)
        return JsonResponse(transferencia_serializer.data)
    elif request.method == 'PUT':
        transferencia_data = JSONParser().parse(request)
        transferencia_serializer = TranferenciaSerializer(transferencia, data=transferencia_data)
        if transferencia_serializer.is_valid():
            transferencia_serializer.save()
            return JsonResponse(transferencia_serializer.data)
        return JsonResponse(transferencia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        transferencia.delete()
        return JsonResponse({'message': 'Transferencia eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Factura
@csrf_exempt
@api_view(['GET', 'POST'])
def getFactura(request):
    if request.method == 'GET':
        factura = Factura.objects.all()
        factura_serializer = FacturaSerializer(factura, many=True)
        return JsonResponse(factura_serializer.data, safe=False)
    elif request.method == 'POST':
        factura_data = JSONParser().parse(request)
        factura_serializer = FacturaSerializer(data=factura_data)
        if factura_serializer.is_valid():
            factura_serializer.save()
            return JsonResponse(factura_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(factura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_factura(request, id):
    try:
        factura = Factura.objects.get(numero_factura=id)
    except Factura.DoesNotExist:
        return JsonResponse({'message': 'La factura no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        factura_serializer = FacturaSerializer(factura)
        return JsonResponse(factura_serializer.data)
    elif request.method == 'PUT':
        factura_data = JSONParser().parse(request)
        factura_serializer = FacturaSerializer(factura, data=factura_data)
        if factura_serializer.is_valid():
            factura_serializer.save()
            return JsonResponse(factura_serializer.data)
        return JsonResponse(factura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        factura.delete()
        return JsonResponse({'message': 'Factura eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Detalle Factura
@csrf_exempt
@api_view(['GET', 'POST'])
def getDetalleFactura(request):
    if request.method == 'GET':
        detalle = Detalle_Factura.objects.all()
        detalle_serializer = Detalle_FacturaSerializer(detalle, many=True)
        return JsonResponse(detalle_serializer.data, safe=False)
    elif request.method == 'POST':
        detalle_data = JSONParser().parse(request)
        detalle_serializer = Detalle_FacturaSerializer(data=detalle_data)
        if detalle_serializer.is_valid():
            detalle_serializer.save()
            return JsonResponse(detalle_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(detalle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_detFactura(request, id):
    try:
        detalle = Detalle_Factura.objects.get(id_detalle_factura=id)
    except Detalle_Factura.DoesNotExist:
        return JsonResponse({'message': 'El detalle no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        detalle_serializer = Detalle_FacturaSerializer(detalle)
        return JsonResponse(detalle_serializer.data)
    elif request.method == 'PUT':
        detalle_data = JSONParser().parse(request)
        detalle_serializer = Detalle_FacturaSerializer(detalle, data=detalle_data)
        if detalle_serializer.is_valid():
            detalle_serializer.save()
            return JsonResponse(detalle_serializer.data)
        return JsonResponse(detalle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        detalle.delete()
        return JsonResponse({'message': 'Detalle eliminado correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Guia de despacho
@csrf_exempt
@api_view(['GET', 'POST'])
def getGuiaDespacho(request):
    if request.method == 'GET':
        guia = Guiadedespacho.objects.all()
        guia_serializer = guiadedespachoSerializer(guia, many=True)
        return JsonResponse(guia_serializer.data, safe=False)
    elif request.method == 'POST':
        guia_data = JSONParser().parse(request)
        guia_serializer = guiadedespachoSerializer(data=guia_data)
        if guia_serializer.is_valid():
            guia_serializer.save()
            return JsonResponse(guia_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(guia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_guiadespacho(request, id):
    try:
        guia = Guiadedespacho.objects.get(codigo_guia=id)
    except Guiadedespacho.DoesNotExist:
        return JsonResponse({'message': 'La guia no existe'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        guia_serializer = guiadedespachoSerializer(guia)
        return JsonResponse(guia_serializer.data)
    elif request.method == 'PUT':
        guia_data = JSONParser().parse(request)
        guia_serializer = guiadedespachoSerializer(guia, data=guia_data)
        if guia_serializer.is_valid():
            guia_serializer.save()
            return JsonResponse(guia_serializer.data)
        return JsonResponse(guia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guia.delete()
        return JsonResponse({'message': 'Guia eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#Soap Proveedor
class ProveedorList(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = Proveedor

class ProveedorService(ServiceBase):
    @rpc(Integer(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        _returns=Unicode)
    
    def create_proveedor(ctx, codigo_proveedor, nombre_pro, apellido_pro, direcion_pro):
        registro = Proveedor()
        registro.codigo_proveedor = codigo_proveedor
        registro.nombre_pro = nombre_pro
        registro.apellido_pro = apellido_pro
        registro.direcion_pro = direcion_pro
        registro.save()
        return "Proveedor creado : " + str(codigo_proveedor)
    
    @rpc(Integer(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        Unicode(nillable=False),
        _returns=Unicode)
    
    def update_proveedor(ctx, codigo_proveedor, nombre_pro, apellido_pro, direcion_pro):
        registro = Proveedor.objects.get(pk=codigo_proveedor)
        registro.nombre_pro = nombre_pro
        registro.apellido_pro = apellido_pro
        registro.direcion_pro = direcion_pro
        registro.save()
        return "Proveedor actualizado : " + str(codigo_proveedor)
    
    @rpc(Integer(nillable=False),_returns=ProveedorList)
    def get_proveedor(ctx, codigo_proveedor):
        regitro = Proveedor.objects.get(pk=codigo_proveedor)
        return regitro
    
    @rpc(_returns=Iterable(ProveedorList))
    def get_all_proveedor(ctx):
        return Proveedor.objects.all()
    
    @rpc(Integer(nillable=False),_returns=Unicode)
    def delete_proveedor(ctx, codigo_proveedor):
        registro = Proveedor.objects.get(pk=codigo_proveedor)
        registro.delete()
        return "Proveedor eliminado  : " + str(codigo_proveedor)
    
soap_app_proveedor = Application([ProveedorService],
    tns='django.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
    )

django_soap_proveedor = DjangoApplication(soap_app_proveedor)
crud_proveedor = csrf_exempt(django_soap_proveedor)