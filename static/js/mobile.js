$.jQTouch({
	icon: 'jqtouch.png',
	    statusBar: 'black-translucent',
	    preloadImages: [
			    '/static/jqtouch/img/chevron.png',
			    '/static/jqtouch/img/back_button_clicked.png',
			    '/static/jqtouch/img/button_clicked.png'
			    ]
	    });
var neighborhood = "unknown";
if (neighborhood == "unknown") {
    if (navigator.geolocation) {  
	navigator.geolocation.getCurrentPosition(function(position) {  
		
		$.getJSON('/search?coords=' + position.coords.longitude + '%2C' + position.coords.latitude, 
			  function(data) {
			      neighborhood = data.name;
			      $('#results').html(data.name);
			      $('#title_results').html('Neighborhood (' + data.name + ')');
			  });   
	    });
    }
    else {
	$('#title_results').html('Neighborhood (Location Unavailable)');
    }
}