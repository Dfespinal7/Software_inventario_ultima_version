function actDocumento(){
    var documento=document.getElementById('documento');
    var selectedOption = documento.options[documento.selectedIndex];
    var valor = selectedOption.getAttribute('data-documento');
    document.getElementById('doc').value = valor;
}

function cantidadStock() {
    // Obtiene los valores de los campos y los convierte a enteros
    var entrada = parseInt(document.getElementById('ent').value) || 0;
    var salida = parseInt(document.getElementById('sal').value) || 0;
    var resultado = entrada - salida;
    
    // Establece el resultado en el campo de stock
    var stockField = document.getElementById('stock');
    stockField.value = resultado;
    valorInv();
}
function valorInv(){
    stock=parseInt(document.getElementById("stock").value)||0
    ent=parseInt(document.getElementById("valoruni").value)||0
    result=stock*ent
    document.getElementById("valorinv").value=result
}



// Agrega eventos de input a los campos de entrada y salida
document.getElementById('ent').addEventListener('input', cantidadStock);
document.getElementById('sal').addEventListener('input', cantidadStock);
document.getElementById('valoruni').addEventListener('input', valorInv);
