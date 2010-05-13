$.jQTouch({
	icon: 'jqtouch.png',
	    statusBar: 'black-translucent',
	    preloadImages: [

			    '/static/jqtouch/themes/img/toolbar.png',
			    '/static/jqtouch/themes/img/chevron.png',
			    '/static/jqtouch/img/chevron.png',
			    '/static/jqtouch/img/back_button_clicked.png', 
			    '/static/jqtouch/img/button_clicked.png',
		    ]
	    });
$(function(){
	// Show a swipe event on swipe test
	/*
	$('#home').
	    bind('pageAnimationEnd', function(e, info){
		    $('#neighborhood_link').attr('href', '/neighborhood/' + neighborhood.slug);
		    }); */
	$('#map').
	    bind('pageAnimationEnd', function(e, info){
		    var map = new google.maps.Map2(document.getElementById("map_canvas"));
		    map.setCenter(new google.maps.LatLng(neighborhood.centroid_y, 
							 neighborhood.centroid_x), 13);
		    
		    coords=eval(neighborhood.polygon);
		    
		    var polygon = new google.maps.Polygon(coords,
							  "#f33f00", 5, 1,"#f00000", 0.2); 
		  
		    map.addOverlay(polygon);
		});

	
	
    });

  
var neighborhood = "unknown";
if (neighborhood == "unknown") {
    if (navigator.geolocation) {  
	navigator.geolocation.getCurrentPosition(function(position) {  
		
		$.getJSON('/lookup?coords=' + position.coords.longitude + '%2C' + position.coords.latitude, 
			  function(data) {
			      neighborhood = data;
			      neighborhood_slug = data.slug;
			      $('#results').html('You are in ' + data.name);
			      $('dneighborhood_link').attr('href', '/neighborhood/' + data.slug);
			      $('#wikilink').attr('href', data.wiki);
			      $('#wikilink').text('Wikipedia Entry for ' + data.name);
			      $('#neighborhood_link').text(data.name + ' Information');
			      $('#status').hide();
			  });   
	    });
    }
    else {
	$('#results').html('Neighborhood (Location Unavailable)');
    }
}