var pageCounter    = 1;
var btn            = document.getElementById("menu");
var chartContainer = document.getElementById("scrolling-thing");
var back_to_start  = document.getElementById("mybutton");
var end_of_page    = document.getElementById("end"); 
var back           = document.getElementById("back"); 
var next           = document.getElementById("next"); 
var timeframe_label= document.getElementById("timeframe_label"); 
var trends_label   = document.getElementById("trends_label"); 
var fundamental    = document.getElementById("fundamental"); 
var elliot         = document.getElementById("elliot"); 
var zoom           = document.getElementById("zoom"); 
var simulation     = document.getElementById("simulation"); 
var level_line     = document.getElementById("level_line"); 
var inverse        = document.getElementById("inverse"); 
var candlesticks_label   = document.getElementById("candlesticks_label");
var underline      = [];
var trend          = [];
var left           = 0;
var right          = 0;
var parity         = 0;
var base           = 0;
var quote          = 0;
var timeframe      = 0;
var meta           = false;
var sim            = false;
var visibility     = [];
var inputs         = document.getElementsByClassName("parity");
var parities       = {'eurusd':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'audchf':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'audusd':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'chfjpy':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'gbpusd':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'usdjpy':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                      'usdcad':{'1': [], '5': [], '15': [], '30': [], '60': [], '240': [], '1440': [], '10080': [], '43200': []},
                     };
var data_types     = {'spinning_top':'red', 'doji':'black', 'long_legged_doji':'#093b09', 'dragonfly_doji':'pink', 'gravestone_doji':'orange', 'marubozu':'purple', 'hammer':'grey', 'hanging_man':'gold', 'inverted_hammer':'#964B00', 'shooting_star':'#264348'}; 

back_to_start.addEventListener("click", function(){
    // window.scrollTo(0,0);
    left  = 0;
    right = 99;
    renderHTML(parities[parity], base, quote, timeframe, meta);
});

end_of_page.addEventListener("click", function(){
    // window.scrollTo(20000, 20000);

});

back.addEventListener("click", function(){
    
    if(left != 0){
      left  = left  - 50;
      right = right - 50;
      renderHTML(parities[parity], base, quote, timeframe, meta);
    }
    
});

next.addEventListener("click", function(){

    //check visiblity of charts
    left  = left + 50;
    right = right + 50;

    renderHTML(parities[parity], base, quote, timeframe, meta);

});

$(document).ready(function () {
$('#nav li').first().addClass("active").find('ul').show();
$('#nav > li > a').click(function(){
  if ($(this).attr('class') != 'active'){
    $('#nav li ul').slideUp();
    $(this).next().slideToggle();
    $('#nav li a').removeClass('active');
    $(this).addClass('active');
  }
});
});


$(document).ready(function(){
      build_parity();
});

function request_data(base, quote, timeframe){
  
    var ourRequest = new XMLHttpRequest();  
    
    ourRequest.open('GET', 'http://ec2-18-219-165-101.us-east-2.compute.amazonaws.com:5000/all_data?base=' + base + '&quote=' + quote + '&timeframe=' + timeframe, true);
    // link: ec2-18-219-165-101.us-east-2.compute.amazonaws.com
    ourRequest.onload = function() {
      console.log('Loading...');
    if (ourRequest.status >= 200 && ourRequest.status < 400) {
      var ourData = JSON.parse(ourRequest.responseText);
      parities[base + quote][timeframe] = ourData;
      } else {
        console.log("We connected to the server, but it returned an error.", ourRequest.status);
      }
    };
    ourRequest.onerror = function() {
      console.log("Connection error");
    };
    ourRequest.send(null);
}

function get_coordinates(base, quote, timeframe, candle_index){

    var ourRequest = new XMLHttpRequest();  
    
    ourRequest.open('GET', 'http://localhost:5000/coordinates/' + trend +'?base=' + base + '&quote=' + quote + '&timeframe=' + timeframe + 
      '&candle_index=' + candle_index, true);
    // link: ec2-18-219-165-101.us-east-2.compute.amazonaws.com
    ourRequest.onload = function() {
      console.log('Trend...');
    if (ourRequest.status >= 200 && ourRequest.status < 400) {
      var ourData = JSON.parse(ourRequest.responseText);
      var t = ourData;
      console.log("Asd");
      } else {
        console.log("We connected to the server, but it returned an error.", ourRequest.status);
      }
    };
    ourRequest.onerror = function() {
      console.log("Connection error");
    };
    ourRequest.send(null);
}

function build_parity(){

    for(parity in parities){

      var base       = parity.substr(0, 3);
      var quote      = parity.substr(3, 5);

      for(timeframe in parities[parity]){
        request_data(base, quote, timeframe);
      }
    }
}

timeframe_label.addEventListener("click", function(e){

  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  timeframe  = e.target.id.slice(1);
  // console.log(timeframe);
  left       = 0;
  right      = 99; 

  // console.log(parities[parity]);
  renderHTML(parities[parity], base, quote, timeframe, meta);
});

trends_label.addEventListener("click", function(e){

  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  trend      = e.target.id == 'uptrend' ? 'bullish' : 'bearish';

  meta       = ['trends', trend];
  left       = left;
  right      = right; 

  // console.log(parities[parity]);
  renderHTML(parities[parity], base, quote, timeframe, meta);
}); 

inverse.addEventListener("click", function(e){

  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  trend      = e.target.id;
  console.log(trend);
  meta       = ['inverse', trend];
  left       = left;
  right      = right; 

  // console.log(parities[parity]);
  renderHTML(parities[parity], base, quote, timeframe, meta);
}); 

level_line.addEventListener("click", function(e){

  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);

  meta       = ['level_lines'];
  left       = left;
  right      = right; 

  // console.log(parities[parity]);
  renderHTML(parities[parity], base, quote, timeframe, meta);
}); 

candlesticks_label.addEventListener("click", function(e){

  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  candle     = e.target.id;

  // console.log(candle);
  meta       = ['candlesticks', candle];
  left       = left;
  right      = right; 

  // console.log(parities[parity]);
  renderHTML(parities[parity], base, quote, timeframe, meta);
});

fundamental.addEventListener("click", function(e){
  // console.log("Asd");
  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);

  // console.log(candle);
  meta       = ['fundamental'];
  left       = left;
  right      = right; 

  renderHTML(parities[parity], base, quote, timeframe, meta);
});

elliot.addEventListener("click", function(e){
  // console.log("Asd");
  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);

  // console.log(candle);
  meta       = ['elliot'];
  left       = left;
  right      = right; 

  renderHTML(parities[parity], base, quote, timeframe, meta);
});

zoom.addEventListener("click", function(e){
  
  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);

  left  = 0;
  right = 0;
  // timeframe = '1';
  // console.log(base, quote, timeframe);
  renderHTML(parities[parity], base, quote, timeframe);
});

btn.addEventListener("click", function(e) {
  
  parity     = e.target.id; 
  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  timeframe  = '1';
  meta       = 'false';
  $("#scrolling-thing").css("width", "1300px");

  left       = 0;
  right      = 99; 


  renderHTML(parities[parity], base, quote, timeframe, meta);
});

simulation.addEventListener("click", function(e) {
  
  // parity     = e.target.id; 
  base       = parity.substr(0, 3);
  quote      = parity.substr(3, 5);
  timeframe  = '1';
  meta       = 'false';
  sim        = true;
  $("#scrolling-thing").css("width", "1300px");
  $("#status").css("display", "inline");
  get_coordinates(base, quote, timeframe, 150);

  var i = 1;
  total = parities[parity][timeframe].meta.total;
  // get_trend(base, quote, timeframe, 'bearish', left, right);
  meta = ['simulation'];
  (function loop() {
    left++;
    right++; 
    renderHTML(parities[parity], base, quote, timeframe, meta);

    if (++i < total) {
        setTimeout(loop, 500);  
    }
})();  
  
});

function renderHTML(data, base, quote, timeframe, meta = false) {
    
    data_to_pull = [];
    time_labels = {'1': 'M1', '5' : 'M5', '15': 'M15', '30': 'M30', '60': 'H1', '240': 'H4', '1440': 'D1', '10080': 'W', '43200': 'M'};
    var candles = [];
    var data_lines = [];
    
    dataPts = {
        type: "candlestick",
        opacity: .2,
        risingColor: "white",
        color:"black",
        showInLegend: true,
        name: "",
        yValueFormatString: "##0.0000",
        xValueFormatString: "DD-MM-YY",
        dataPoints: []
      };

      // console.log(data);
    for(i in data[timeframe].data){
        day   = data[timeframe].data[i].day;
        hour  = data[timeframe].data[i].hour;
        open  = data[timeframe].data[i].open;
        close = data[timeframe].data[i].close;
        high  = data[timeframe].data[i].high;
        low   = data[timeframe].data[i].low;
        types = data[timeframe].data[i].types;

        // console.log(day);
        split_day  = day.split("-");
        split_hour = hour.split(":");
        
        candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
    }
    if(left == 0 && right == 0){
        dataPts.dataPoints = candles;
        set_height(data[timeframe].meta.total, data);
      }else{
        dataPts.dataPoints = candles.slice(left, right);
      }
    dataPts.name       = time_labels[timeframe];
    data_to_pull.push(dataPts);
   
    // Descendent trend

    if(meta != false){

      var candles = [];
      dataPts = {
          type: "candlestick",
          // opacity: .2,
          risingColor: "white",
          color:"#808080",
          showInLegend: true,
          name: "",
          yValueFormatString: "##0.0000",
          xValueFormatString: "DD-MM-YY",
          // visible:false,
          dataPoints: []
        };

      level_lines = [];
      simulation  = [];

      for(i in data[timeframe].data){
          day   = data[timeframe].data[i].day;
          hour  = data[timeframe].data[i].hour;
          open  = data[timeframe].data[i].open;
          close = data[timeframe].data[i].close;
          high  = data[timeframe].data[i].high;
          low   = data[timeframe].data[i].low;
          trends = data[timeframe].data[i].trends;

          split_day  = day.split("-");
          split_hour = hour.split(":");
          
          meta_data  = data[timeframe].data[i].meta;
          // console.log(meta_data['level_line']);
          
          if(meta[0] == 'trends'){
            // console.log(meta_data, i)
            if(meta_data['trends'] == meta[1]){
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:'red'});
            }else
            {
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
            }
          }

          if(meta[0] == 'inverse'){
            // console.log(meta_data, i)
            if(meta_data['inverse'] == meta[1]){
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:'red'});
            }else
            {
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
            }
          }

          if(meta[0] == 'candlesticks'){
            if(meta_data['candlesticks'].includes(meta[1])){
              // console.log(meta_data);
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:'red'});
            }else
            {
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
            }

          }

          if(meta[0] == 'fundamental'){

            if(meta_data['fundamental'] !== undefined){
                // underline.push(i);
                candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:meta_data['fundamental'][0]});
            }else
            {
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
            }
          }
          
          if(meta[0] == 'level_lines'){

            if(meta_data['level_line'] !== undefined){
              // candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
              
              for(var el in  meta_data['level_line']){              

                lvl = meta_data['level_line'][el]['level'];
                if(level_lines[i] === undefined){
                    level_lines[i] = [];
                    level_lines[i].push({'x': lvl, 'y': meta_data['level_line'][el]['pos']});
                }else{

                    level_lines[i].push({'x': lvl, 'y': meta_data['level_line'][el]['pos']});
                }
              }
            }

              // data_to_pull.push(data_lines);
          }

          if(meta[0] == 'simulation'){

              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
              simulation.push({x: i - left, y: open});

              // console.log(meta_data);

          }

          if(meta[0] == 'elliot'){

            if(meta_data['elliot'] !== undefined){
                if(meta_data['elliot'] == 'max'){
                    candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:'red'});
                }
                else if(meta_data['elliot'] == 'min'){
                    candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close], color:'yellow'});
                }
                else{
                    candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
                }
            }else
            {
              candles.push({ label: new Date(split_day[0], split_day[1]-1, split_day[2], split_hour[0], split_hour[1]), y: [open, high, low, close]});
            }
          }

          if(meta_data['candlesticks'].includes(meta[1])){
            x = meta[1].replace("_", " ");
            name = x[0].toUpperCase() + x.slice(1);
          }
      }

      if(meta[0] == 'trends'){
        name = meta[1][0].toUpperCase() + meta[1].slice(1);
      }

      if(meta[0] == 'fundamental'){
        name = 'Fundamental analysis';
      }

      if(meta[0] == 'elliot'){
        name = 'Elliot waves';
      }

      if(meta[0] == 'inverse'){
        name = meta[1];
      }

      if(meta[0] == 'level_lines'){
        name = 'Level lines';
      }

      if(meta[0] == 'simulation'){
        name = 'Simulation';
        d = {        
          type: "line",
          dataPoints: simulation.slice(left, right)
        };
        // console.log(d);
        data_to_pull.push(d);
      }

      if(left == 0 && right == 0){
        dataPts.dataPoints = candles;
        set_height(data[timeframe].meta.total), data;
      }else{
        dataPts.dataPoints = candles.slice(left, right);
        
        var dta = {};
        for(i = left; i < right; i++){
          if(level_lines[i] !== undefined){
              for(j = 0; j < level_lines[i].length; j++){
                  // console.log(level_lines[i][j]);
                  if(dta[level_lines[i][j]['x']] === undefined){
                        // console.log(level_lines[i][j]['x']);

                      dta[level_lines[i][j]['x']] = [];
                      dta[level_lines[i][j]['x']].push({x: i - left, y: level_lines[i][j]['y']});
                  }else{
                      dta[level_lines[i][j]['x']].push({x: i - left, y: level_lines[i][j]['y']});
                  }
              }
          }
        }
        
        for(i in dta){
            d = {        
              type: "line",
              dataPoints: dta[i]
            };
            console.log(dta[i]);
            data_to_pull.push(d);
        }
      }
      
      dataPts.name       = name;
      data_to_pull.push(dataPts);

    }

    display_chart(data_to_pull, base, quote);
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function set_height(candles_per_page){

  if(candles_per_page > 5000){
      $("#scrolling-thing").css("width", "40000px");
    }
    if(candles_per_page > 3000){
      $("#scrolling-thing").css("width", "15000px");
    }else if(candles_per_page > 1500){
      $("#scrolling-thing").css("width", "10000px"); 
    }else if(candles_per_page > 1000){
      $("#scrolling-thing").css("width", "6000px"); 
    }else if(candles_per_page > 150){
      $("#scrolling-thing").css("width", "1500px"); 
    }else{
      $("#scrolling-thing").css("width", "1000px"); 
    }
}

function display_chart(data_to_pull, base, quote){

  var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: false,
    theme: "light2", // "light1", "light2", "dark1", "dark2"
    exportEnabled: true,
    title:{
      text: base.toUpperCase() + '/' + quote.toUpperCase(),
      verticalAlign: "top", // "top", "center", "bottom"
      horizontalAlign: "left" // "left", "right", "center"
    },
    // subtitles: [{
    //   text: "Subtitle",
    //   verticalAlign: "top", // "top", "center", "bottom"
    //   horizontalAlign: "left" // "left", "right", "center"
    // }],
    zoomEnabled: true,
    zoomType: "xy",
    // interactivityEnabled: false,
    axisX: {
        labelFormatter: function(e) {
          return e.value;
        },
        // gridThickness: 1,
      },
    axisY: {
      includeZero:false, 
      title: "Price"
    },
    axisY2:{
      title: "Price"
    },
    toolTip: {
      shared: false
    },
    legend: {
      cursor: "pointer",
      horizontalAlign: "left", // "center" , "right"
      verticalAlign: "top",  // "top" , "bottom"
      itemclick: toggleDataSeries,
      fontSize: 15,

    },     
    dataPointWidth: 1,
    data: data_to_pull
  });
  
  chart.render();

  // console.log(chart.data[1]);

  function toggleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
      e.dataSeries.visible = false;
    } else {
      e.dataSeries.visible = true;
    }
    e.chart.render();
  }
}
