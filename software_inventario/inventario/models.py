from django.db import models


# Create your models here.



class Clientes(models.Model):
    idCliente=models.BigAutoField(primary_key=True,blank=True)
    nombre=models.CharField(max_length=150)
    documento=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre}"

class Categorias(models.Model):
    idCategoria=models.BigAutoField(primary_key=True,blank=True)
    nombreCategoria=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombreCategoria}"

class Proveedores(models.Model):
    idProveedor=models.BigAutoField(primary_key=True,blank=True)
    nombre=models.CharField(max_length=150)
    documento=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre}"

class Productos(models.Model):
    idProducto=models.CharField(primary_key=True,blank=True,max_length=150)
    idCategoria=models.ForeignKey(Categorias,on_delete=models.CASCADE)
    nombreProducto=models.CharField(max_length=150)
    unidadMedida=models.CharField(max_length=150,default="sin unidad de medida")
    stock=models.IntegerField(null=True,default=0) #el stock es el resultado de la resta de entradas y salidas, no confundir con cantidad de las otras tablas
    
    def __str__(self):
        return f"{self.nombreProducto}"

class Entradas(models.Model):
    idEntrada=models.BigAutoField(primary_key=True,blank=True)
    fechaEnt=models.DateField()
    idProveedor=models.ForeignKey(Proveedores,on_delete=models.CASCADE)
    idProducto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    unidadMedida=models.CharField(max_length=150,default=0)
    observacion=models.CharField(max_length=150,default=0)
    cantEntInicial=models.IntegerField(default=0)
    cantidadEntrada=models.IntegerField(default=0)
    valorUnidad=models.DecimalField(max_digits=30,decimal_places=0,default=0)

    def __str__(self):
        return f"{self.cantidadEntrada}" #esto es una prueba

class Salidas(models.Model):
    idSalida=models.BigAutoField(primary_key=True,blank=True)
    fechaSal=models.DateField()
    idProducto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    idCliente=models.ForeignKey(Clientes,on_delete=models.CASCADE)
    documento=models.CharField(max_length=150)  #viene del cliente
    observacion=models.CharField(max_length=150,default="sin Observacion")
    cantidadSalida=models.IntegerField(default=0)
    valorUnidad=models.IntegerField(default=0)
    totalValorSal=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.cantidadSalida}"

class StockInventarios(models.Model):
    idStockInventario=models.BigAutoField(primary_key=True,blank=True)
    nombreCategoria=models.CharField(max_length=150) #viene del producto
    idProducto=models.ForeignKey(Productos,on_delete=models.CASCADE) #va el nombre del producto
    unidadMedida=models.CharField(max_length=150) #va el nombre del producto
    totalEntrada=models.IntegerField()
    totalSalida=models.IntegerField()
    stock=models.IntegerField(default=0) #resultado de la resta de entre la entrada y la salida
    valorUnidad=models.DecimalField(max_digits=30,decimal_places=0,default=0) #puede venir de la tabla productos
    valorInvenario=models.IntegerField(default=0) #es la multiplicacion entre el stock y valorUnidad


class Usuarios(models.Model):
    ROLES=(
        (1,"administrador"),
        (2,"empleado"),
        (3,"superadmin")
    )
    idUsuario=models.BigAutoField(primary_key=True, blank=True)
    nombre=models.CharField(max_length=100)
    email=models.CharField(max_length=150, unique=True)
    password=models.CharField(max_length=150)
    rol=models.IntegerField(choices=ROLES,default=2)