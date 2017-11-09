"use strict"; // Start of use strict

// 7. google map
function gMap(lat, long, city) {
	if (lat, long) {
		lat = lat.replace(",", ".");
		long = long.replace(",", ".");
	}
	if ($('.google-map').length) {
        $('.google-map').each(function () {
        	// getting options from html
        	var mapName = $(this).attr('id');
        	var mapLat = $(this).data('map-lat');
        	var mapLng = $(this).data('map-lng');
        	var iconPath = $(this).data('icon-path');
        	var mapZoom = $(this).data('map-zoom');
        	var mapTitle = $(this).data('map-title');
        	// if zoom not defined the zoom value will be 15;
        	if (!mapZoom) {
        		var mapZoom = 15;
        	};
        	// init map
        	var map;
					if (lat && long && city) {
						map = new GMaps({
                div: '#'+mapName,
                scrollwheel: false,
                lat: lat,
                lng: long,
                zoom: mapZoom
							});
					}else {
						map = new GMaps({
								div: '#'+mapName,
								scrollwheel: false,
								lat: mapLat,
								lng: mapLng,
								zoom: mapZoom
						});
					}
            // if icon path setted then show marker
            if(iconPath && city) {
								map.addMarker({
			            	icon: iconPath,
		                lat: lat,
		                lng: long,
		                title: city
			           	});
        				}else if(iconPath) {
									map.addMarker({
				            	icon: iconPath,
			                lat: "42.679485",
			                lng: "23.332116",
			                title: "Sofia"
				           	});
        				}
        });
		};
}



// instance of fuction while Document ready event
jQuery(document).on('ready', function () {
	(function ($) {
		gMap();
	})(jQuery);
});
