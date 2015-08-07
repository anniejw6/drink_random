$(function(){
	$('button').click(function(){
		d = $('form').serialize();
		console.log(d);
		$.ajax({
			url: '/signUpUser',
			// data: $('form').serialize(),
			//data: 'username=1&password=2', 
			//dataType: "json",
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
