$(document).ready(function(){

	//$("input[name*='-descripcion']").attr("readonly","true");
	$("input[name*='-precio_unitario']").attr("readonly","true");
	$("input[name*='-precio_total']").attr("readonly","true");

});

$("select[name*='-tipo']").on("change",function(){
debugger	
	var id_c=this.name;
	var uno_id=id_c.replace("detallecotizacion_set-", "");
	var res_id=uno_id.replace("-tipo", "");
	var namecant="detallecotizacion_set-"+res_id+"-cantidad";
	var nameancho="detallecotizacion_set-"+res_id+"-ancho";
	var namealto="detallecotizacion_set-"+res_id+"-altura";

	var tipo=this.value;


	var cantidad = $("input[name="+namecant+"]").val();
	var ancho = $("input[name="+nameancho+"]").val();
	var altura = $("input[name="+namealto+"]").val();
	var empaque = $("#id_empaque").val();
	var cepillo = $("#id_cepillo").val();
	console.log(cantidad,ancho,altura,tipo,res_id,empaque,cepillo)
	get_calcular(cantidad,ancho,altura,tipo,res_id,empaque,cepillo)

});
function totales()
{
			var precio=0;
			$( "[name*='precio_total']" ).each(function() {
			
				precio=precio+parseFloat($(this).val());

				console.log(precio)
				//$("#totalgeneral").val(precio);

			});
			var empaque=$("#id_empaque_costo").val();
			var cepillo=$("#id_cepillo_costo").val();
			precio=precio+parseFloat(empaque)+parseFloat(cepillo);
				document.getElementById("totalgeneral").value = precio;
}
function get_calcular(cantidad,ancho,altura,tipo,id,empaque,cepillo){
	debugger
			var empaque_costo=$("#id_empaque_costo").val();
			var cepillo_costo=$("#id_cepillo_costo").val();
		$.ajax({
	 	   	url:'/djmicrosip_cotizacion_puertas/calculo/',
	 	   	type : 'get',
	 	   	data : {
	 	   		'cantidad':cantidad,
	 	   		'ancho':ancho,
	 	   		'altura':altura,
	 	   		'tipo':tipo,
	 	   		'empaque':empaque,
	 	   		'cepillo':cepillo,
	 	   		'empaque_costo':empaque_costo,
	 	   		'cepillo_costo':cepillo_costo,
	 	   	},
	 	   	success: function(data){
	 	   		var namedesc="detallecotizacion_set-"+id+"-descripcion";
	 	   		$("input[name="+namedesc+"]").val(data.descripcion);
	 	   		var namedesc="detallecotizacion_set-"+id+"-precio_unitario";
	 	   		$("input[name="+namedesc+"]").val(data.unitario);
	 	   		var namedesc="detallecotizacion_set-"+id+"-precio_total";
	 	   		$("input[name="+namedesc+"]").val(data.total);
	 	   		$("#id_empaque_costo").val(data.empaque_costo);
				$("#id_cepillo_costo").val(data.cepillo_costo);
	 	   		totales()
			},
		});
}


