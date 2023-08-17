from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import * 
from .forms import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "app/base.html")


def empleados(request):
    return render(request, "app/empleados.html")

def acerca(request):
    return render(request, "app/acerca.html")

def clientes(request):
    return render(request, "app/clientes.html")

def proveedores(request):
    return render(request, "app/proveedores.html")

def producto(request):
    return render(request, "app/producto.html")

def producto(request):
    ctx = {"db": Producto.objects.all()}
    return render(request, "app/producto.html", ctx)


class EmpleadoList(LoginRequiredMixin, ListView):
    model = Empleado

class EmpleadoCreate(LoginRequiredMixin, CreateView):
    model = Empleado
    fields = ['nombre', 'apellido', 'cargo', 'email', 'telefono']
    success_url = reverse_lazy('empleados')

class EmpleadoDetail(LoginRequiredMixin, DetailView):
    model = Empleado

class EmpleadoUpdate(LoginRequiredMixin, UpdateView):
    model = Empleado
    fields = ['nombre', 'apellido', 'cargo', 'email', 'telefono']
    success_url = reverse_lazy('empleados')

class EmpleadoDelete(LoginRequiredMixin, DeleteView):
    model = Empleado
    success_url = reverse_lazy('empleados')


#_____________________

class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente

class ClienteCreate(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'email', 'telefono']
    success_url = reverse_lazy('clientes')

class ClienteDetail(LoginRequiredMixin, DetailView):
    model = Cliente

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido',  'email', 'telefono']
    success_url = reverse_lazy('clientes')

class ClienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('clientes')

#__________________________________
#
class ProveedorList(LoginRequiredMixin, ListView):
    model = Proveedor

class ProveedorCreate(LoginRequiredMixin, CreateView):
    model = Proveedor
    fields = ['nombre', 'email', 'telefono']
    success_url = reverse_lazy('proveedores')

class ProveedorDetail(LoginRequiredMixin, DetailView):
    model = Proveedor

class ProveedorUpdate(LoginRequiredMixin, UpdateView):
    model = Proveedor
    fields = ['nombre', 'email', 'telefono']
    success_url = reverse_lazy('proveedores')

class ProveedorDelete(LoginRequiredMixin, DeleteView):
    model = Proveedor
    success_url = reverse_lazy('proveedores')

#__________________________________ Login, logout y registro
#

def login_request(request):
    if request.method == "POST":
        miForm = AuthenticationForm(request, data=request.POST)
        if miForm.is_valid(): 
            usuario = miForm.cleaned_data.get('username')
            clave = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                login(request, user)
# __________________
                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = '/media/avatares/default.jpg'
                finally:
                    request.session['avatar'] = avatar



                return render(request, "app/base.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request, "app/login.html", {"form":miForm, "mensaje": "Datos inválidos"})
        else:
            return render(request, "app/login.html", {"form":miForm,"mensaje": "Datos inválidos"})


    miForm = AuthenticationForm()    

    return render(request, "app/login.html", {"form":miForm})

def register(request):
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST) # UserCreationForm 
        if form.is_valid():  # Si pasó la validación de Django
            usuario = form.cleaned_data.get('username')
            form.save()
            return render(request, "app/base.html", {"mensaje":"Usuario Creado"})        
    else:
        form = RegistroUsuariosForm() # UserCreationForm 

    return render(request, "app/registro.html", {"form": form}) 


#_________________________ Registro de usuarios
#

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()
            return render(request, "app/base.html", {'mensaje': f"Usuario {usuario.username} actualizado correctamente"})
        else:
            return render(request, "app/editarPerfil.html", {'form': form })
    else:
         form = UserEditForm(instance=usuario)
    return render(request, "app/editarPerfil.html", {'form': form, 'usuario':usuario.username})



@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            #_________________ Esto es para borrar el avatar anterior
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0: # Si esto es verdad quiere decir que hay un Avatar previo
                avatarViejo[0].delete()

            #_________________ Grabo avatar nuevo
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()

            #_________________ Almacenar en session la url del avatar para mostrarla en base
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session['avatar'] = imagen

            return render(request, "app/base.html")
    else:
        form = AvatarFormulario()
    return render(request, "app/agregarAvatar.html", {'form': form})


#___________________

def buscarProducto(request):
    return render(request, "app/producto.html")

def buscar3(request):
    if request.GET['precio']:
        precio = request.GET['precio']
        producto = Producto.objects.filter(precio__icontains=precio)
        return render(request,
                      "app/resultadosProducto.html",
                     {"precio":precio, "db":producto})
    
    return HttpResponse("No se ingresaron datos para la búsqueda")

def formProducto(request):
    if request.method == "POST":
        producto = Producto(nombre=request.POST['nombre'], precio=request.POST['precio'])
        producto.save()
        return HttpResponse("Se grabó con exito")
    
    

    return render(request, "app/productoForm.html")

def formProducto2(request):
     if request.method == "POST":
        miForm2 = formProducto2(request.POST)
        if miForm2.is_valid: 
             informacion = miForm2.cleaned_data
             producto = Producto(nombre=informacion['nombre'], precio=informacion['precio'])
             producto.save()
             return render(request, "app/base.html")

     else:
         miForm2 = formProducto()
        
        
         return render(request, "app/formProducto2.html", {"form":miForm2})

