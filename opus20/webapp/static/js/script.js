

$(function(){
  $('#fetchData').on('click', function(){
    var $btn = $(this).button('loading')
    $.ajax({
      url: "/download/" + device_id,
      type: 'get',
      success: function (response) {
        //console.log('response received');
        location.reload()
        $btn.button('reset')
      }, error: function (response) {
        console.log('ajax request to fetch data failed');
        alert('ajax request to fetch data failed');
        $btn.button('reset')
      },
    });
  });
});

