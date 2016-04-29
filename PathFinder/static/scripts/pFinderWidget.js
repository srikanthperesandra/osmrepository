/**
 * http://usejsdoc.org/
 */

$.ajaxSetup({async:false});
/*$.getScript("jqwidgets/jqxcore.js");
$.getScript("jqwidgets/jqxdata.js");
$.getScript("jqwidgets/jqxinput.js");
$.getScript("jqwidgets/jqxbuttons.js");
*/
$.ajaxSetup({async:true});

var osmMap = null;
var pfWidget = (function(){
	
	
			return{
				tabConatiner:null,
				templateStr:null,
				theme:"ui-sunny",
				map:null,
				nodesData:null,
				source:[],
				srcLocation:null,
				destLocation:null,
				appConfig:{
					sEndpoint:"/api/v1",
					streetService:"/streets",
					pathService:"/path",
					MAPBOX_KEY: "pk.eyJ1Ijoic3Jpa2FudGhwZXJlc2FuZHJhIiwiYSI6ImNpbmtkeGE3NjAwN2N3N2tsd3QzdTdveHcifQ.foQHZKPnsWsoGer49vc_MQ"
				},
				init:function(){
					var thisRef = this;
					var src = document.getElementById("mapArea").src;
					document.getElementById("go").onclick=function(){
						//alert(thisRef.srcLocation);
						//alert(thisRef.destLocation);
						
						$.get(thisRef.appConfig.sEndpoint+thisRef.appConfig.pathService+"?src="+thisRef.srcLocation+"&dest="+thisRef.destLocation).done(function(data){
							//alert(JSON.stringify(data));
							//thisRef.addRoute(data);
							//.addRoute(data);
							query="?points=";
							for(var i=0;i<data.points.length;i++){
								var temp=JSON.stringify([data.points[i]['lng'],data.points[i]['lat']])
								if(i==data.points.length-1){
									query=query+temp;
								}else{
									query=query+temp+"|";
								}
							}
							document.getElementById("mapArea").src=src+query;
							
						}).fail(function(err){
							alert(JSON.stringify(err));
						})
					
				 }
				},
				prepareWidgets:function(){
					//alert("called");
					 var thisRef = this; 
					 //alert(JSON.stringify(thisRef.nodesData[0].street['meta_data']));
					 for(var i=0;i<thisRef.nodesData.length;i++){
						 //alert(JSON.stringify(record));
						 var temp = {"label":thisRef.nodesData[i].street['meta_data'].name,"value":thisRef.nodesData[i].street.osmId};
						 thisRef.source.push(temp)
					 }
					 $("#source").jqxInput({ theme: thisRef.theme, placeHolder: " Source",minLength: 1, source:thisRef.source,height:'25' });
					 $("#destination").jqxInput({ theme: thisRef.theme, placeHolder: " Destination", minLength: 1, source:thisRef.source ,height:'25' });
					 $("#go").jqxButton({ theme: thisRef.theme, enableHover: false });
					 $("#source").on("select",function(event){
						 var item = event.args.item;
						 thisRef.srcLocation = item.value;
					 });
					 
					 $("#destination").on("select",function(event){
						 var item = event.args.item;
						 thisRef.destLocation = item.value;
					 });
					 
				},
				invokeStreetsService:function(){
					var thisRef = this;
					$.get(thisRef.appConfig.sEndpoint+thisRef.appConfig.streetService).done(function(data){
						try{
							//alert(data);
							thisRef.nodesData = data;
							//alert(thisRef.nodesData);
							thisRef.prepareWidgets();
						}catch(err){
							alert("err"+err);
						}
						
					}).fail(function(err){
						//alert(err);
						alert(JSON.stringify(err));
					})
				},
				plotMap:function(){
					//alert(document.getElementById("osmMap"));
					//alert("called");
					  osmMap = L.map('bwMap',{
						    center: [48.777106, 9.180769],
						    zoom: 10
						    });

						    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
						    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'+'&copy; <a href="http://www.mapbox.com">MapBox</a>'+' contributors'
						    }).addTo(osmMap);
					 //alert(this.map)
				    //document.getElementById("osmMap").style.dsiplay="block";
				    //L.Util.requestAnimFrame(thisRef.map.invalidateSize,thisRef.map,!1,thisRef.map._container);
				},
				addRoute:function(data){
					var thisRef = this;
					var points = [];
					var polyPoints =[];
					var wayPoints = [];
					data=data.substr(data.indexOf("=")+1)
					//alert(data);
					points=data.split("|");
					for(var i=0;i<points.length;i++){
						var temp = JSON.parse(points[i]);
						polyPoints.push(new L.LatLng(temp[0],temp[1]))
						wayPoints.push(L.latLng(temp[0],temp[1] ));
					}
					
						
					
					var polylineOptions = {
				               color: 'green',
				               weight: 4,
				               opacity: 0.9
				             };
					
				      var polyline = new L.Polyline(polyPoints, polylineOptions);
				         osmMap.addLayer(new L.marker(polyPoints[0]));
				         osmMap.addLayer(new L.marker(polyPoints[polyPoints.length-1]));
				         //alert(thisRef.appConfig.MAPBOX_KEY);
				         var mapBox=L.Routing.mapbox(thisRef.appConfig.MAPBOX_KEY,{
				 			profile: 'mapbox.walking'
						 });
				         
				         
				        
				         
				         //alert(mapBox)
				         var control = L.Routing.control({
								waypoints: wayPoints,
								router:mapBox,
							    routeWhileDragging: true,
							    reverseWaypoints: true,
							    showAlternatives: true,
								lineOptions:{
							        styles: [
									            {color: 'red', opacity: 0.15, weight: 5},
									            {color: 'white', opacity: 0.8, weight: 2},
									            {color: 'blue', opacity: 0.5, weight: 6}
									        ]
									    }
							    
							}).addTo(osmMap);
				         //alert(control);
				         L.Routing.errorControl(control).addTo(osmMap);
				         osmMap.addLayer(polyline);
				         osmMap.fitBounds(polyline.getBounds());
				        
						
				},
			};
})();