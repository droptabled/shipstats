var width = window.innerWidth;
var height = window.innerHeight-50;
var max_circle_size = 30;
var max_line_thickness = 15;
var max_length = height/1.75;
var svg = d3.select("svg").attr("width", width).attr("height", height);
var g = d3.select("g")

var force = d3.forceSimulation() 
	.force("center", d3.forceCenter(width / 2, height / 2))
	.force("collision", d3.forceCollide(function(d) { return d.relative_size*max_circle_size }))
	.force("link",
		d3.forceLink()
		.id(function(d) { return d.index })
		.distance(function(d) { return (1.3-d.relative_strength)*max_length }) //extra buffer so closest relation is not 0 lengthed
	);
	
function dragstarted(d) {
	if (!d3.event.active) force.alphaTarget(0.5).restart();
	d.fx = d.x;
	d.fy = d.y;
}

function dragged(d) {
	d.fx = d3.event.x;
	d.fy = d3.event.y;
}

function dragended(d) {
	if (!d3.event.active) force.alphaTarget(0.5);
	d.fx = null;
	d.fy = null;
}

$("#Submit").click(function(){
	$("#canvas").empty();
	$.ajax({
		url: 'graphdata',
		data: {
			type: $('.typevalue:checked').map(function(){ return this.value }).get().join(","),
			nation: $('.nationvalue:checked').map(function(){ return this.value }).get().join(","),
			tier: $('.tiervalue:checked').map(function(){ return this.value }).get().join(","),
			premium: $("#premium").val()
		},
		dataType: 'json',
		success: function (json) {
			force.nodes(json.nodes).force("link").links(json.edges);

			var link = g.selectAll(".link").data(json.edges).enter().append("line")
				.attr("stroke-width", function (d) { return Math.max(d.relative_strength*max_line_thickness, 1); })
				.attr("stroke", function(d) { return "rgb(0,"+d.relative_strength*255+",0)"; });

			var node = g.selectAll(".node")
				.data(json.nodes)
				.enter().append("g")
				.attr("class", "node")
				.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended));  

			node.append('circle')
				.attr('r', function (d) { return d.relative_size*max_circle_size; })
				.attr('fill', function (d) { return "url('#" + d.nation + "')"; });

			node.append("text")
				.attr("dx", function(d) { return -1*d.name.length*4 })
				.attr("dy", function(d) { return d.relative_size*max_circle_size + 10; })
				.attr("filter", "url(#bgwhite)")
				.style("font-family", "Arial")
				.style("font-size", "15px")
				.text(function (d) {
					return d.name
				});

			force.on("tick", function () {
				link.attr("x1", function (d) { return d.source.x; })
					.attr("y1", function (d) { return d.source.y; })
					.attr("x2", function (d) { return d.target.x; })
					.attr("y2", function (d) { return d.target.y; });
				node.attr("transform", function (d) {
					return "translate(" + d.x + "," + d.y + ")";
				});
			});
		}
	});
});
