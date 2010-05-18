var neighborhood = "unknown";

function get_location() {

    if (neighborhood == "unknown") {
	if (navigator.geolocation) {  
	    navigator.geolocation.getCurrentPosition(function(position) {  
		    var coords = position.coords.longitude + '%2C' + position.coords.latitude;
		    $.getJSON('/lookup?coords=' + coords,
			      function(data) {
				  neighborhood = data;
				  neighborhood_slug = data.slug;
				  $('#results').html('You are in ' + data.name);
				  
				  var wiki_url='http://en.m.wikipedia.org/wiki/' + data.wiki;
				  $('#wikilink').attr('href', wiki_url);
				  $('#yoga_link').attr('href', '/local/yoga?coords=' + coords);
				  $('#coffee_link').attr('href', '/local/coffee?coords=' + coords);
				  $('#beer_link').attr('href', '/local/beer?coords=' + coords);
				  $('#bike_link').attr('href', '/local/bikes?coords=' + coords);
				  $('#strip_link').attr('href', '/local/strip?coords=' + coords);
				  $('#pole_link').attr('href', '/local/pole?coords=' + coords);
				  $('#transit_link').attr('href', '/transit/stops?coords=' + coords);
				  
				  $('#wikilink').text('Wikipedia Entry for ' + data.name);
				  $('#neighborhood_link').text(data.name + ' Information');
				  $('#neighborhood_title').text(data.name);
				  $('#status').hide();
				  $('#results').hide();
			      });   
		});
	}
	else {
	    neighborhood="NA";
	    $('#status').hide();
	    $('#results').text("Geolocation Unvailable");
	    
	}
    }
}

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
	get_location();
	if (neighborhood == "NA") {

	    $('#yoga_link').attr('href', '#browse_by_quad');
	    $('#coffee_link').attr('href', '#browse_by_quad');
	    $('#beer_link').attr('href', '#browse_by_quad');
	    $('#bike_link').attr('href', '#browse_by_quad');
	    $('#strip_link').attr('href', '#browse_by_quad');
	    $('#pole_link').attr('href', '#browse_by_quad');
	    $('#transit_link').attr('href', '#browse_by_quad');
		};
	$('#home').
	    bind('pageAnimationEnd', function(e, info){
		    //	    alert(neighborhood.slug)
		    //$('#neighborhood_link').attr('href', '#neighborhood/');

		    }); 
	$('#neighborhood').
	    bind('pageAnimationEnd', function(e, info){
		    
		    }); 
	$('#map').
	    bind('pageAnimationEnd', function(e, info){
		    var map = new google.maps.Map2(document.getElementById("map_canvas"));
		    map.setCenter(new google.maps.LatLng(neighborhood.centroid_y, 
							 neighborhood.centroid_x), 14);
		    
		    coords=eval(neighborhood.polygon);
		    
		    var polygon = new google.maps.Polygon(coords,
							  "#f33f00", 5, 1,"#f00000", 0.2); 
		  
		    map.addOverlay(polygon);
		});


	if (neighborhood == "NA") {
	    $('#browse').attr('class', 'current');

	}

    });

  
