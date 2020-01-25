$(function() {
  'use strict';

  if ($('#formAgriFoodTrend').length) {
    var waitingAjax = false;
    var $graphArea = $('#graphArea');
    var $alert = $graphArea.find('.alert-danger');
    var $chart = $graphArea.find('.chart');

    $('#formAgriFoodTrend').on('submit', function(e) {
      e.preventDefault();
      const form = $(this);
      const url = form.attr('action');

      if (!waitingAjax) {
        $.ajax({
          url: url,
          method: 'POST',
          dataType: 'html',
          data: form.serialize(),
          beforeSend: function() {
            waitingAjax = true;
            $alert.text('');
            $alert.hide();
            $chart.empty();
          },
          success: function(data) {
            $chart.append(data);
          },
          error: function(err) {
            $alert.text(err.responseText);
            $alert.show();
          },
          complete: function() {
            waitingAjax = false;
            $graphArea.show();
          }
        });
      }
    });
  }
});
