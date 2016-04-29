'''
Created on Feb 10, 2016

@author: srikanth

'''
from gi.repository import GtkClutter,Clutter
from services.registry.Registry import Registry
GtkClutter.init([])
from gi.repository import GObject,Gtk,GtkChamplain, Champlain,Pango
from services.entitiy.NodeService import NodeService
from bson.int64 import long
from fsp.Coordinates import Coordinates
from pfinder.PFinderConfig import downArrowImage 
import json
class BootStarpWidget:
    def __init__(self):
        self.window = None
        self.widget = None
        self.srcTextView = None
        self.destTextView= None
        self.boxContainer = None
        self.table = None
        self.submit = None
        self.inputContianer=None
        self.nodes_service = Registry.getInstance().getService("node_service")
        self.cGraphService = Registry.getInstance().getService("cGraph_service")
        self.fsp_service =  Registry.getInstance().getService("fsp_service")
        self.gHoper_service = Registry.getInstance().getService("gHoper_service")
        self.down_image = None
        self.liststore = None
        self.lat = 51.0612466
        self.lng=5.4208665
        self.view= None
    def init(self):
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.connect("destroy", Gtk.main_quit)
        self.widget = GtkChamplain.Embed()
        self.widget.set_size_request(640, 480)
        self.view = self.widget.get_view()
        self.view.center_on(self.lat, self.lng)
        self.view.set_reactive(True)
        self.view.set_property('kinetic-mode', True)
        self.view.set_property('zoom-level', 10)
        self.boxContainer = Gtk.HBox(False, 10)
        self.inputContianer=Gtk.VBox(False, 10)
        self.buttonInit()
        self.prepareListModel()
        self.initSrcTextView()
        self.initDestTextView()
        self.tableView()
        self.inputContianer.pack_start(self.srcTextView, fill=False,expand=False, padding=0)
        self.inputContianer.pack_start(self.destTextView, fill=False,expand=False, padding=0)
        self.inputContianer.pack_start(self.submit, fill=False,expand=False, padding=0)
        self.inputContianer.pack_start(self.table, fill=False,expand=False, padding=0)
        self.boxContainer.pack_start(self.inputContianer, fill=False, expand=False, padding=0)
        self.boxContainer.add(self.widget)
        self.window.add(self.boxContainer)
        #self.window.add(self.widget)
        self.window.show_all()
    def tableView(self):
        self.table = Gtk.Table()
        
        '''label=Gtk.Label()
        label.set_text("abc")
        label1=Gtk.Label()
        label1.set_text("abcef")
        self.table.attach(label,0,1,0,1)
        self.table.attach(label1,0,1,1,2)
        '''
    def buttonInit(self):
        self.submit = Gtk.Button()
        self.submit.set_label("Go")
        self.submit.connect("clicked", self.onclickHandler)    
    def onclickHandler(self,widget):
        srcLocation  = self.srcTextView.get_model().get_value(self.srcTextView.get_active_iter(),0)
        destLocation  = self.destTextView.get_model().get_value(self.destTextView.get_active_iter(),0)
        #print (srcLocation)
        srcNode =   self.cGraphService.getStreetfromNode(long(srcLocation))#srcLocation['targetNode']['osmId']#self.srcTextView.get_model().get_value(self.srcTextView.get_active_iter(),0)
        destNode =  self.cGraphService.getStreetfromNode(long(destLocation))#destLocation['targetNode']['osmId']#self.destTextView.get_model().get_value(self.destTextView.get_active_iter(),0)
        #srcNode = self.nodes_service.getNode(srcOSMId)
        #destNode = self.nodes_service.getNode(destOSMId)
        srcMarker = self.createMarker(srcNode['street']['meta_data']['name'],srcNode['targetNode']["lat"] , srcNode['targetNode']["lng"])
        destMarker = self.createMarker(destNode['street']['meta_data']['name'] ,destNode['targetNode']["lat"], destNode['targetNode']["lng"])
        layer = Champlain.MarkerLayer()
        layer.add_marker(srcMarker)
        srcMarker.set_reactive(True)
        layer.add_marker(destMarker)
        destMarker.set_reactive(True)
        result=self.invokeFSPService(long(srcLocation), long(destLocation))
        #print (result)
        self.updateUIToAddPath(result)
        #self.updateUIToAddPath3(result)
        #layer.set_all_markers_draggable()
        #layer.show()
        self.view.add_layer(layer)
        self.view.ensure_layers_visible(True)
        #self.view.refresh()
    def initSrcTextView(self):
        self.srcTextView = Gtk.ComboBox()
        self.srcTextView.set_model(self.liststore)
        cell = Gtk.CellRendererText()
        self.srcTextView.pack_start(cell, False)
        self.srcTextView.add_attribute(cell, 'text', 1)
        self.srcTextView.set_active(0)
    def initDestTextView(self):
        self.destTextView = Gtk.ComboBox()
        self.destTextView.set_model(self.liststore)
        cell = Gtk.CellRendererText()
        self.destTextView.pack_start(cell, False)
        self.destTextView.add_attribute(cell, 'text', 1)
        self.destTextView.set_active(0)
    def createMarker(self,name,lat,lng):
        #print (lat)
        orange = Clutter.Color.new(50, 0, 50, 200)
        marker = Champlain.Label.new_with_text(name, "Serif 10", None,orange)
        marker.set_use_markup(True)
        marker.set_alignment(Pango.Alignment.LEFT)
        marker.set_color(orange)
        marker.set_location(lng, lat)
        return marker
    def prepareListModel(self):
        self.liststore = Gtk.ListStore(str, str)
        counter = 0
        for cEdge in self.cGraphService.getClusterEdges():
            try:
                meta_data = cEdge["street"]["meta_data"]
                if 'name' in meta_data:
                        #print (meta_data)
                    self.liststore.append([str(cEdge['targetNode']['osmId']), meta_data['name']])
                    counter=counter +1
            except OverflowError as e:
                print (e)
    def invokeFSPService(self,src,dest):
        result=self.fsp_service.calculateShortestPath(src, dest)
        return self.fsp_service.processResult(result)
    def updateUIToAddPath(self,fsp_result):
        print (fsp_result)
        path_layer = Champlain.PathLayer()
        streets = fsp_result['path']
        x = [0,1]
        y= [0,1]
        distance =Gtk.Label()
        distance.set_text("Distance: "+str(fsp_result['distance']/1000)+" Km")
        self.table.attach(distance,x[0],x[1],y[0],y[1])
        y[0]=y[0]+1
        y[1]=y[1]+1
        for node in streets:
            targetNode = node['targetNode']
            street_node = node['street']
            coord = Champlain.Coordinate.new_full(targetNode['lng'], targetNode['lat'])
            path_layer.add_node(coord)
            label = Gtk.Label()
            if 'name' in street_node["meta_data"] and 'highway' in street_node["meta_data"]:
                label.set_text(street_node["meta_data"]['name']+", "+"highway:"+street_node['meta_data']['highway'])
            else:
                label.set_text("highway:"+street_node['meta_data']['highway'])
            self.table.attach(label,x[0],x[1],y[0],y[1])
            y[0]=y[0]+1
            y[1]=y[1]+1
            
            down_image = Gtk.Image()
            down_image.set_from_file(downArrowImage)
            self.table.attach(down_image,x[0],x[1],y[0],y[1])
            down_image.show()
            
            y[0]=y[0]+1
            y[1]=y[1]+1
        finish =Gtk.Label()
        finish.set_text("Finish")
        self.table.attach(finish,x[0],x[1],y[0],y[1])
        self.view.add_layer(path_layer)
        self.view.ensure_layers_visible(True)
        self.table.show_all()
        #self.inputContianer.add_child(self.table)
        #self.inputContianer.pack_start(self.table, fill=False,expand=False, padding=0)
    def updateUIToAddPath2(self,fsp_result):
        path_layer = Champlain.PathLayer()
        streets = fsp_result['path']
        for i in range(0,len(streets)-1):
            result = self.invokeGraphHoperRoutingService(streets[i]['targetNode'],streets[i+1]['targetNode']).decode("utf-8")
            #print (result)
            result =json.loads(result)
            if not('paths' in result):
                continue
            instructions = result["paths"][0]["instructions"]
            points = result["paths"][0]["points"]["coordinates"]
            for instruction in instructions:
                #print (instruction['interval'][0])
                src = points[instruction["interval"][0]]
                dest = points[instruction["interval"][1]]
                src_coord = Champlain.Coordinate.new_full(src[0],src[1])
                dest_coord = Champlain.Coordinate.new_full(dest[0],dest[1])
                path_layer.add_node(src_coord)
                path_layer.add_node(dest_coord)
        self.view.add_layer(path_layer)
        self.view.ensure_layers_visible(True)
    def updateUIToAddPath3(self,fsp_result):
        path_layer = Champlain.PathLayer()
        dash = [6, 2]
        path_layer.set_dash(dash)
        streets = fsp_result['path']
        result = self.invokeGraphHoperRoutingService(streets[0]['targetNode'],streets[len(streets)-1]['targetNode']).decode("utf-8")
            #print (result)
        result =json.loads(result)
        instructions = result["paths"][0]["instructions"]
        points = result["paths"][0]["points"]["coordinates"]
        for instruction in instructions:
                #print (instruction['interval'][0])
            src = points[instruction["interval"][0]]
            dest = points[instruction["interval"][1]]
            src_coord = Champlain.Coordinate.new_full(src[0],src[1])
            dest_coord = Champlain.Coordinate.new_full(dest[0],dest[1])
            path_layer.add_node(src_coord)
            if instruction['sign'] == 2:
                path_layer.set_rotation(Clutter.RotateAxis().X_AXIS,60.6,src[0],src[1],0)
            #else:
                #path_layer.set_rotation(Clutter.RotateAxis().X_AXIS,-45,src[0],src[1],0)
            path_layer.add_node(dest_coord)
        self.view.add_layer(path_layer)
        self.view.ensure_layers_visible(True)       
    def invokeGraphHoperRoutingService(self,fromNode,toNode):
        point1 = Coordinates(fromNode['lat'],fromNode['lng'])
        point2 = Coordinates(toNode['lat'],toNode['lng'])
        return self.gHoper_service.invokeRoutingService(point1, point2)
bootStrapWidget = BootStarpWidget()
bootStrapWidget.init()
Gtk.main()
