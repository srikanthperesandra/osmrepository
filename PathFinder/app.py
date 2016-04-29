'''
Created on Apr 26, 2016

@author: srikanth
'''
from flask.globals import request
from bson.int64 import long
API_PATH = "/api/v1/"

from flask import Flask,render_template,Response
from services.registry.Registry import Registry
from services.registry.RegistryServices import RegistryServices
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route(API_PATH+"streets",methods=['GET'])
def getStreets():
    cRouteService = Registry.getInstance().getService(RegistryServices.CROUTES_SERVICE)
    if cRouteService == None:
        return Response("failed to find Cluster Route Service from Registry",status=500,mimetype="text/plain")
    cRoutesStreets = cRouteService.getcRoutesStreetsWithNames()
    #for cRouteStreet in cRouteService.getcRoutesStreetsWithNames():
    #cRoutesStreets.append(json.loads(str(cRouteStreet)))
    resp = Response(dumps(cRoutesStreets))
    resp.headers['content-type'] = 'application/json'
    return resp
    #return Response(cRoutesStreets,status=200,mimetype="application/json")
    #return "nodes"
@app.route(API_PATH+"path",methods=['GET']) 
def fspService():
    if not('src' in request.args) or not('dest' in request.args):
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    src_street = request.args['src'] 
    dest_street = request.args['dest']
    if src_street==None or dest_street==None:
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    if src_street=="" or dest_street=="":
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    fsp_service = Registry.getInstance().getService(RegistryServices.FSP_SERVICE)
    if fsp_service == None:
        return Response("failed to find Routing Service from Registry",status=500,mimetype="text/plain")
    #print (src_street)
    result = fsp_service.invokeRelationBasedFSPService(long(src_street),long(dest_street))
    #print(result)
    return Response(dumps(result),status=200,mimetype="application/json")
@app.route(API_PATH+"path/alternatives",methods=['GET']) 
def fspService2():
    if not('src' in request.args) or not('dest' in request.args):
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    src_street = request.args['src'] 
    dest_street = request.args['dest']
    if src_street==None or dest_street==None:
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    if src_street=="" or dest_street=="":
        return Response("Bad request: please provide src,dest street osmIdentifiers",status=400,mimetype="text/plain")
    fsp_service = Registry.getInstance().getService(RegistryServices.FSP_SERVICE)
    if fsp_service == None:
        return Response("failed to find Routing Service from Registry",status=500,mimetype="text/plain")
    #print (src_street)
    result = fsp_service.invokeRelationBasedFSPService2(long(src_street),long(dest_street))
    #print(result)
    return Response(dumps(result),status=200,mimetype="application/json")
if __name__ == '__main__':
    app.run(debug=True)