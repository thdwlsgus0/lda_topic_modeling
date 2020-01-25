$(function() {
  'use strict';

  $('input.btn-icheck').each(function() {
    var self = $(this);
    const label = self.next();
    const label_text = label.text();
    label.remove();

    self.iCheck({
      checkboxClass: 'icheckbox_line-green',
      radioClass: 'iradio_line-green',
      insert: '<div class="icheck_line-icon"></div>' + label_text
    });
  });

  if ($('#calendar').length) {
    //Date for the calendar events (dummy data)
    var date = new Date();
    var d = date.getDate(),
      m = date.getMonth(),
      y = date.getFullYear();
    $('#calendar').fullCalendar({
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay'
      },
      buttonText: {
        today: 'today',
        month: 'month',
        week: 'week',
        day: 'day'
      },
      //Random default events
      events: [
        {
          title:
            'International Symposium on Flower Bulbs and Herbaceous Perennials (ISFBHP)',
          start: new Date(y, m, 1),
          backgroundColor: '#f56954', //red
          borderColor: '#f56954' //red
        },
        {
          title:
            'International Conference on Food and Agricultural Engineering (ICFAE)',
          start: new Date(y, m, 18),
          end: new Date(y, m, 20),
          backgroundColor: '#f39c12', //yellow
          borderColor: '#f39c12' //yellow
        },
        {
          title:
            'International Conference on Food and Agricultural Engineering (ICFAE)',
          start: new Date(y, m, 14),
          allDay: false,
          backgroundColor: '#0073b7', //Blue
          borderColor: '#0073b7' //Blue
        },
        {
          title: 'Organic & Natural Trade Fair',
          start: new Date(y, m, d, 12, 0),
          end: new Date(y, m, d, 14, 0),
          allDay: false,
          backgroundColor: '#00c0ef', //Info (aqua)
          borderColor: '#00c0ef' //Info (aqua)
        },
        {
          title: 'Seoul Fermented Food & Culture Show',
          start: new Date(y, m, d + 1, 19, 0),
          end: new Date(y, m, d + 1, 22, 30),
          allDay: true,
          backgroundColor: '#00a65a', //Success (green)
          borderColor: '#00a65a' //Success (green)
        }
      ],
      editable: true,
      droppable: true, // this allows things to be dropped onto the calendar !!!
      drop: function(date, allDay) {
        // this function is called when something is dropped

        // retrieve the dropped element's stored Event Object
        var originalEventObject = $(this).data('eventObject');

        // we need to copy it, so that multiple events don't have a reference to the same object
        var copiedEventObject = $.extend({}, originalEventObject);

        // assign it the date that was reported
        copiedEventObject.start = date;
        copiedEventObject.allDay = allDay;
        copiedEventObject.backgroundColor = $(this).css('background-color');
        copiedEventObject.borderColor = $(this).css('border-color');

        // render the event on the calendar
        // the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
        $('#calendar').fullCalendar('renderEvent', copiedEventObject, true);

        // is the "remove after drop" checkbox checked?
        if ($('#drop-remove').is(':checked')) {
          // if so, remove the element from the "Draggable Events" list
          $(this).remove();
        }
      }
    });

    /* ADDING EVENTS */
    var currColor = '#3c8dbc'; //Red by default
    //Color chooser button
    var colorChooser = $('#color-chooser-btn');
    $('#color-chooser > li > a').click(function(e) {
      e.preventDefault();
      //Save color
      currColor = $(this).css('color');
      //Add color effect to button
      $('#add-new-event').css({
        'background-color': currColor,
        'border-color': currColor
      });
    });
    $('#add-new-event').click(function(e) {
      e.preventDefault();
      //Get value and make sure it is not null
      var val = $('#new-event').val();
      if (val.length == 0) {
        return;
      }

      //Create events
      var event = $('<div />');
      event
        .css({
          'background-color': currColor,
          'border-color': currColor,
          color: '#fff'
        })
        .addClass('external-event');
      event.html(val);
      $('#external-events').prepend(event);

      //Add draggable funtionality
      init_events(event);

      //Remove event from text input
      $('#new-event').val('');
    });
  }

  if ($('#nav-left').length) {
    $('#nav-left').affix({
      offset: {
        top: $('#nav-left').offset().top,
        bottom:
          $('footer').outerHeight(true) +
          $('.application').outerHeight(true) +
          40
      }
    });
  }

  if ($('.input-daterange input').length) {
    $('.input-daterange input').each(function() {
      $(this).datepicker({
        clearDates: true,
        autoclose: true,
        format: 'yyyy-m-d',
        viewMode: '',
        minViewMode: ''
      });
    });
  }

  if ($('input#id_term').length) {
    $('input#id_term').daterangepicker({
      locale: {
        format: 'Y-MM-D'
      }
    });
  }

  if ($('.icheck').length) {
    $('input').iCheck({
      checkboxClass: 'icheckbox_square-green',
      radioClass: 'iradio_square-green',
      increaseArea: '20%' // optional
    });
  }

  $('#cats').on('change', function() {
    const selected = 'cat' + $(this).val();
    $('#subcats option').each(function(item) {
      if ($(this).attr('parent') === selected) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });

    $('#subcats').val($('#subcats option:visible:first').val());
  });
});
