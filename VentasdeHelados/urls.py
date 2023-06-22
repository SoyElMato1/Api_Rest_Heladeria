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
    path('getoferta/', getoferta, name='crear_productos'),
    path('getoferta/<id>', detalle_oferta, name='detalle_ofertas'),
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
    #Transferencia
    path('gettrans/', getTrans, name='transferencias'),
    path('det_dettrans/<id>', detalleTransferencia, name='detalle_transferencias'),
    #Usuario
    path('getusuario/', registro_usuario, name='usuarios'),
    path('getcliente/', getCliente, name='clientes'),
    #Carrito
    # path('create/', CrearCarritoView.as_view(), name='carrito'),
    path('user/<int:id>', listar_carrito, name='carrito_usuario'),
    path('add/', agregar_carrito, name='agregar_producto'),
    path('restar/', eliminar_carritoitem, name='restar_producto'),
    path('listarcompra/', ListarCompras, name='listar_compra'),
    path("comprar/created", CrearCompra.as_view(), name="crear_compra"),
    #Bodega
    path('getbodega/', listar_bodega, name='bodegas'),
    path('det_bodega/<id>', detalle_bodega, name='detalle_bodegas'),
    path('createbodega/', CrearProdbodega, name='crear_bodegas'),
    path('bodega/<int:id>', listar_prodbodega.as_view(), name='bodega_producto'),
    path('producto/<int:id>', ListarStockBodegaFilterView.as_view(), name='producto_bodega'),
    #Pedido
    path('getpedido/', listarPedido, name='pedidos'),
    path('pefa/<int:id>',listarpedidofactura, name='factura_pedido'),
    path('estped/<int:id>',ActualizarEstadoPedido.as_view(), name='guia_pedido'),
    #factura
    path('getfactura/', listarFactura, name='facturas'),
    path('proveedor/<int:id>', listarFacturaProveedor, name='detalle_facturas'),
    path('createfactura/', CrearFactura, name='crear_factura'),
    #Guia de despacho
    path('getguia/', listarGuia, name='guias'),
    path('createguia/', CrearGuia, name='crear_guia'),
    path('guiasucu/<int:id>', listarGuiaSucursal, name='detalle_guias'),
    #Login
    path('login/', login, name='login'),
]