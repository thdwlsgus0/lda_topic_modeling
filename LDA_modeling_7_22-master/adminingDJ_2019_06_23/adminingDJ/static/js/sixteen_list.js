
    var sixteen_list =[{"keyword":"노균병","count":66},{"keyword":"방제","count":43},{"keyword":"피해","count":40}, {"keyword":"재배","count":32},{"keyword":"약","count":11},{"keyword":"수확","count":10},{"keyword":"마늘","count":67},{"keyword":"출하","count":39},{"keyword":"배추","count":36}, {"keyword":"고온","count":15},{"keyword":"기온","count":4},{"keyword":"작물","count":18},{"keyword":"밭","count":8},{"keyword":"생육","count":6}];
    var color = d3.scaleLinear()
            .domain([0,1,2,3,4,5,6,10,15,20,300])
            .range(["#FF0000", "#FF5E00", "#FFE400", "#1DDB16", "#0054FF", "#0100FF", "#5F00FF", "#FF00DD", "#FF007F", "#000000", "#4374D9", "#476600"]);

    d3.layout.cloud().size([800, 300])
            .words(sixteen_list)
            .rotate(0)
            .fontSize(function(d) { return d.count; })
            .on("end", draw)
            .start();

    function draw(words) {
        d3.select("svg.wordcloud2")
                .attr("width", 1000)
                .attr("height", 350)
                .attr("class", "wordcloud2")
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
    
   