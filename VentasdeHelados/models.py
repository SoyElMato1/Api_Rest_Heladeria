from typing import Tuple
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, correo_user, nom_user, ap_user, password, is_staff, is_superuser, rol, **extra_fields):
        user = self.model(
            username = username,
            correo_user = self.normalize_email(correo_user),
            nom_user = nom_user,
            ap_user = ap_user,
            is_staff = is_staff,
            is_superuser = is_superuser,
            rol = rol,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return user
    def create_superuser(self, username, correo_user, nom_user, ap_user, password=None, **extra_fields):
        return self._create_user(username, correo_user, nom_user, ap_user, password, True, True, "admin", **extra_fields)
    
    def create_usercli(self, username, correo_user, nom_user, ap_user, password=None, **extra_fields):
        return self._create_user(username, correo_user, nom_user, ap_user, password, False, False, "cliente", **extra_fields)
    
CHOICES_ROLES = [
    ('admin', 'admin'),
    ('cliente', 'cliente'),
]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    correo_user = models.EmailField("Correo",max_length=100, unique=True)
    nom_user = models.CharField("Nombre", max_length=20, blank=True, null=True, default="(Sin Nombre)")
    ap_user = models.CharField("Apellido", max_length=20, blank=True, null=True, default="(Sin Apellido)")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    rol = models.CharField(max_length=30, choices=CHOICES_ROLES)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo_user', 'nom_user', 'ap_user']

    def __str__(self) -> str:
        return self.username
        
    def natural_key(self) -> Tuple[str]:
        return (self.username,)

class Cliente(models.Model):
    rutcliente =  models.BigIntegerField(primary_key= True)
    dv = models.CharField(max_length=1)
    nombre_cli = models.CharField(max_length=25)
    apellido_cli = models.CharField(max_length=25)
    telefono = models.CharField(max_length=25)
    direccion = models.CharField(max_length=40)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Sabor (models.Model):
    id_sabor = models.BigIntegerField(primary_key=True)
    tipo_sabor = models.CharField(max_length=30)

class Tamano (models.Model):
    id_tamano = models.BigIntegerField(primary_key=True)
    tipo_tamano = models.CharField(max_length=30)

class Estado_Producto (models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    tipo_estado = models.CharField(max_length=30)

class Producto (models.Model):
    codigo_producto = models.BigIntegerField(primary_key=True)
    nom_producto =models.CharField(max_length=25)
    precio  = models.IntegerField()
    stock = models.IntegerField()
    id_sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE)
    id_tamano = models.ForeignKey(Tamano, on_delete=models.CASCADE)
    id_estado = models.ForeignKey(Estado_Producto, on_delete=models.CASCADE)

class Proveedor (models.Model):
    codigo_proveedor = models.BigIntegerField(primary_key=True)
    nombre_pro = models.CharField(max_length=25)
    apellido_pro = models.CharField(max_length=25)
    direcion_pro = models.CharField(max_length=25)

class Banco (models.Model):
    codigo_banco = models.BigIntegerField(primary_key= True)
    nombre_banco = models.CharField(max_length=25)

class Metodo_pago (models.Model):
    codigo_pago = models.BigIntegerField(primary_key= True)
    tipo_pago = models.CharField(max_length=25)
    codigo_banco = models.ForeignKey( Banco, on_delete=models.CASCADE)

class Region (models.Model):
    codigo_region = models.BigIntegerField(primary_key= True)
    nombre_region = models.CharField(max_length=100)

class Provincia (models.Model):
    codigo_provincia = models.BigIntegerField(primary_key= True)
    nombre_provincia = models.CharField(max_length=25)
    codigo_region = models.ForeignKey( Region, on_delete=models.CASCADE)

class Comuna (models.Model):
    codigo_comuna = models.BigIntegerField(primary_key= True)
    nombre_comuna = models.CharField(max_length=25)
    codigo_provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

class Cargo (models.Model):
    codigo_cargo = models.BigIntegerField(primary_key= True)
    nombre_cargo = models.CharField(max_length=25)

class Sucursal (models.Model):
    codigo_sucursal = models.BigIntegerField(primary_key= True)
    rut_sucursal = models.CharField(max_length=25)
    nombre_sucursal = models.CharField(max_length=25)
    direccion_sucursal = models.CharField(max_length=25)
    capacidad = models.IntegerField(default=800)
    cantidad_producto = models.IntegerField()
    codigo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    codigo_comuna = models.ForeignKey(Comuna, null=True, on_delete=models.CASCADE)

class Trabajador (models.Model):
    rut_trabajador =models.BigIntegerField(primary_key= True)
    dv = models.CharField(max_length=1)
    nombre_trabajador = models.CharField(max_length=25)
    apellido_trabajador = models.CharField(max_length=25)
    fecha_nac = models.CharField(max_length=25)
    codigo_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    codigo_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

class Boleta (models.Model):
    numero_boleta = models.BigIntegerField(primary_key= True)
    rut_trabajador = models.ForeignKey( Trabajador, on_delete=models.CASCADE)
    codigo_sucursal = models.ForeignKey( Sucursal, on_delete=models.CASCADE)
    fecha_boleta = models.CharField(max_length=25)
    total = models.IntegerField()

class Detalle_Boleta(models.Model):
    id_det_bo = models.BigIntegerField(primary_key= True)
    codigo_producto = models.ForeignKey( Producto, on_delete=models.CASCADE)
    precio = models.IntegerField()
    total = models.IntegerField()
    cantidad_producto = models.IntegerField()
    numero_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)

class Bodega (models.Model):
    codigo_bodega = models.BigIntegerField(primary_key= True)
    nombre_bodega = models.CharField(max_length=25, unique=True)
    direccion_bo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    capacidad_ocupada = models.PositiveIntegerField()
    codigo_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

class DetalleBodega (models.Model):
    id_det_bo = models.BigIntegerField(primary_key= True)
    codigo_producto = models.ForeignKey( Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    codigo_bodega = models.ForeignKey( Bodega, on_delete=models.CASCADE)

class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True)
    create = models.DateTimeField(auto_now_add=True)
    total = models.PositiveBigIntegerField(default=0)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Items(models.Model):
    id_items = models.BigAutoField(primary_key=True)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="productos")
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveBigIntegerField()

class Compra (models.Model):
    id_compra = models.BigIntegerField(primary_key= True)
    fecha_compra = models.CharField(max_length=25)
    total = models.IntegerField()
    estado = models.BooleanField(default=True)
    productos = models.JSONField()
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

class Tranferencia (models.Model):
    codigo_transferencia = models.BigIntegerField(primary_key= True)
    codigo_cuenta = models.IntegerField()
    codigo_sucursal = models.ForeignKey( Sucursal, on_delete=models.CASCADE)
    email = models.CharField(max_length=40)
    monto = models.IntegerField()

CHOICES_CONDICION = [
    ("cancelado", "cancelado"),
    ("en retraso", "en retraso"),
    ("en preparacion", "en preparacion"),
    ("en reparto", "en reparto"),
    ("en camino", "en camino"),
    ("entregado", "entregado")
]

CHOICES_TIPORETIRO = [
    ("retiro en tienda", "retiro en tienda"),
    ("envio a domicilio", "envio a domicilio")
]

class Guiadedespacho (models.Model):
    codigo_guia = models.BigAutoField(primary_key= True)
    fecha_guia = models.DateField(auto_now_add=True)
    condicion = models.CharField(max_length=25, choices=CHOICES_CONDICION, default="en preparacion")
    tipo_retiro = models.CharField(max_length=25, choices=CHOICES_TIPORETIRO)
    direccion = models.CharField(max_length=200)
    codigo_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    rut_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

class Detalle_Guia(models.Model):
    id_det_guia = models.BigAutoField(primary_key= True)
    codigo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.PositiveIntegerField()
    codigo_guia = models.ForeignKey(Guiadedespacho, on_delete=models.CASCADE, related_name="productos")

class Factura (models.Model):
    numero_factura = models.BigAutoField(primary_key= True)
    fecha_factura = models.DateField(auto_now_add=True)
    productos = models.JSONField()
    total = models.PositiveIntegerField()
    total_productos = models.PositiveIntegerField()
    rut_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    codigo_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

CHOICES_PEDIDO = [
    ("cancelado", "cancelado"),
    ("en retraso", "en retraso"),
    ("en preparacion", "en preparacion"),
    ("en reparto", "en reparto"),
    ("en camino", "en camino"),
    ("entregado", "entregado")
]

class Pedido (models.Model):
    id_pedido = models.BigAutoField(primary_key= True)
    fecha_pedido = models.DateField(auto_now_add=True)
    condicion = models.CharField(max_length=25, choices=CHOICES_PEDIDO, default="en preparacion")
    direccion_despacho = models.CharField(max_length=200)
    rut_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    numero_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)