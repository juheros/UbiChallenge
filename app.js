    google.maps.visualRefresh = true;
    
    var map;
    var markers = [];
    var icon_green = 'img/icon_green.png';
    var icon_red = 'img/icon_red.png';
    var icon_yellow =  'img/icon_yellow.png';

    function initialize() {
      var mapOptions = {
        zoom:15
      };

      map = new google.maps.Map(document.getElementById('map-canvas'),
          mapOptions);
       var latlng = new google.maps.LatLng(4.814789,-75.707603);
      map.setCenter(latlng);
    }


    function LimpiarMarcadores() {
      for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(null);
      }
      markers= [];
    }

    function getIcono(pasajeros){
      if (pasajeros < 10 ){
        return icon_green;
      }
      if (pasajeros >= 10 && pasajeros <= 30 ){
        return icon_yellow;
      }
      if (pasajeros > 30 ){
        return icon_red;
      }
    }

    function dibujarVehiculo(variable_id){

    
      LimpiarMarcadores();

            
      $.ajax({  type: "GET",
                dataType: "json",
                url : "http://things.ubidots.com/api/v1.6/variables/"+variable_id+"/values?page_size=1&page=1",
                headers: {
                    'X-Auth-Token' : 'vUOiTKHogWDlj7fjUgZLfG1KSA0WVuK941zLEHQg7LNkLeoQlwPwfJ5hgRNI'
                },
                 success: function(data){

                    var latlng = new google.maps.LatLng( data.results[0].context["latitud"], data.results[0].context["longitud"]);
                    var marker = new google.maps.Marker({
                    position: latlng,
                    map:map,
                    title:  "Nivel de gasolina: "+data.results[0].value + "%",
                    cursor: 'default',
                    icon: getIcono(data.results[0].context["pasajeros"]),
                    draggable: false
                    });
                    var popup = new google.maps.InfoWindow({
                      content: 'Gasolina: ' +  data.results[0].value +'% <br />  Pasajeros: ' +  data.results[0].context["pasajeros"]
                    });
             
                    popup.open(map, marker);
                    //limits.extend(latlng);
                    
                    markers.push(marker);
                    //$('#gasolina').append('El nivel actual de gasolina es: ' + data.results[0].value + '%<br />');
                    
                    
                    
                 }
             });

    }

    function main(){
      $.ajax({  type: "GET",
                dataType: "json",
                url : "http://things.ubidots.com/api/v1.6/datasources/52d95910f91b2813517c8d00/variables",
                headers: {
                    'X-Auth-Token' : 'vUOiTKHogWDlj7fjUgZLfG1KSA0WVuK941zLEHQg7LNkLeoQlwPwfJ5hgRNI'
                },
                 success: function(data){
                    for (var i = 0; i < data.results.length; i++){
                      dibujarVehiculo(data.results[i].id);
                    }
                    
                    
                 }
                 
              });
      setTimeout('main()', 5000);
    }
    initialize();
    main();