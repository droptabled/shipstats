function addBoxPlot(svg, results, x, y, width, height){
	boxplotWidth = width/40
	var div = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);
	xleft = x(results["ship_primary_median"]) - boxplotWidth/2

	// 5th and 95th percentile whiskers
	var arr = [results["ship_secondary_5th"], results["ship_secondary_95th"]];
	for(i=0; i<arr.length; i++){
		svg.append("g")
			.append("line")
			.attr("x1", xleft)
			.attr("x2", xleft + boxplotWidth)
			.attr("y1", y(arr[i]))
			.attr("y2", y(arr[i]))
			.style("stroke", "gray");
	}
	
	// 5th and 95th connection lines
	svg.append("g")
		.append("line")
		.attr("x1", x(results["ship_primary_median"]))
		.attr("x2", x(results["ship_primary_median"]))
		.attr("y1", y(results["ship_secondary_5th"]))
		.attr("y2", y(results["ship_secondary_95th"]))
		.style("stroke", "gray");
		
	// q1-q3 triangle
	svg.append("g")
		.append("rect")
		.attr("x", xleft)
		.attr("width", boxplotWidth)
		.attr("y", y(results["ship_secondary_q3"]))
		.attr("height", y(results["ship_secondary_q1"])-y(results["ship_secondary_q3"]))
		.style("fill", "none")
		.style("stroke", "gray");

	// median circle
	svg.append("g")
		.append("circle")
		.attr("cx", x(results["ship_primary_median"]))
		.attr("cy", y(results["ship_secondary_median"]))
		.attr("r", boxplotWidth/8)
		.style("fill", "gray")
		.style("stroke", "black")
		.on("mouseover", function(d) {
			div.transition()
				.duration(200)
				.style("opacity", .9);
			div.html("First Ship Win Ratio: "
				+ parseFloat(results["ship_primary_median"]).toFixed(4)
				+ "<br/>"+"Secondary Ship Win Ratio: "
				+ parseFloat(results["ship_secondary_median"]).toFixed(4)
			)
				.style("left", (d3.event.pageX) + "px")
				.style("top", (d3.event.pageY - 28) + "px");
		})
		.on("mouseout", function(d) {
			div.transition()
				.duration(500)
				.style("opacity", 0);
		});
}

function drawScatter(svg, results, x, y){
	var div = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);
	var sum_x = 0;
	var sum_y = 0;
	var sum_xx = 0;
	var sum_xy = 0;
	var count = results.length;
	var minx = 1;
	var maxx = 0;

	//calculating line of best fit
	for (i=0; i<count; i++) {
		sum_x += results[i][0];
		sum_y += results[i][1];
		sum_xx += results[i][0]*results[i][0];
		sum_xy += results[i][0]*results[i][1];
		if(results[i][0] > maxx) { maxx = results[i][0]; }
		if(results[i][0] < minx) { minx = results[i][0]; }
	}

	var m = (count*sum_xy - sum_x*sum_y) / (count*sum_xx - sum_x*sum_x);
	var b = (sum_y/count) - (m*sum_x)/count;

	//draw line of best fit
	svg.append("g")
	.append("line")
	.attr("x1", x(minx))
	.attr("x2", x(maxx))
	.attr("y1", y(minx*m + b))
	.attr("y2", y(maxx*m + b))
	.style("stroke", "red");
	
	//draw legend for line of best fit stats
	svg.append("g")
    .append("text")
	.attr("x", x(maxx)-150)
	.attr("y", y(maxx*m + b)+100)
	.attr("font-size", "15px")
	.attr("font-weight", "bold")
	.attr("fill", "red")
	.text("y = " + m.toFixed(3) + "x + " + b.toFixed(3));

	//drawing scatter plots
	for (var i=0; i<results.length; i++){
		svg.append("g")
		.append("circle")
		.attr("class", "boxplot mean")
		.attr("cx", x(results[i][0]))
		.attr("cy", y(results[i][1]))
		.attr("r", 2)
		.attr("first", results[i][0])
		.attr("second", results[i][1])
		.style("fill", "gray")
		.style("stroke", "black")
		.on("mouseover", function(d) {
			div.transition()
				.duration(200)
				.style("opacity", .9);
			div.html("First Ship Win Ratio: "+$(this).attr("first")+"<br/>"+"Secondary Ship Win Ratio: "+$(this).attr("second"))
				.style("left", (d3.event.pageX) + "px")
				.style("top", (d3.event.pageY - 28) + "px");
		})
		.on("mouseout", function(d) {
			div.transition()
				.duration(500)
				.style("opacity", 0);
		});
	}
	
	//drawing line of best fit
	
}

var padding={top:10, bottom:100, left:50, right:10};
var plottype;
$("button.generate").click(function () {
	var first = $("#ship1").val();
	var second = $("#ship2").val();
	plottype = $(this).val();
	$.ajax({
		url: '/compare_ships',
		data: {
			ship1: first,
			ship2: second,
			type: plottype
		},
		dataType: 'json',
		success: function (data) {
			//empty out the previous graph and redraw
			$("svg").remove();
			
			var height=window.innerHeight-100;
			var width=window.innerWidth-100;
			var svg = d3.select("#svgElement1").append("svg").attr("width", width).attr("height", height);

			var minx = 1;
			var maxx = 0;
			var miny = 1;
			var maxy = 0;
			var buffer = 0.01;
			if (plottype == "1"){
				for(var i=0; i<data.length; i++){
					if (data[i]["ship_primary_median"] < minx) { minx = data[i]["ship_primary_median"]; }
					if (data[i]["ship_primary_median"] > maxx) { maxx = data[i]["ship_primary_median"]; }
					if (data[i]["ship_secondary_5th"] < miny) { miny = data[i]["ship_secondary_5th"]; }
					if (data[i]["ship_secondary_95th"] > maxy) { maxy = data[i]["ship_secondary_95th"]; }
				}
			}
			if (plottype == "2"){
				jsondata = JSON.parse(data);
				for(var i=0; i<jsondata.length; i++){
					if (jsondata[i][0] < minx) { minx = jsondata[i][0]; }
					if (jsondata[i][0] > maxx) { maxx = jsondata[i][0]; }
					if (jsondata[i][1] < miny) { miny = jsondata[i][1]; }
					if (jsondata[i][1] > maxy) { maxy = jsondata[i][1]; }	
				}
			}
			var xdomain = [parseFloat(minx)-buffer, parseFloat(maxx)+buffer];
			var ydomain = [parseFloat(miny)-buffer, parseFloat(maxy)+buffer];
			
			var x = d3.scaleLinear().range([padding.left, width - padding.right]).domain(xdomain);
			var xAxis = d3.axisBottom(x).ticks(10);
			var y = d3.scaleLinear().range([height - padding.bottom, padding.top]).domain(ydomain);
			var yAxis = d3.axisLeft(y).ticks(10);
			
			//drawing the graph axes
			svg.append("g")
				.attr('class', 'axis')
				.attr("transform", "translate("+padding.left+","+"0"+")")
				.call(yAxis);

			svg.append("text")
				.attr("transform", "rotate(-90)")
				.attr("x",0 - ((height-padding.bottom+padding.top) / 2))
				.attr("dy", "1em")
				.style("text-anchor", "middle")
				.text("Second Ship Win Ratio");
				
			svg.append("g")
				.attr("class", "x axis")
				.attr("transform", "translate("+"0"+","+(height-padding.bottom)+")")
				.call(xAxis);

			svg.append("text")
				.attr("class", "label")
				.attr("x", ((width+padding.left-padding.right) / 2))
				.attr("y", (height-padding.bottom+padding.top+25)) //offsett by additional 25 to keep under the axis 
				.style("text-anchor", "middle")
				.text("First Ship Win Ratio");
			
			//plotting the data
			if (plottype == "1"){
				for(var i=0; i<data.length; i++){
					addBoxPlot(svg, data[i], x, y, width, height);
				}
			}
			else if (plottype == "2"){
				drawScatter(svg, jsondata, x, y);
			}
		}
	});
});
