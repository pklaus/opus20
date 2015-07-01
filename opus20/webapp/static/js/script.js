

$(function(){
  $('#fetchData').on('click', function(){
    var $btn = $(this);
    $btn.prop('disabled', true);
    var $text = $btn[0].textContent;
    $btn.prop('textContent', "Loading...");
    $.ajax({
      url: "/download/" + device_id,
      type: 'get',
      success: function (response) {
        //console.log('response received');
        $btn.prop('disabled', false);
        $btn.prop('textContent', $text);
        location.reload()
      }, error: function (response) {
        console.log('ajax request to fetch data failed');
        alert('ajax request to fetch data failed');
        $btn.prop('disabled', false);
        $btn.prop('textContent', $text);
      },
    });
  });
});

