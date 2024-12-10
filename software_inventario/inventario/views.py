from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa

#commit
def inicio(request):
    return render(request,'inventario/inicio.html')

def listar_stock(request):
    k=StockInventarios.objects.all()
    context={"data":k}
    return render(request,'inventario/stock/stock_inventario.html',context)

def listar_entrada(request):
    k=Entradas.objects.all()
    suma=0
    for i in k:
     suma=suma+i.valorUnidad*i.cantEntInicial
   
    context={"data":k,"suma":suma}
    return render(request,'inventario/entrada/listar_entrada.html',context)

def listar_producto(request):
    k=Productos.objects.all()
    context={"data":k}
    return render(request,'inventario/producto/listar_producto.html',context)

def form_guardar(request):
    k=Categorias.objects.all()
    p=Proveedores.objects.all()
    c=Clientes.objects.all()
    contex={"categorias":k,"proveedores":p,"clientes":c}
    return render(request,'inventario/producto/form_productos.html',contex)

def guardar_datos(request):
    if request.method=='POST':
        k = None  # Entradas
        s = None  # Salidas
        #Producto
        idProducto=request.POST.get("idProducto")
        fecha=request.POST.get("fecha")
        idCategoria=Categorias.objects.get(pk=request.POST.get("idCategoria"))
        nombre=request.POST.get("nombreProducto")
        unidadMedi=request.POST.get("unidadMedida")
        stock=request.POST.get("stock",0) or 0
        #Entrada
        idEntrada=request.POST.get("idEntrada")
        idProveedor=Proveedores.objects.get(pk=request.POST.get("idProveedor"))
        #idProducto=request.POST.get("idProducto")
        #unidadMedi=request.POST.get("unidadMedida")
        obsent=request.POST.get("obsent")
        cantent=request.POST.get("cantent",0) or 0
        valoruEntr=request.POST.get("valoruEntr",0) or 0
        #Salida
        idSalida=request.POST.get("idSalida")
        #idProducto=request.POST.get("idProducto")
        idCliente=Clientes.objects.get(pk=request.POST.get("idCliente"))
        doc=request.POST.get("documento",0)or 0
        obssal=request.POST.get("obssal")
        cantsal=request.POST.get("cantsal",0) or 0
        valoruSal=request.POST.get("valoruSal",0) or 0
        #stock
        idStockInventadrio=request.POST.get("idStock")
        #idCategoria=Categorias.objects.get(pk=request.POST.get("idCategoria"))
        #idProducto=request.POST.get("idProducto")
        #unidadMedi=request.POST.get("unidadMedida")
        #idEntrada=request.POST.get("idEntrada")
        #idSalida=request.POST.get("idSalida")
        #stock=request.POST.get("stock")
        #valoruEntr=request.POST.get("valoruEntr")
        valorinv=request.POST.get("valorinv",0) or 0
        
        if Productos.objects.filter(idProducto=idProducto).exists():
            messages.error(request,f'El id {idProducto} ya existe en la base de datos')
            return redirect('form_guardar')

        q=Productos(idProducto=idProducto,idCategoria=idCategoria,nombreProducto=nombre,unidadMedida=unidadMedi,stock=stock)
        q.save()
        resta=int(cantent)-int(cantsal)
        messages.success(request, "Producto creado correctamente")
        if int(cantent)>0:
          k=Entradas(idProveedor=idProveedor,idProducto=q,unidadMedida=unidadMedi,observacion=obsent,cantidadEntrada=resta,cantEntInicial=cantent,valorUnidad=valoruEntr,fechaEnt=fecha)
          k.save()
          messages.success(request, "Entrada Creada Correctamente")
        else:
            pass  
        if int(cantsal)>0:    
          s=Salidas(idProducto=q,idCliente=idCliente,documento=doc,observacion=obssal,cantidadSalida=cantsal,valorUnidad=valoruSal,fechaSal=fecha)
          s.save()
          messages.success(request, "Salida Creada Correctamente")
        else:
            pass
        cat=q.idCategoria
        unim=q.unidadMedida
        stock1=q.stock
        if k:
            uni=k.valorUnidad
        else:
            uni=0       
        inv=StockInventarios(nombreCategoria=cat,idProducto=q,unidadMedida=unim,totalEntrada=k.cantidadEntrada if k else 0,totalSalida=s.cantidadSalida if s else 0,stock=stock1,valorUnidad=uni,valorInvenario=valorinv)
        inv.save()
        messages.success(request, "Stock Creado Correctamente")
        
        return HttpResponseRedirect(reverse('listar_producto',args=()))
    

def listar_salida(request):
        k=Salidas.objects.all()
        context={"data":k}
        return render(request,'inventario/salida/listar_salidas.html',context)

def listar_proveedor(request):
     q=Proveedores.objects.all()
     contex={"data":q}
     return render(request,'inventario/proveedor/listar_proveedor.html',contex)

def listar_cliente(request):
     q=Clientes.objects.all()
     contex={"data":q}
     return render(request,'inventario/cliente/listar_cliente.html',contex)
 
def listar_categoria(request):
     q=Categorias.objects.all()
     contex={"data":q}
     return render(request,'inventario/categoria/listar_categoria.html',contex)

def form_entradas(request):
     k=Productos.objects.all()
     q=Proveedores.objects.all()
     context={"productos":k,"proveedores":q}
     return render(request,'inventario/entrada/form_entrada.html',context)

def guardar_entrada(request):
     if request.method=='POST':
          idEntrada=request.POST.get("idEntrada")
          fecha=request.POST.get("fechaEntrada")
          producto=Productos.objects.get(pk=request.POST.get("producto"))
          proveedor=Proveedores.objects.get(pk=request.POST.get("proveedor"))
          unidad=request.POST.get("unidadMedida")
          obs=request.POST.get("observacion")
          cantent=request.POST.get("cantidadEntrada")
          valoru=request.POST.get("valorUnidad")
          cantEntActual=request.POST.get("cantEntActual")
          if idEntrada=='':
               ent=Entradas(fechaEnt=fecha,idProveedor=proveedor,idProducto=producto,unidadMedida=unidad,observacion=obs,cantidadEntrada=cantent,cantEntInicial=cantent,valorUnidad=valoru)
               ent.save()

              
          
               
               
               messages.success(request,"Entrada creada correctamente")
               stock=StockInventarios.objects.get(idProducto=producto)
               sum=stock.totalEntrada+int(cantent)
               stock.totalEntrada=sum
               stock.stock=sum-int(stock.totalSalida)
               
               stock.valorInvenario=int(stock.valorInvenario)+(int(valoru)*int(cantent))
               stock.valorUnidad=int(stock.valorInvenario)/int(stock.stock)
               stock.save()
               
               actproduct=Productos.objects.get(idProducto=producto.idProducto)
               actproduct.stock=stock.stock
               actproduct.save()
               
               return HttpResponseRedirect(reverse('listar_entrada'))
          else:
               e=Entradas.objects.get(pk=idEntrada)
               if e.cantEntInicial!=e.cantidadEntrada:
                   messages.error(request,'Las Entradas que ya han tenido salidas no pueden ser modificadas')
                   return redirect('listar_entrada')
               elif e.cantEntInicial==e.cantidadEntrada:
                e.fechaEnt=fecha
                e.idProveedor=proveedor
                e.idProducto=producto
                e.unidadMedida=unidad
                e.observacion=obs
                e.cantEntInicial=cantent
                e.cantidadEntrada=cantent
                e.valorUnidad=valoru
                e.save()  

                sal=Salidas.objects.filter(idProducto=producto)
                totalsal=0
                for i in sal:
                    totalsal=totalsal+int(i.totalValorSal)
                print(totalsal)
                
                messages.success(request,"Entrada Crada correctamente")
                stock=StockInventarios.objects.get(idProducto=producto)
                entra=Entradas.objects.filter(idProducto=producto)
                totalent=0
                valorinv=0
                for i in entra:
                    totalent=totalent+int(i.cantEntInicial)
                    valorinv=valorinv+int(i.cantEntInicial)*int(i.valorUnidad)
                    print(valorinv)
                

                stock.totalEntrada=totalent
                stock.valorInvenario=valorinv-totalsal
                stock.stock=int(stock.totalEntrada)-int(stock.totalSalida)
                stock.valorUnidad=int(stock.valorInvenario)/int(stock.stock)
                stock.save()

                
                actproduct=Productos.objects.get(idProducto=producto.idProducto)
                actproduct.stock=stock.stock
                actproduct.save()
                
                return HttpResponseRedirect(reverse('listar_entrada'))


              
              
     
def form_salida(request):
     c=Clientes.objects.all()
     p=Productos.objects.all()
     contex={"clientes":c,"productos":p}
     return render(request,'inventario/salida/form_salidas.html',contex)
     
def guardar_salida(request):
    if request.method == 'POST':
        idSalida = request.POST.get("idSalida")
        fecha = request.POST.get("fecha")
        cliente = Clientes.objects.get(pk=request.POST.get("cliente"))
        producto = Productos.objects.get(pk=request.POST.get("producto"))
        obs = request.POST.get("observacion")
        cantsal = int(request.POST.get("cantidadSalida"))
        valoru = int(request.POST.get("valorUnidad",0) or 0)
        nueva_cantidad_salida = cantsal

        # Obtener el stock del producto
        s = StockInventarios.objects.get(idProducto=producto)
        if cantsal > int(s.stock):
            messages.error(request,f"La cantidad de la  salida supera el stock de este producto, actualmente hay {s.stock} almacenados en stock")
            return redirect('form_salida')
        else:

            # Calcular la cantidad y el valor de la salida
            ent = Entradas.objects.filter(idProducto=producto).order_by('fechaEnt')
            cantidad_a_saldar = cantsal
            valor_total_salida = 0

            # Si es una edición de una salida existente
            if idSalida:
                try:
                    # Obtener la salida original para comparar
                    salida_original = Salidas.objects.get(pk=idSalida)
                    cantidad_salida_anterior = salida_original.cantidadSalida

                    # Restaurar el inventario original (revertir la salida previa)
                    s.totalSalida -= cantidad_salida_anterior  # Devolver las unidades de salida previas
                    s.stock += cantidad_salida_anterior  # Aumentar el stock nuevamente
                    valor_total_salida_anterior = salida_original.totalValorSal
                    s.valorInvenario += valor_total_salida_anterior  # Aumentar el valor del inventario nuevamente
                    s.valorUnidad = s.valorInvenario / s.stock if s.stock > 0 else 0
                    s.save()

                    # Restaurar las cantidades en las entradas
                    cantidad_a_restaurar = cantidad_salida_anterior
                    for entrada in ent:
                        if cantidad_a_restaurar <= 0:
                            break
                        cantidad_usada = entrada.cantEntInicial - entrada.cantidadEntrada
                        cantidad_a_restituir = min(cantidad_a_restaurar, cantidad_usada)
                        entrada.cantidadEntrada += cantidad_a_restituir
                        cantidad_a_restaurar -= cantidad_a_restituir
                        entrada.save()

                except Exception as e:
                    messages.error(request, f"Error al restaurar la salida anterior: {str(e)}")
                    return redirect('formulario_salida')

            # Aplicar la nueva salida
            cantidad_a_saldar = nueva_cantidad_salida
            for entrada in ent:
                if cantidad_a_saldar <= 0:
                    break
                cantidad_disponible = int(entrada.cantidadEntrada)
                valor_unitario = int(entrada.valorUnidad)

                if cantidad_disponible <= cantidad_a_saldar:
                    valor_total_salida += cantidad_disponible * valor_unitario
                    cantidad_a_saldar -= cantidad_disponible
                    entrada.cantidadEntrada = 0  # Marcar esta entrada como completamente usada
                else:
                    valor_total_salida += cantidad_a_saldar * valor_unitario
                    entrada.cantidadEntrada -= cantidad_a_saldar
                    cantidad_a_saldar = 0
                entrada.save()

            # Actualizar o crear la salida
            if idSalida == '':
                salida = Salidas(
                    fechaSal=fecha,
                    idProducto=producto,
                    idCliente=cliente,
                    documento=cliente.documento,
                    observacion=obs,
                    cantidadSalida=nueva_cantidad_salida,
                    valorUnidad=valoru,
                    totalValorSal=valor_total_salida
                )
                salida.save()
            else:
                salida_original.fechaSal = fecha
                salida_original.idCliente = cliente
                salida_original.idProducto = producto
                salida_original.documento = cliente.documento
                salida_original.observacion = obs
                salida_original.cantidadSalida = nueva_cantidad_salida
                salida_original.valorUnidad = valoru
                salida_original.totalValorSal = valor_total_salida
                salida_original.save()

            # Actualizar el inventario
            s.totalSalida += nueva_cantidad_salida
            s.stock -= nueva_cantidad_salida
            s.valorInvenario -= valor_total_salida
            s.valorUnidad = s.valorInvenario / s.stock if s.stock > 0 else 0
            s.save()

            # Actualizar el stock en Productos
            producto.stock = s.stock
            producto.save()

            messages.success(request, 'Salida editada correctamente' if idSalida else 'Salida creada correctamente')
            return HttpResponseRedirect(reverse('listar_salida'))

    return HttpResponseRedirect(reverse('listar_salida'))





   

def editar_entrada(request,idEntrada):
     k=Entradas.objects.get(pk=idEntrada)
     p=Proveedores.objects.all()
     pro=Productos.objects.all()
     context={"data":k,"idEntrada":idEntrada,"proveedores":p,"productos":pro}
     return render(request,'inventario/entrada/form_entrada.html',context)


def editar_salida(request,idSalida):
    c=Clientes.objects.all()
    p=Productos.objects.all()
    s=Salidas.objects.get(pk=idSalida)
    context={"idSalida":idSalida,"clientes":c,"productos":p,"data":s}
    return render(request,'inventario/salida/form_salidas.html',context)


def eliminar_entrada(request, idEntrada):
    try:
        entrada = Entradas.objects.get(pk=idEntrada)
        producto = entrada.idProducto

        # Actualizar el stock antes de eliminar la entrada
        stock = StockInventarios.objects.get(idProducto=producto)
        stock.totalEntrada -= entrada.cantidadEntrada
        stock.valorInvenario -= entrada.cantidadEntrada * entrada.valorUnidad
        stock.stock = stock.totalEntrada - stock.totalSalida
        stock.valorUnidad = stock.valorInvenario / stock.stock if stock.stock > 0 else 0
        stock.save()

        # Eliminar la entrada
        entrada.delete()

        # Actualizar el stock del producto
        producto.stock = stock.stock
        producto.save()

        messages.success(request, 'Entrada eliminada correctamente')
    except Entradas.DoesNotExist:
        messages.error(request, 'Entrada no encontrada')
    except Exception as e:
        messages.error(request, f'Error al eliminar la entrada: {str(e)}')

    return HttpResponseRedirect(reverse('listar_entrada'))


def eliminar_salida(request, idSalida):
    try:
        salida = Salidas.objects.get(pk=idSalida)
        producto = salida.idProducto

        # Obtener el stock del producto
        stock = StockInventarios.objects.get(idProducto=producto)

        # Restaurar el inventario original
        stock.totalSalida -= salida.cantidadSalida
        stock.stock += salida.cantidadSalida
        stock.valorInvenario += salida.totalValorSal
        stock.valorUnidad = stock.valorInvenario / stock.stock if stock.stock > 0 else 0
        stock.save()

        # Restaurar las cantidades en las entradas
        entradas = Entradas.objects.filter(idProducto=producto).order_by('fechaEnt')
        cantidad_a_restaurar = salida.cantidadSalida
        for entrada in entradas:
            if cantidad_a_restaurar <= 0:
                break
            cantidad_usada = entrada.cantEntInicial - entrada.cantidadEntrada
            cantidad_a_restituir = min(cantidad_a_restaurar, cantidad_usada)
            entrada.cantidadEntrada += cantidad_a_restituir
            cantidad_a_restaurar -= cantidad_a_restituir
            entrada.save()

        # Eliminar la salida
        salida.delete()

        messages.success(request, 'Salida eliminada correctamente')
    except Salidas.DoesNotExist:
        messages.error(request, 'Salida no encontrada')
    except Exception as e:
        messages.error(request, f'Error al eliminar la salida: {str(e)}')

    return HttpResponseRedirect(reverse('listar_salida'))

def form_edit_product(request,idProducto):
    k=Productos.objects.get(pk=idProducto)
    cat=Categorias.objects.all()
    context={"idProducto":idProducto,"data":k,"categorias":cat}
    return render(request,'inventario/producto/edit_product.html',context)

def guardar_edit_product(request):
    if request.method=='POST':
        idProducto=request.POST.get("idProducto")
        categ=Categorias.objects.get(pk=request.POST.get("idCategoria"))
        nombre=request.POST.get("nombreProducto")
        unidad=request.POST.get("unidadMedida")
        stock=request.POST.get("stock")

        pro=Productos.objects.get(pk=idProducto)
        pro.idCategoria=categ
        pro.nombreProducto=nombre
        pro.unidadMedida=unidad
        pro.stock=stock
        pro.save()
        messages.success(request,'Producto editado correctamente')
        return redirect('listar_producto')

def buscar_producto(request):
    if request.method=='POST':
        prod=request.POST.get("producto")
        query=Productos.objects.filter(nombreProducto__icontains=prod)
        context={"prod":prod,"data":query}
        return render(request,'inventario/producto/listar_producto.html',context)
    else:
        messages.warning(request,"No se encontro Usuario")
    return HttpResponseRedirect(reverse("listar_citas"))

def eliminar_producto(request,idProducto):
    pro=Productos.objects.get(pk=idProducto)
    pro.delete()
    messages.warning(request,"El producto ha sido eliminado")
    return redirect('listar_producto')

def buscar_entrada(request):
    if request.method=='POST':
        prod=request.POST.get("producto")
        k=Entradas.objects.filter(idProducto__nombreProducto__icontains=prod)
        suma=0
        for i in k:
            suma=suma+i.cantEntInicial*i.valorUnidad
        context={"data":k,"prod":prod,"suma":suma}
        return render(request,'inventario/entrada/listar_entrada.html',context)

def buscar_salida(request):
    if request.method=='POST':
        prod=request.POST.get("producto")
        p=Salidas.objects.filter(idProducto__nombreProducto__icontains=prod)
        contex={"data":p,"prod":prod}
        return render(request,'inventario/salida/listar_salidas.html',contex)
    
def buscar_stock(request):
    if request.method=='POST':
        pro=request.POST.get("producto")
        k=StockInventarios.objects.filter(idProducto__nombreProducto__icontains=pro)
        context={"data":k,"pro":pro}
        return render(request,'inventario/stock/stock_inventario.html',context)

def form_proveedor(request):
    return render(request,'inventario/proveedor/form_proveedor.html')

def guardar_proveedor(request):
    if request.method=='POST':
        idProveedor=request.POST.get("idProveedor")
        nom=request.POST.get("nombreProveedor")
        doc=request.POST.get("documento")
        if idProveedor=='':
            pro=Proveedores(nombre=nom,documento=doc)
            pro.save()
            messages.success(request,'Proveedor añadido correctamente')
            return redirect('listar_proveedor')
        else:
            p=Proveedores.objects.get(pk=idProveedor)
            p.nombre=nom
            p.documento=doc
            p.save()
            messages.success(request,'Proveedor editado correctamente')
            return redirect('listar_proveedor')
    
def editar_proveedor(request,idProveedor):
    pro=Proveedores.objects.get(pk=idProveedor)
    contex={"data":pro,"idProveedor":idProveedor}
    return render(request,'inventario/proveedor/form_proveedor.html',contex)

def eliminar_proveedor(request,idProveedor):
    p=Proveedores.objects.get(pk=idProveedor)
    p.delete()
    messages.warning(request,'Proveedor eliminado')
    return redirect('listar_proveedor')
def buscar_proveedor(request):
    if request.method=='POST':
        proveedor=request.POST.get("proveedor")
        p=Proveedores.objects.filter(nombre__icontains=proveedor)
        contex={"data":p,"proveedor":proveedor}
        return render(request,'inventario/proveedor/listar_proveedor.html',contex)
    
def form_categoria(request):
    return render(request,'inventario/categoria/form_categoria.html')

def guardar_categoria(request):
    if request.method=='POST':
        idCategoria=request.POST.get("idCategoria")
        nom=request.POST.get("categoria")
        if idCategoria=='':
            c=Categorias(nombreCategoria=nom)
            c.save()
            messages.success(request,'Categoria Añadida')
            
        else:
            c=Categorias.objects.get(pk=idCategoria)
            c.nombreCategoria=nom
            c.save()
            messages.success(request,'Categoria editada correctamente')
        return redirect('listar_categoria')

    
def editar_categoria(request,idCategoria):
    c=Categorias.objects.get(pk=idCategoria)
    context={"data":c,"idCategoria":idCategoria}
    return render(request,'inventario/categoria/form_categoria.html',context)

def eliminar_categoria(request,idCategoria):
    c=Categorias.objects.get(pk=idCategoria)
    c.delete()
    messages.warning(request,"Categoria Eliminada")
    return redirect('listar_categoria')

def buscar_categoria(request):
    if request.method=='POST':
        nombre=request.POST.get("nombre")
        c=Categorias.objects.filter(nombreCategoria__icontains=nombre)
        contex={"data":c,"nombre":nombre}
        return render(request,'inventario/categoria/listar_categoria.html',contex)
    
def form_clientes(request):
    return render(request,'inventario/cliente/form_cliente.html')

def guardar_cliente(request):
    if request.method=='POST':
        idCliente=request.POST.get("idCliente")
        nombre=request.POST.get("nombre")
        doc=request.POST.get("documento")
        if idCliente=='':
            c=Clientes(nombre=nombre,documento=doc)
            c.save()
            messages.success(request,"Cliente añadido correctamente")
            
        else:
            c=Clientes.objects.get(pk=idCliente)
            c.nombre=nombre
            c.documento=doc
            c.save()
            messages.success(request,"Cliente editado correctamente")
        return redirect('listar_cliente')
    
def editar_cliente(request,idCliente):
    c=Clientes.objects.get(pk=idCliente)
    contex={"data":c,"idCliente":idCliente}
    return render(request,'inventario/cliente/form_cliente.html',contex)

def eliminar_cliente(request,idCliente):
    cli=Clientes.objects.get(pk=idCliente)
    cli.delete()
    messages.warning(request,'Cliente Eliminado')
    return redirect('listar_cliente')

def buscar_cliente(request):
    if request.method=='POST':
        nom=request.POST.get("cliente")
        c=Clientes.objects.filter(nombre__icontains=nom)
        contex={"data":c,"nom":nom}
        return render(request,'inventario/cliente/listar_cliente.html',contex)
    
def listar_peps(request):
    p=Productos.objects.all()
    contex={"productos":p}
    return render(request,'inventario/stock/peps.html',contex)

def busqueda_peps(request):
    p=Productos.objects.all()
    if request.method=='GET':
        codigo=request.GET.get("codigo")
        ent=Entradas.objects.filter(idProducto__idProducto__icontains=codigo).order_by('fechaEnt')
        for i in ent:
            i.diferen=int(i.cantEntInicial)-int(i.cantidadEntrada)
        messages.success(request,f'PEPS del producto {codigo}')
    contex={"productos":p,"entradas":ent}
    return render(request,'inventario/stock/peps.html',contex)

def listar_abc(request):
    abc = StockInventarios.objects.all()
    enta = Entradas.objects.all()
    totalinvent = sum(int(v.cantEntInicial) * int(v.valorUnidad) for v in enta)

    # Crear un diccionario para almacenar las sumas de cada producto
    valor_por_producto = {}

    # Calcular totalvalorE para cada producto
    for i in abc:
        ent = Entradas.objects.filter(idProducto=i.idProducto)
        suma = sum(int(e.valorUnidad) * int(e.cantEntInicial) for e in ent)
        valor_por_producto[i.idProducto] = suma

    # Ordenar los productos según su totalvalorE
    abc = sorted(abc, key=lambda x: valor_por_producto[x.idProducto], reverse=True)

    # Asignar los valores a cada producto
    sumatotal = 0
    for i in abc:
        suma = valor_por_producto[i.idProducto]
        sumatotal += suma
        i.totalvalorE = suma
        i.sumat = sumatotal
        i.porcent = (sumatotal / totalinvent * 100) if totalinvent else 0

    contex = {"data": abc}
    return render(request, 'inventario/stock/indicadoresabc.html', contex)

def descargar_pdf_entrada(request, idEntrada):
    entrada=Entradas.objects.get(pk=idEntrada)
    valor=int(entrada.cantEntInicial)*int(entrada.valorUnidad)
    contex={"data":entrada,"valor":valor}
    html_content=render_to_string('inventario/entrada/remision_ent.html',contex)
    response=HttpResponse(content_type='application/pdf')
    response['Content-Dispotition']='attachment';filename="remision.pdf"
    pisa_status=pisa.CreatePDF(html_content,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')

    return response

def descargar_pdf_salida(request,idSalida):
    salida=Salidas.objects.get(pk=idSalida)
    subtotal=int(salida.cantidadSalida)*int(salida.valorUnidad)
    iva=None
    if subtotal>0:
        iva=subtotal*19/100
    else:
        iva=0
    total=subtotal+iva
    contex={"data":salida,"subtotal":subtotal,"iva":iva,"total":total}
    html_content=render_to_string('inventario/salida/factura_salida.html',contex)
    response=HttpResponse(content_type='application/pdf')
    response['Content-Dispotition']='attachment';filename="factura.pdf"
    pisa_status=pisa.CreatePDF(html_content,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')

    return response

    

def vista_loguin(request):
    return render(request,'inventario/autenticacion/loguin.html')

def loguin(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            q=Usuarios.objects.get(email=username,password=password)
            datos={"nombre":q.nombre,
                   "email":q.email,
                   "password":q.password,
                   "rol":q.rol}
            request.session["logueo"]=datos
            messages.success(request,f'Bienvenido {q.nombre}!!!')
            return redirect('inicio')
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario o contraseña no válidos...")
            return render(request,'inventario/autenticacion/loguin.html')
    else:
        if request.session.get("logueo", False):
            return redirect('inicio')
        else:
            return redirect('inicio')
        
def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request,"Sesión cerrada correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('vista_loguin')

def vista_registro_usuario(request):
    return render(request,'inventario/autenticacion/registrar_usuario.html')
    #prueba commit


def registrar_usuario(request):
    if request.method=='POST':
        nombre=request.POST.get("nombre")
        emaila=request.POST.get("email")
        password=request.POST.get("password")
        rol=request.POST.get("rol")

        usuarios=Usuarios.objects.all()
        for i in usuarios:
            
            if i.email==emaila:
                messages.error(request,'Ya existe un usuario creado con ese correo')
                return redirect('vista_registro_usuario')
                break

        usu=Usuarios(nombre=nombre,email=emaila,password=password,rol=rol)
        usu.save()
        messages.success(request,'Usuario registrado corectamente')
        return redirect ('vista_loguin')
        
def vista_factura(request):
    obj=Clientes.objects.all()
    contex={"data":obj}
    return render(request,'inventario/salida/generar_fact.html',contex)

def lista_factura(request):
    obj = Clientes.objects.all()
    if request.method == 'POST':
        fecha = request.POST.get("fecha")
        cliente = request.POST.get("cliente")
        formato = request.POST.get("formato")
        
        s = Salidas.objects.filter(fechaSal=fecha, idCliente__idCliente=cliente)
        
        if formato == "factura":
            nombre = ""
            doc = ""
            subtotal = 0
            iva = 0
            
            if s.exists():
                nombre = s[0].idCliente.nombre
                doc = s[0].documento
                for i in s:      
                    subtotal += i.valorUnidad*i.cantidadSalida
                
                if subtotal > 0:
                    iva = subtotal * 19 / 100
                
                total = subtotal + iva
                contex = {
                    "datos": s,
                    "data": obj,
                    "nombre": nombre,
                    "doc": doc,
                    "fecha": fecha,
                    "subtotal": subtotal,
                    "iva": iva,
                    "total": total
                }
                html_content = render_to_string('inventario/salida/facturas_form.html', contex)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="factura_salidas.pdf"' 
                pisa_status = pisa.CreatePDF(html_content, dest=response)
                
                if pisa_status.err:
                    return HttpResponse('Error al generar PDF')
                return response
            
            else:
                return HttpResponse('No se encontraron salidas para la fecha y cliente seleccionados.')

        elif formato == "remision":
            context = {"data": s, "fecha": fecha}
            
            if s.exists():
                html_contentr = render_to_string('inventario/salida/remision_salida.html', context)
                responsea = HttpResponse(content_type='application/pdf')
                responsea['Content-Disposition'] = 'inline; filename="remision_salidas.pdf"'  
                pisa_statusa = pisa.CreatePDF(html_contentr, dest=responsea)
                
                if pisa_statusa.err:
                    return HttpResponse('Error al generar PDF')
                return responsea
            
            else:
                return HttpResponse('No se encontraron salidas para la fecha y cliente seleccionados.')




def Grafica(request):
    # Obtén todos los registros de StockInventarios
    inventarios = StockInventarios.objects.all()
    
    # Inicializa listas para los datos de la gráfica
    nombres_productos = []
    stocks = []
    entradas_totales = []
    salidas_totales = []

    # Filtrar y preparar los datos por producto
    for inventario in inventarios:
        # Obtener el nombre del producto y el stock actual
        nombres_productos.append(inventario.idProducto.nombreProducto)
        stocks.append(inventario.stock)
        
        # Filtrar entradas y salidas para cada producto
        entradas_producto = Entradas.objects.filter(idProducto=inventario.idProducto)
        salidas_producto = Salidas.objects.filter(idProducto=inventario.idProducto)
        
        # Calcular las entradas y salidas totales para cada producto
        total_entradas = sum(entrada.cantEntInicial for entrada in entradas_producto)
        total_salidas = sum(salida.cantidadSalida for salida in salidas_producto)
        
        entradas_totales.append(total_entradas)
        salidas_totales.append(total_salidas)

    # Obtener el tipo de filtro desde la URL
    tipo = request.GET.get("tipo")

    # Filtrar los datos según el tipo seleccionado (si corresponde)
    if tipo == "entradas":
        salidas_totales = [0] * len(entradas_totales)
    elif tipo == "salidas":
        entradas_totales = [0] * len(salidas_totales)

    # Contexto para la plantilla
    context = {
        "data": inventarios,
        "nombres_productos": nombres_productos,
        "stocks": stocks,
        "entradas_totales": entradas_totales,
        "salidas_totales": salidas_totales,
        "tipo": tipo,
    }

    return render(request, 'inventario/stock/Grafica.html', context)


def listar_usuario(request):
    usu=Usuarios.objects.all()
    contex={"data":usu}
    return render(request,'inventario/usuario/listar_usuario.html',contex)

def form_usuario(request):
    return render(request,'inventario/usuario/form_usuario.html')

def guardar_usuario(request):
    if request.method=='POST':
        idUsuario=request.POST.get("idUsuario")
        nombre=request.POST.get("nombre")
        email=request.POST.get("email")
        contra=request.POST.get("contra")
        rol=request.POST.get("rol")
        if idUsuario == '':
            k=Usuarios.objects.all()
            for i in k:
                if i.email==email:
                    messages.error(request,"Ya existe un usuario creado con este email")
                    return render(request,'inventario/usuario/form_usuario.html')
                    break
                else:
                    pass
            usu=Usuarios(nombre=nombre,email=email,password=contra,rol=rol)
            usu.save()
            messages.success(request,"Usuario creado correctamente")
            return redirect('listar_usuario')
        else:
            user=Usuarios.objects.get(pk=idUsuario)
            user.nombre=nombre
            user.email=email
            user.password=contra
            user.rol=rol
            user.save()
            messages.success(request,"Usuario editado correctamente")
            return redirect('listar_usuario')

def editar_usuario(request,idUsuario):
    usu=Usuarios.objects.get(pk=idUsuario)
    contex={"data":usu,"idUsuario":idUsuario}
    return render(request,'inventario/usuario/form_usuario.html',contex)

def eliminar_usuario(request,idUsuario):
    user=Usuarios.objects.get(pk=idUsuario)
    user.delete()
    messages.warning(request,'Usuario eliminado correctamente')
    return redirect('listar_usuario')