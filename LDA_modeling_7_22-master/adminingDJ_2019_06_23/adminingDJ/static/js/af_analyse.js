$(function() {
  'use strict';

  $(document).ready(function() {
    if ($('#formAgriFoodAnalyse').length) {
      var waitingAjax = false;
      var $graphArea = $('#graphArea');
      var $alert = $graphArea.find('.alert-danger');
      var $charts = $graphArea.find('.charts');

      var $alert2 = $('#formAgriFoodAnalyse').find('.alert-warning');
      var $alertMessage = $alert2.find('.message');

      $('#formAgriFoodAnalyse').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);

        const url = form.attr('action');

        const timeFreq = form.find('#timeFreq').val();
        const drStart = form.find('#drStart').val();
        const drEnd = form.find('#drEnd').val();

        const checkTime = checkTimeFreq(timeFreq, drStart, drEnd);
        if (checkTime !== 0) {
          $charts.empty();
          $alertMessage.text(checkTime);
          $alert2.show();

          return false;
        }

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
              $alert2.hide();
              $charts.empty();
            },
            success: function(data) {
              $charts.append(data);
            },
            error: function(err) {
              $alert.text(err.responseText);
              $alert.show();
            },
            complete: function() {
              $graphArea.show();
              setTimeout(function() {
                waitingAjax = false;
              }, 2000);
            }
          });
        }
      });
    }

    $('input.mediaOpt').on('ifClicked', function() {
      const _this = $(this);
      const checked = _this.prop('checked');

      const added = checked ? -1 : 1;
      var countChecked = $('input.mediaOpt:checked').length + added;

      $('input.mediaAll').iCheck(countChecked == 5 ? 'check' : 'uncheck');
    });

    $('input.mediaAll').on('ifClicked', function() {
      const _this = $(this);
      const checked = _this.prop('checked');
      $('input.media').iCheck(checked ? 'uncheck' : 'check');
    });

    function checkTimeFreq(timeFreq, drStart, drEnd) {
      var dt1 = new Date(drStart);
      var dt2 = new Date(drEnd);

      if (timeFreq === 'daily') {
        var diff = Math.floor(
          (Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) -
            Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate())) /
            (1000 * 60 * 60 * 24)
        );
        if (diff <= 200) {
          return 0;
        }
        return 'Select 6 months period.';
      }

      if (timeFreq === 'monthly') {
        var diff = Math.abs(
          Math.round(
            (dt2.getTime() - dt1.getTime()) / 1000 / (60 * 60 * 24 * 7 * 4)
          )
        );
        if (diff <= 200) {
          return 0;
        }
        return 'Select 16 years period.';
      }

      if (timeFreq === 'yearly') {
        var diff = Math.abs(
          Math.round(
            (dt2.getTime() - dt1.getTime()) / 1000 / (60 * 60 * 24) / 365.25
          )
        );
        if (diff <= 200) {
          return 0;
        }
        return 'Select 200 years period.';
      }

      if (timeFreq === 'weekly') {
        var diff = Math.abs(
          Math.round(
            (dt2.getTime() - dt1.getTime()) / 1000 / (60 * 60 * 24 * 7)
          )
        );
        if (diff <= 200) {
          return 0;
        }
        return 'Select 4 years period.';
      }
    }
  });
});
