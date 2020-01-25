$(document).ready(function() {
  $.ajax({
    url: url,
    method: 'POST',
    dataType: 'json',
    data: form.serialize(),
    beforeSend: function() {
      waitingAjax = true;

      $alert.text('');
      $alert.hide();
      $chart.hide();
    },
    success: function(data) {
      var labels = [];
      var pSum = [];

      data.forEach(function(dt, ndx) {
        var label = dt.year;
        if (dt.week != undefined) {
          label = dt.week + '/' + label;
        } else if (dt.month != undefined) {
          label += '-' + dt.month;
          if (dt.day != undefined) {
            label += '-' + dt.day;
          }
        }

        const sm =
          parseInt(dt.news_freq__sum) +
          parseInt(dt.news_freq__sum) +
          parseInt(dt.news_freq__sum);
        if (ndx <= 10) {
          labels.push(label);

          pSum.push(sm);

          if (ndx == 10) {
            chartData.labels = labels;
            chartData.datasets[0].data = pSum;

            window.myMixedChart2.data = chartData;
            window.myMixedChart2.update();
          }
        } else {
          window.myMixedChart2.data.datasets[0].data.push(sm);
          window.myMixedChart2.data.labels.push(label);
          var newwidth = $('#canvas').width() + 60;
          $('.canvas').width(newwidth);
        }
      });

      $chart.show();
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

  function generateLabels() {
    var chartLabels = [];
    for (x = 0; x < 100; x++) {
      chartLabels.push('Label' + x);
    }
    return chartLabels;
  }

  function generateData() {
    var chartData = [];
    for (x = 0; x < 100; x++) {
      chartData.push(Math.floor(Math.random() * 100 + 1));
    }
    return chartData;
  }

  function addData(numData, chart) {
    for (var i = 0; i < numData; i++) {
      chart.data.datasets[0].data.push(Math.random() * 100);
      chart.data.labels.push('Label' + i);
      var newwidth = $('.chartAreaWrapper2').width() + 60;
      $('.chartAreaWrapper2').width(newwidth);
    }
  }

  var chartData = {
    labels: generateLabels(),
    datasets: [
      {
        label: 'Test Data Set',
        data: generateData()
      }
    ]
  };

  $(function() {
    var rectangleSet = false;

    var canvasTest = $('#chart-Test');
    var chartTest = new Chart(canvasTest, {
      type: 'bar',
      data: chartData,
      maintainAspectRatio: false,
      responsive: true,
      options: {
        tooltips: {
          titleFontSize: 0,
          titleMarginBottom: 0,
          bodyFontSize: 12
        },
        legend: {
          display: false
        },
        scales: {
          xAxes: [
            {
              ticks: {
                fontSize: 12,
                display: false
              }
            }
          ],
          yAxes: [
            {
              ticks: {
                fontSize: 12,
                beginAtZero: true
              }
            }
          ]
        },
        animation: {
          onComplete: function() {
            if (!rectangleSet) {
              var scale = window.devicePixelRatio;

              var sourceCanvas = chartTest.chart.canvas;
              var copyWidth = chartTest.scales['y-axis-0'].width - 10;
              var copyHeight =
                chartTest.scales['y-axis-0'].height +
                chartTest.scales['y-axis-0'].top +
                10;

              var targetCtx = document
                .getElementById('axis-Test')
                .getContext('2d');

              targetCtx.scale(scale, scale);
              targetCtx.canvas.width = copyWidth * scale;
              targetCtx.canvas.height = copyHeight * scale;

              targetCtx.canvas.style.width = `${copyWidth}px`;
              targetCtx.canvas.style.height = `${copyHeight}px`;
              targetCtx.drawImage(
                sourceCanvas,
                0,
                0,
                copyWidth * scale,
                copyHeight * scale,
                0,
                0,
                copyWidth * scale,
                copyHeight * scale
              );

              var sourceCtx = sourceCanvas.getContext('2d');

              // Normalize coordinate system to use css pixels.

              sourceCtx.clearRect(0, 0, copyWidth * scale, copyHeight * scale);
              rectangleSet = true;
            }
          },
          onProgress: function() {
            if (rectangleSet === true) {
              var copyWidth = chartTest.scales['y-axis-0'].width;
              var copyHeight = chartTest.scales['y-axis-0'].height;

              var sourceCtx = chartTest.chart.canvas.getContext('2d');
              sourceCtx.clearRect(0, 0, copyWidth, copyHeight);
            }
          }
        }
      }
    });
    addData(5, chartTest);
  });
});
