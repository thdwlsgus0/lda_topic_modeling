$(function() {
  'use strict';

  var waitingAjax = false;
  $('#feedbackForm').on('submit', function(e) {
    const _this = $(this);
    const $respMessage = _this.find('.respMessage');
    const url = _this.attr('action');

    $.ajax({
      url: url,
      method: 'POST',
      dataType: 'JSON',
      data: _this.serialize(),
      beforeSend: function() {
        waitingAjax = true;
        $respMessage.empty();
      },
      success: function(data) {
        $respMessage.append('<p class="text-success">' + data.message + '</p>');
      },
      error: function(err) {
        const data = err.responseJSON;
        $respMessage.append('<p class="text-danger">' + data.message + '</p>');
      },
      complete: function() {
        waitingAjax = false;
      }
    });

    e.preventDefault();
  });
});
