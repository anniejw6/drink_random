$(function(){

	$(document).on('click', '.submit button', function () {   
		var text = document.getElementById("errnotes").value; 
		d = 'num_err='+newVal+'&err_descrip='+text;
		// console.log(d);
		// console.log(text);
		$.ajax({
			url: '/submission',
			data: d,
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});