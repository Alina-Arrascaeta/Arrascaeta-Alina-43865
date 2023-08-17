from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name="inicio" ),

    path('empleados/', EmpleadoList.as_view(), name="empleados"),
    path('create_empleado/', EmpleadoCreate.as_view(), name="create_empleado"),
    path('detail_empleado/<int:pk>/', EmpleadoDetail.as_view(), name="detail_empleado"),
    path('update_empleado/<int:pk>/', EmpleadoUpdate.as_view(), name="update_empleado"),
    path('delete_empleado/<int:pk>/', EmpleadoDelete.as_view(), name="delete_empleado"),

    path('clientes/', ClienteList.as_view(), name="clientes"),
    path('create_cliente/', ClienteCreate.as_view(), name="create_cliente"),
    path('detail_cliente/<int:pk>/', ClienteDetail.as_view(), name="detail_cliente"),
    path('update_cliente/<int:pk>/', ClienteUpdate.as_view(), name="update_cliente"),
    path('delete_cliente/<int:pk>/', ClienteDelete.as_view(), name="delete_cliente"),

    path('proovedores/', ProveedorList.as_view(), name="proveedores"),
    path('create_proveedor/', ProveedorCreate.as_view(), name="create_proveedor"),
    path('detail_proveedor/<int:pk>/', ProveedorDetail.as_view(), name="detail_proveedor"),
    path('update_proveedor/<int:pk>/', ProveedorUpdate.as_view(), name="update_proveedor"),
    path('delete_proveedor/<int:pk>/', ProveedorDelete.as_view(), name="delete_proveedor"),

    path('login/', login_request, name="login"),
    path('logout/', LogoutView.as_view(template_name="app/logout.html"), name="logout"),
    path('register/', register, name="register"),

    
    path('editar_perfil/', editarPerfil, name="editar_perfil"),
    path('agregar_avatar/', agregarAvatar, name="agregar_avatar"),


    path('producto/', producto, name="producto"),
    path('buscar_producto/', buscarProducto,  name="buscar_producto"),
    path('buscar3/', buscar3, name="buscar3"),
    path('form_producto', formProducto, name="form_producto"),
    path('form_producto2/', formProducto2, name="form_producto2"),

    path('acerca/', acerca, name="acerca"),

]