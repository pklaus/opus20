

$(function(){
  $('#fetchData').on('click', function(){
    //console.log('trying to fetch data...');
    $.ajax({
      url: "/download/" + device_id,
      type: 'get',
      success: function (response) {
        //console.log('response received');
        location.reload()
        // ajax success callback
      }, error: function (response) {
        console.log('ajax request to fetch data failed');
        alert('ajax request to fetch data failed');
        // ajax error callback
      },
    });
  });
});

