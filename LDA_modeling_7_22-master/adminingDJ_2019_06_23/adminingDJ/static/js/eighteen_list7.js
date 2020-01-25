
    var eighteen_list = [{"keyword":"양파","count":50}, {"keyword":"피해", "count":41}, {"keyword":"생산","count":39}, {"keyword":"재배","count":38}, {"keyword":"농민", "count":37},{"keyword":"가격","count":36},{"keyword":"마름","count":34},{"keyword":"노균병","count":31},{"keyword":"농가","count":31},{"keyword":"마늘","count":28}, 
    {"keyword":"확산","count":24}, {"keyword":"병해","count":22}, {"keyword":"면적","count":19},{"keyword":"방제","count":17},{"keyword":"재해","count":16},{"keyword":"무안","count":14},{"keyword":"비","count":24},{"keyword":"수확","count":23},{"keyword":"자연재해","count":20}
, {"keyword":"고온","count":29},{"keyword":"생산량","count":28},{"keyword":"생육","count":25},{"keyword":"하락","count":24},{"keyword":"월동","count":23},{"keyword":"보험","count":22},{"keyword":"경북","count":21},{"keyword":"폭락","count":20},
 {"keyword":"가뭄","count":20},{"keyword":"조생종","count":20},{"keyword":"비료","count":20},{"keyword":"주산지","count":20},{"keyword":"농작물","count":20},{"keyword":"출하","count":20},{"keyword":"강우","count":20},{"keyword":"감염","count":20},{"keyword":"시장","count":20}];
    var color = d3.scaleLinear()
            .domain([0,1,2,3,4,5,6,10,15,20,30,40,50,60,70,80,90,100,300])
            .range(["#FF0000", "#FF5E00", "#FFE400", "#1DDB16", "#0054FF", "#0100FF", "#5F00FF", "#FF00DD", "#FF007F", "#000000", "#4374D9", "#476600","#FF0000", "#FF5E00", "#FFE400", "#1DDB16", "#0054FF", "#0100FF", "#5F00FF", "#FF00DD", "#FF007F", "#000000", "#4374D9", "#476600"]);

    d3.layout.cloud().size([400, 300])
            .words(eighteen_list)
            .rotate(0)
            .fontSize(function(d) { return d.count; })
            .on("end", draw)
            .start();

    function draw(words) {
        d3.select("svg.wordcloud3")
                .attr("width", 800)
                .attr("height", 350)
                .attr("class", "wordcloud3")
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
    

    