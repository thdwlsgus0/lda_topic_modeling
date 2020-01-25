
    
    var twelve_list=[{"keyword":"가격","count":58}, {"keyword":"가뭄","count":13},{"keyword":"배추","count":12},{"keyword":"노균병","count":33},{"keyword":"방제","count":22},{"keyword":"피해","count":12},{"keyword":"농약","count":24},{"keyword":"살포","count":13},{"keyword":"식물","count":13},{"keyword":"재배","count":33},{"keyword":"수확","count":10},{"keyword":"생산","count":9},{"keyword":"감소","count":16},{"keyword":"약제","count":7}];
    var color = d3.scaleLinear()
            .domain([0,1,2,3,4,5,6,10,15,20,300])
            .range(["#FF0000", "#FF5E00", "#FFE400", "#1DDB16", "#0054FF", "#0100FF", "#5F00FF", "#FF00DD", "#FF007F", "#000000", "#4374D9", "#476600"]);

    d3.layout.cloud().size([800, 300])
            .words(twelve_list)
            .rotate(0)
            .fontSize(function(d) { return d.count; })
            .on("end", draw)
            .start();

    function draw(words) {
        d3.select("svg.wordcloud")
                .attr("width", 1000)
                .attr("height", 350)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(320,200)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.count + "px"; })
                .style("fill", function(d, i) { return color(i); })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.keyword; });
    }
    
  