var map;
var marker;
var addr_components;
$(document).ready(function(){
    map = new GMaps({
        el: '#map',
        lat: 41.03806,
        lng: 28.986648
    });
    $('#search').click(function(e){
        e.preventDefault();
        GMaps.geocode({
            address: $('#address_src').val().trim(),
            callback: function(results, status){
                if(status=='OK'){
                  var latlng = results[0].geometry.location;
                  map.setCenter(latlng.lat(), latlng.lng());
                  map.addMarker({
                    lat: latlng.lat(),
                    lng: latlng.lng()
                  });
                }
            }
        });
    });

    $('#address_src').keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            GMaps.geocode({
                address: $('#address_src').val().trim(),
                callback: function(results, status){
                    if(status=='OK'){
                      var latlng = results[0].geometry.location;
                      map.setCenter(latlng.lat(), latlng.lng());
                      map.addMarker({
                        lat: latlng.lat(),
                        lng: latlng.lng()
                      });
                    }
                }
            });
        }
    });

    map.setContextMenu({
        control: 'map',
        options: [{
            title: 'Adres Olarak Seç',
            name: 'add_marker_set_address',
            action: function(e) {
                this.removeMarkers();
                var adrStr='';
                GMaps.geocode({
                  lat:e.latLng.lat(),
                  lng:e.latLng.lng(),
                  callback: function(results, status){
                    if(status=='OK'){
                        addr_components = results[0].address_components;
                        console.log(addr_components);
                        adrStr = parseAddress(results[0].addr_components);
                        $('#address').val(adrStr);
                        $('#lat').val(e.latLng.lat());
                        $('#lng').val(e.latLng.lng());
                        map.addMarker({
                            lat: e.latLng.lat(),
                            lng: e.latLng.lng(),
                            title: 'My Address',
                            infoWindow: {
                              content: '<p>'+adrStr+'</p>'
                            }
                          });
                    }
                  }
                });
            }
        }]
    });
});

function parseAddress(address_components){
    var address_str = '';
    addr_components.forEach(function(item){

        item.types.forEach(function(type){
            if(checkType(type)){
                console.log(item.long_name+" "+type);
                address_str += item.long_name+" ";
            }
        });
    });
    return address_str;
}

function checkType(type){
    var result;
    switch(type){
        case 'neighborhood':
            result = true;
            break;
        case 'route':
            result = true;
            break;
        case 'sublocality':
            result = true;
            break;
        case 'locality':
            result = true;
            break;
        default:
            result=false;
            break;
    }
    return result;
}