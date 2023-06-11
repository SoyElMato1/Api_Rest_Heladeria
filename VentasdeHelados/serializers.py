from rest_framework import serializers, status
from .models import *
from django.contrib.auth.models import User
from django.http import Http404


class SaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sabor
        fields=['id_sabor','tipo_sabor']

class TamanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamano
        fields=['id_tamano','tipo_tamano']

class EstadoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Producto
        fields=['id_estado','tipo_estado']

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields=['codigo_cargo','nombre_cargo']

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields=['codigo_proveedor','nombre_pro','apellido_pro','direcion_pro']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['codigo_region','nombre_region']
        
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ['codigo_provincia', 'nombre_provincia','codigo_region']

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = ['codigo_comuna', 'nombre_comuna','codigo_provincia']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['codigo_sucursal','rut_sucursal','nombre_sucursal','direccion_sucursal','capacidad','cantidad_producto','codigo_producto','codigo_comuna']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['codigo_producto','nom_producto','precio','stock','id_sabor','id_tamano','id_estado']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['rutcliente', 'dv','nombre_cli','apellido_cli','telefono','razon_social','direccion']

class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = ['codigo_banco','nombre_banco']

class Metodo_pagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodo_pago
        fields = ['codigo_pago','tipo_pago', 'codigo_banco']

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ['rut_trabajador', 'dv','nombre_trabajador','apellido_trabajador','fecha_nac','codigo_cargo','codigo_sucursal']

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = ['numero_boleta','fecha_boleta','rut_trabajador', 'codigo_sucursal','total']

class Detalle_BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Boleta
        fields = ['id_det_bo','codigo_producto','precio','total','cantidad_producto','numero_boleta']

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class TranferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tranferencia
        fields = ['codigo_transferencia','codigo_cuenta','codigo_sucursal','email','monto']

class guiadedespachoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guiadedespacho
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['numero_factura','fecha_factura','rut_trabajador','codigo_sucursal','total']

class Detalle_FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Factura
        fields = ['id_detalle_factura','cantidad_producto','precio','codigo_producto','numero_factura','total']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        usuario = User.objects.create_user(**validated_data)
        return usuario

#Carrito
class UnProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["codigo_producto", "nom_producto", "precio"]

class ItemsSerializer(serializers.ModelSerializer):
    producto = UnProductoSerializer(many=False)
    precio = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = Items
        fields = ["id_carrito", "producto", "cantidad", "precio"]

    def total(self, item: Items):
        precio = item.cantidad * item.producto.precio
        return precio

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="precio_total")

    class Meta:
        model = Carrito
        fields = ["id_carrito", "items", "total", "id_usuario"]

    def precio_total(self, carrito: Carrito):
        items = carrito.items.all()
        total = sum([item.cantidad * item.producto.precio for item in items])
        return total

    def create(self, validated_data):
        carrito = Carrito.objects.create(**validated_data)
        return carrito

class AgregarCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["producto", "cantidad", "id_carrito"]

    def save(self):
        producto = self.validated_data["producto"]
        cantidad = self.validated_data["cantidad"]
        id_carrito = self.validated_data["id_carrito"]

        try:
            cartitem = Items.objects.get(id_carrito=id_carrito, producto=producto)
            cartitem.cantidad += cantidad
            cartitem.precio = cartitem.cantidad * cartitem.producto.precio
            cartitem.save()
            self.instance = cartitem
        except Items.DoesNotExist:
            producto2 = Producto.objects.get(codigo_producto=int(producto.codigo_producto))
            nuevoPrecio = producto2.precio* cantidad
            self.instance = Items.objects.create(
                producto=producto,
                id_carrito=id_carrito,
                cantidad=cantidad,
                precio=nuevoPrecio
            )
            return self.instance

class RestarCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["producto", "id_carrito"]
    def save(self):
        try:
            producto = self.validated_data["producto"]
            id_carrito = self.validated_data["id_carrito"] 
        except KeyError:
            raise Http404
        try:
            cartitem = Items.objects.get(producto=producto, id_carrito=id_carrito)
        except Items.DoesNotExist:
            raise Http404
        if cartitem.cantidad == 1:
            cartitem.delete()
            return self.instance

        cartitem.cantidad -= 1
        cartitem.precio = cartitem.cantidad * cartitem.producto.precio
        cartitem.save()

        return self.instance

#Bodega
class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = "__all__"

class StockBodegaSerializer(serializers.ModelSerializer):
    id_producto = serializers.StringRelatedField()
    class Meta:
        model = DetalleBodega
        fields = "__all__"
    
class CrearStockBodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleBodega
        fields = "__all__"
    def save(self, **kwargs):
        id_bodega = self.data["codigo_bodega"]
        stock = self.validated_data["cantidad_producto"]
        id_producto = self.validated_data["codigo_producto"]
        bodega = Bodega.objects.get(codigo_bodega=id_bodega)
        try:
            producto = DetalleBodega.objects.get(codigo_producto=id_producto, codigo_bodega=id_bodega)
            stock_sumado = producto.cantidad_producto + stock_sumado
            producto.cantidad_producto = stock_sumado
            stock_en_bodega = bodega.capacidad_ocupada
            nuevo_stock = stock + stock_en_bodega
            if bodega.capacidad > nuevo_stock:
                bodega.capacidad_ocupada = nuevo_stock
                bodega.save()
                producto.save()
                self.instance = producto
                return self.instance
            raise serializers.ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)
        except DetalleBodega.DoesNotExist:
            stock_bodega = bodega.capacidad_ocupada
            nuevo_stock = stock + stock_bodega
            if bodega.capacidad > nuevo_stock:
                bodega.capacidad_ocupada = nuevo_stock
                bodega.save()
                self.instance = DetalleBodega.objects.create(**self.validated_data)
                return self.instance
            raise serializers.ValidationError({"status": "Conflict", "message": "La capacidad ocupa de la bodega supera a la capacidad maxima de la bodega"}, status.HTTP_409_CONFLICT)

