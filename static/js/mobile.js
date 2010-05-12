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
	$('#swipeme').swipe(function(evt, data) {                
		$(this).html('You swiped <strong>' + data.direction + '</strong>!');
	    });
	$('a[target="_blank"]').click(function() {
		if (confirm('This link opens in a new window.')) {
		    return true;
		} else {
		    $(this).removeClass('active');
		    return false;
		}
	    });
	// Page animation callback events
	$('#home').
	    bind('pageAnimationEnd', function(e, info){
		    $('#neighborhood_link').attr('href', '/neighborhood/' + neighborhood_slug);
		});
	
	
    });

  
var neighborhood = "unknown";
if (neighborhood == "unknown") {
    if (navigator.geolocation) {  
	navigator.geolocation.getCurrentPosition(function(position) {  
		
		$.getJSON('/lookup?coords=' + position.coords.longitude + '%2C' + position.coords.latitude, 
			  function(data) {
			      neighborhood = data.name;
			      neighborhood_slug = data.slug;
			      $('#results').html('You are in ' + data.name);
			      $('#neighborhood_link').attr('href', '/neighborhood/' + data.slug);
			      $('#status').hide();
			  });   
	    });
    }
    else {
	$('#results').html('Neighborhood (Location Unavailable)');
    }
}