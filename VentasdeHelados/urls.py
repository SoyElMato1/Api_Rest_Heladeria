from django.urls import path
from .views import *
from .viewspais import *
from .viewssucursal import *
from .viewsnegocio import *

urlpatterns = [
    #Sabor
    path('getsabor/', getsabor, name='sabores'),
    path('det_sabor/<id>', detalle_sabor, name='detalle_sabores'),
    #Tamaño
    path('gettamano/', gettamano, name='tamaños'),
    path('det_tamano/<id>', detalle_tamano, name='detalle_tamano'),
    #Estado Producto
    path('getestado/', getestadoproducto, name='estados'),
    path('det_estado/<id>', detalle_estadoproducto, name='detalle_estados'),
    #Cargo
    path('getcargo/', getcargo, name='cargos'),
    path('det_cargo/<id>', detalle_cargo, name='detalle_cargos'),
    #Proveedor
    path('getproveedor/', getproveedor, name='proveedores'),
    path('det_prove/<id>', detalle_proveedor, name='detalle_proveedores'),
    path('soap/', crud_proveedor, name='crud_proveedor'),
    #Region
    path('getregion/', getregion, name='regiones'),
    path('det_region/<id>', detalle_region, name='detalle_regiones'),
    #Provincia
    path('getprovincia/', getprovincia, name='provincias'),
    path('det_provincia/<id>', detalle_provincia, name='detalle_provincias'),
    #Comuna
    path('getcomuna/', getcomuna, name='comunas'),
    path('det_comuna/<id>', detalle_comuna, name='detalle_comunas'),
    #Sucursal
    path('getsucursal/', getsucursal, name='sucursales'),
    path('det_sucursal/<id>', detalle_sucursal, name='detalle_sucursales'),
    #Producto
    path('getproducto/', getProducto, name='productos'),
    path('det_producto/<id>', detalle_producto, name='detalle_productos'),
    #Cliente
    path('getcliente/', getCliente, name='clientes'),
    path('det_cliente/<id>', detalle_cliente, name='detalle_clientes'),
    #Banco
    path('getbanco/', getBanco, name='bancos'),
    path('det_banco/<id>', detalle_banco, name='detalle_bancos'),
    #Metodo de pago
    path('getmetodo/', getMetodo_pago, name='metodos'),
    path('det_metodo/<id>', detalle_metodo, name='detalle_metodos'),
    #Trabajador
    path('gettrabajador/', getTrabajador, name='trabajadores'),
    path('det_trabajador/<id>', detalle_trabajador, name='detalle_trabajadores'),
    #Boleta
    path('getboleta/', getBoleta, name='boletas'),
    path('det_boleta/<id>', detalle_boleta, name='detalle_boletas'),
    #Detalle Boleta
    path('getdetboleta/', getDetalle_Boleta, name='detboletas'),
    path('det_detboleta/<id>', detalle_det_boleta, name='detalle_detboletas'),
    #Compra
    path('getcompra/', getCompra, name='compras'),
    path('det_compra/<id>', detalle_compra, name='detalle_compras'),
    #Transferencia
    path('gettrans/', getTrans, name='transferencias'),
    path('det_dettrans/<id>', detalleTransferencia, name='detalle_transferencias'),
    #Bodega
    path('getbodega/', listar_bodega, name='bodegas'),
    path('det_bodega/<id>', detalle_bodega, name='detalle_bodegas'),
    path('createbodega/', CrearProdbodega, name='crear_bodegas'),
    path('bodega/<int:id>', listar_prodbodega.as_view(), name='bodega_producto'),
    path('producto/<int:id>', ListarStockBodegaFilterView.as_view(), name='producto_bodega'),
    #Factura
    path('getfactura/', getFactura, name='facturas'),
    path('det_factura/<id>', detalle_factura, name='detalle_facturas'),
    #Detalle Factura
    path('getdetfactura/', getDetalleFactura, name='detfacturas'),
    path('det_detfactura/<id>', detalle_detFactura, name='detalle_detfacturas'),
    #Guia Despacho
    path('getguiadespacho/', getGuiaDespacho, name='guias'),
    path('det_guiadespacho/<id>', detalle_guiadespacho, name='detalle_guias'),
    #Usuario
    path('getusuario/', registro_usuario, name='usuarios'),
    #Carrito
    path('create/', CrearCarritoView.as_view(), name='carrito'),
    path('user/<int:id>', CarritoUsuarioView.as_view(), name='carrito_usuario'),
    path('add/', AgregarCarritoView.as_view(), name='agregar_producto'),
    path('restar/', RestarCarritoItemView.as_view(), name='restar_producto'),
    path('listarcompra/', ListarCompra.as_view(), name='listar_compra'),
    path("comprar/created", CrearCompra.as_view(), name="crear_compra"),

]