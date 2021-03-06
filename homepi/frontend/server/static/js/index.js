var ajax_data;
var latest_value;

$(document).ready(function(e) {

	$('#phone').keyboard({
		layout: 'qwerty',
		usePreview: false,
		autoAccept: true,
		display : {
    		'bksp': 'Delete'
		}
	});

    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    Highcharts.chart('container', {
    	credits: {
    		enabled: false
    	},
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                    	var hour = (new Date).getHours();
                    	var minute = (new Date).getMinutes();
		                    $.ajax({
								type: "GET",
								url: "http://127.0.0.1:5000/data",
								cache: false,
								data: { get_param: 'value' }, 
								dataType: 'json',
								success: function (data) {
									latest_value = parseFloat(data.latest_value);
								},
								async: false
							});
	                        var x = (new Date()).getTime(), // current time
	                            y = latest_value;
	                        series.addPoint([x, y], true, true);
                    }, 30000);
                }
            },
            height: 350
        },
        title: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: ''
            },
            minorGridLineWidth: 0,
        gridLineWidth: 0,
        alternateGridColor: null,
            labels: {
            	enabled: false
            },
plotBands: [{ // Moderate breeze
            from: -1,
            to: 0.0125,
            color: 'rgba(41,182,246,0.3)',
            label: {
                text: '',
                style: {
                    color: '#606060'
                }
            }
        }, { // Light air
            from: 0.0125,
            to: 0.025,
            color: 'rgba(102,187,106, 0.3)',
            label: {
                text: '',
                style: {
                    color: '#606060'
                }
            }
        }, { // Light breeze
            from: 0.025,
            to: 0.0375,
            color: 'rgba(255,202,40, 0.3)',
            label: {
                text: '',
                style: {
                    color: '#606060'
                }
            }
        }, { // Gentle breeze
            from: 0.0375,
            to: 0.05,
            color: 'rgba(255,112,67, 0.3)',
            label: {
                text: '',
                style: {
                    color: '#606060'
                }
            }
        }, { // Moderate breeze
            from: 0.05,
            to: 1,
            color: 'rgba(239,83,80, 0.3)',
            label: {
                text: '',
                style: {
                    color: '#606060'
                }
            }
        }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + Highcharts.dateFormat('%A', this.x) + '</b><br/><b>' + Highcharts.dateFormat('%B %e', this.x) + nth(parseInt(Highcharts.dateFormat('%e', this.x))) + Highcharts.dateFormat(', %l:%M%p', this.x) + '</b>';
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                $.ajax({
					type: "GET",
					url: "http://127.0.0.1:5000/data",
					cache: false,
					data: { get_param: 'value' }, 
					dataType: 'json',
					success: function (data) {
						ajax_data = data.data;
					},
					async: false
				});

				//var now = new Date((new Date()).setMinutes(0));

				var now = new Date();

				/*
				var quarter = Math.floor((now.getHours())/6) + 1;
				if(quarter == 1)
					now = new Date(now.setHours(0));
				else if(quarter == 2)
					now = new Date(now.setHours(6));
				else if(quarter == 3)
					now = new Date(now.setHours(12));
				else if(quarter == 4)
					now = new Date(now.setHours(18));
				*/
				var x_time = now;
				
                for (i = (ajax_data.length - 1); i >= 0; i -= 1) {
                    data.push({
                        x: x_time.getTime(),
                        y: parseFloat(ajax_data[i])
                    });
                    x_time.setMinutes(x_time.getMinutes() - 1);
                }

                return data.reverse();
            }()),
            marker: { enabled: false }
        }]
    });

	update_content();
    var refresher = setInterval("update_content();", 30000);
});

function update_content(){
	update_risk();
	update_weather();
	update_date();
	update_angle();
	update_alerts();
}

function nth(d) {
  if(d>3 && d<21) return 'th';
  switch (d % 10) {
        case 1:  return "st";
        case 2:  return "nd";
        case 3:  return "rd";
        default: return "th";
    }
}

function update_date(){
	var d = new Date();
	var month = "January,February,March,April,May,June,July,August,September,October,November,December".split(",")[d.getMonth()];
	var weekday =  "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",")[d.getDay()];
	var ordinal = nth(d.getDate())

	$("#day").text(weekday + ",");
	$("#date").text(month + " " + d.getDate() + ordinal);
}

function update_risk(){
    $.ajax({
		type: "GET",
		url: "http://127.0.0.1:5000/risk",
		cache: false,
		data: { get_param: 'value' }, 
		dataType: 'json',
		success: function (data) { 
			var output_risk = data.risk;

			switch(output_risk) {
			    case "EXTREME":
			        $("#risk").attr("class","risk_value red-text text-lighten-1");
			        break;
			    case "HIGH":
			        $("#risk").attr("class","risk_value deep-orange-text text-lighten-1");
			        break;
			    case "MEDIUM":
			        $("#risk").attr("class","risk_value amber-text text-lighten-1");
			        break;
			    case "LOW":
			        $("#risk").attr("class","risk_value green-text text-lighten-1");
			        break;
			    case "MINIMAL":
			        $("#risk").attr("class","risk_value light-blue-text text-lighten-1");
			        break;
			    default:
			    	output_risk = "UNKNOWN"
			        $("#risk").attr("class","risk_value light-blue-text text-lighten-1");
			        break;
			}
			output_risk += " RISK";

			$("#risk").text(output_risk);
			$('.tooltipped').tooltip({delay: 50, tooltip: "Your tree is showing some signs of fatigue. Keep an eye on the weather, and regularly observe the limbs of your tree."});
		}
	}); 
}

function update_weather(){
    $.ajax({
		type: "GET",
		url: "http://127.0.0.1:5000/current_weather",
		cache: false,
		data: { get_param: 'value' }, 
		dataType: 'json',
		success: function (data) { 
			var output_risk = data.high + " " + data.low + " " + data.status + " " + data.wind_speed + " " + data.wind_dir ;

			switch(data.status.charAt(0)) {
			    case '2':
			        $("#status").attr("class","wi wi-thunderstorm");
			        break;
			    case '3':
			        $("#status").attr("class","wi wi-sprinkle");
			        break;
			    case '5':
			        $("#status").attr("class","wi wi-rain");
			        break;
			    case '6':
			        $("#status").attr("class","wi wi-snow");
			        break;
			    case '7':
			        $("#status").attr("class","wi wi-fog");
			        break;
			    case '8':
			    	switch(data.status){
			    		case "800":
					        var hour = (new Date).getHours();
					        var quarter = Math.floor(hour/6) + 1;

					        if((quarter == 1) || (quarter == 4))
					        {
					        	$("#status").attr("class","wi wi-night-clear");
					        }
					        else
					        {
					        	$("#status").attr("class","wi wi-day-sunny");
					        }
					        break;
					    case "801":
					        var hour = (new Date).getHours();
					        var quarter = Math.floor(hour/6) + 1;
					        
					        if((quarter == 1) || (quarter == 4))
					        {
					        	$("#status").attr("class","wi wi-night-alt-cloudy");
					        }
					        else
					        {
					        	$("#status").attr("class","wi wi-day-cloudy");
					        }
					        break;
					    default:
					        $("#status").attr("class","wi wi-cloudy");
			        		break;
			    	}
			        break;
			    default:
			        $("#status").attr("class","wi wi-na");
			        break;
			}

			switch(data.wind_dir){
				case "N":
					$("#wind_dir").attr("class","wi wi-direction-up");
					break;
				case "NE":
					$("#wind_dir").attr("class","wi wi-direction-up-right");
					break;
				case "E":
					$("#wind_dir").attr("class","wi wi-direction-right");
					break;
				case "SE":
					$("#wind_dir").attr("class","wi wi-direction-down-right");
					break;
				case "S":
					$("#wind_dir").attr("class","wi wi-direction-down");
					break;
				case "SW":
					$("#wind_dir").attr("class","wi wi-direction-down-left");
					break;
				case "W":
					$("#wind_dir").attr("class","wi wi-direction-left");
					break;
				case "NW":
					$("#wind_dir").attr("class","wi wi-direction-up-left");
					break;
			}

			$("#high").text(data.high);
			$("#low").text(data.low);
			$("#wind_speed").text(data.wind_speed);
		}
	}); 
}

function update_angle(){
    $.ajax({
		type: "GET",
		url: "http://127.0.0.1:5000/angle",
		cache: false,
		data: { get_param: 'value' }, 
		dataType: 'json',
		success: function (data) { 
			var output_angle = data.angle;
			var angle_float = parseFloat(output_angle);
			var angle_percent = (angle_float/90.0)*100.0;

			$("#angle_wrapper").html('');
			if(angle_percent >= 1.0)
			{
				var bar_color = "";
				if(angle_percent < 15.0)
				{
					bar_color = "rgb(102,187,106)";
				}
				else if(angle_percent >= 15.0 && angle_percent < 45.0)
				{
					bar_color = "rgb(255,202,40)";
				}
				else if(angle_percent >= 45.0)
				{
					bar_color = "rgb(239,83,80)";

					if(angle_percent > 90.0)
						angle_percent = 100.0;
				}
				
				$("#angle_wrapper").html('<div id="angle" class="small"></div>');
				
				$("#angle").percircle({
					text: (output_angle + "°"),
					percent: angle_percent,
					progressBarColor: bar_color
				});
			}
		}
	}); 
}

function update_alerts(){
    $.ajax({
		type: "GET",
		url: "http://127.0.0.1:5000/alerts",
		cache: false,
		data: { get_param: 'value' }, 
		dataType: 'json',
		success: function (data) { 
			var output_array = data.info;
			var output_html = "";
			if(output_array.length > 0)
			{
				for(var i = 0; i < output_array.length; i++)
				{
					var type = output_array[i].type;
					var subject = output_array[i].subject;
					var desc = output_array[i].desc;

					var style = type == "error" ? "alert" : "info";

					output_html += '<div data-id="' + i.toString() + '" class="chip tooltipped" data-position="left" data-delay="50" data-tooltip="' + desc + '">' + subject + '<i class="icon_' + style + ' material-icons">' + type + '</i></div>\n';
				}
			}

			else
				output_html = '<div style="font-size: 18px; font-weight: 300; color: #ccc;">No alerts at this time.</div>';
			$("#alert_zone").html(output_html);
			$('.tooltipped').tooltip({delay: 50});
		}
	}); 
}

function alert_click(el){
	var tooltip_id = '#' + $(el).parent().attr('data-tooltip-id');
	$(tooltip_id).remove();
	var alert_url = "http://127.0.0.1:5000/alert_response?";
	alert_url += "id=" + $(el).parent().attr("data-id");
	$.ajax({
	    type: 'POST',
	    url: alert_url,
	    success: function(msg){
	        console.log(alert_url);
	        update_alerts();
	    }
	});
}

