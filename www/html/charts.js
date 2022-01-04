google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

	var data1 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['EC Level', 0],
        ]);
	
	var data2 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Light', 0],
        ]);
	
	var data3 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Air Tem.', 0],
        ]);
	
	var data4 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['PH', 0],
        ]);
	
	
	var data5 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Humidity', 0],
        ]);
	
	var data6 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Water T.', 0],
        ]);
	
	var data7 = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Water L', 0],
        ]);	
	

	var options1 = {
          width: 200, height: 200,
	  min: 0, max: 4,	  
	  redColor: "#ff9900",
	  redFrom: 0.5, redTo: 0.75,  
	  greenFrom: 0.75, greenTo: 2,
	  yellowFrom: 2, yellowTo: 3,
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOut',
	  },
	  majorTicks : ['0','1','2','3','4']
        };
	
	var options2 = {
          width: 200, height: 200,
	  min: 0, max: 30,	  
	  redColor: "#ff9900",
	  redFrom: 2.5, redTo: 5,  
	  greenFrom: 5, greenTo: 30,
	  //yellowFrom: 600, yellowTo: 700,
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOut',
	  },
	  majorTicks : ['0','5','10','15', '20', '25', '30']
        };
		
	var options3 = {
          width: 200, height: 200,
	  min: 10, max: 40,	  
	  redColor: "#ff9900",
	  redFrom: 15, redTo: 18,  
	  greenFrom: 18, greenTo: 27,
	  yellowFrom: 27, yellowTo: 35,
          minorTicks: 10,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOutama',
	  },
	  majorTicks : ['10','20','30','40']
        };
	
        var options4 = {
          width: 200, height: 200,
	  min: 3, max: 9,	  
	  redColor: "#ff9900",
	  redFrom: 4.5, redTo: 5.0,  
	  greenFrom: 5.0, greenTo: 6,
	  yellowFrom: 6, yellowTo: 6.5,
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOutama',
	  },
	  majorTicks : ['3','4','5','6','7','8','9']
        };
	
	
	
	var options5 = {
          width: 135, height: 135,
	  min: 0, max: 100,
	  redColor: "#ff9900",
	  yellowFrom:75, yellowTo: 90,
	  greenFrom: 35, greenTo: 75,
          redFrom: 20, redTo: 35,          
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOut',
	  },
	  majorTicks : ['0','10','20','30','40','50','60','70','80','90','100']
        };
	
	var options6 = {
          width: 135, height: 135,
	  min: 0, max: 40,	  
	  redColor: "#ff9900",
	  redFrom: 15, redTo: 18,  
	  greenFrom: 18, greenTo: 27,
	  yellowFrom: 27, yellowTo: 40,
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOutama',
	  },
	  majorTicks : ['0', '10','20','30','40']
        };
	
	var options7 = {
          width: 135, height: 135,
	  min: 0, max: 100,	  
	  redColor: "#ff9900",
	  redFrom: 30, redTo: 40,  
	  greenFrom: 40, greenTo: 60,
	  yellowFrom: 60, yellowTo: 70,
          minorTicks: 5,
	  animation:{
	    duration: 1000,
	    easing: 'inAndOut',
	  },
	  majorTicks : ['0','20','40','60', '80', '100']
        };


	var chart1 = new google.visualization.Gauge(document.getElementById('chart1'));
	var chart2 = new google.visualization.Gauge(document.getElementById('chart2'));
	var chart3 = new google.visualization.Gauge(document.getElementById('chart3'));
	var chart4 = new google.visualization.Gauge(document.getElementById('chart4'));
	
	var chart5 = new google.visualization.Gauge(document.getElementById('chart5'));
	var chart6 = new google.visualization.Gauge(document.getElementById('chart6'));
	var chart7 = new google.visualization.Gauge(document.getElementById('chart7'));	

	chart1.draw(data1, options1);
	chart2.draw(data2, options2);
	chart3.draw(data3, options3);
	chart4.draw(data4, options4);
	
	chart5.draw(data5, options5);
	chart6.draw(data6, options6);
	chart7.draw(data7, options7);	
		

	setInterval(function() {
	  
	  if(sensorData.ecLevel == 100) {
	    data1.setValue(0, 1, Math.round(0));
	  }
	  
	  else {
	    data1.setValue(0, 1, ( Math.round(sensorData.ecLevel * 10) / 10) );
	  }
	  
          chart1.draw(data1, options1);
        }, 1000);
        
	setInterval(function() {
	      lightDisplayValue = sensorData.lightIntensity/1000
		  lightDisplayValue = Math.round(lightDisplayValue)
	  
          data2.setValue(0, 1, lightDisplayValue);
          chart2.draw(data2, options2);
        }, 1000);
	
	setInterval(function() {
          data3.setValue(0, 1, Math.round(sensorData.temperature));
          chart3.draw(data3, options3);
        }, 1000);
	
	setInterval(function() {
          data4.setValue(0, 1, Math.round(sensorData.phLevel));
          chart4.draw(data4, options4);
        }, 1000);
	
	
	setInterval(function() {
          data5.setValue(0, 1, Math.round(sensorData.humidity));
          chart5.draw(data5, options5);
        }, 1000);
	
	setInterval(function() {
          data6.setValue(0, 1, Math.round(sensorData.waterTemperature));
          chart6.draw(data6, options6);
        }, 1000);
	
	setInterval(function() {
          data7.setValue(0, 1, Math.round(sensorData.waterLevel));
          chart7.draw(data7, options7);
        }, 1000);
					
        
      }
      
