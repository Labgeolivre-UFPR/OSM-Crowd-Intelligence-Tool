# -*- coding: utf-8 -*-
import requests
import datetime
import xml.etree.ElementTree as ET
import processing

def coleta(idd,type_osm):
  
    try:
        url = "https://www.openstreetmap.org/api/0.6/"+type_osm+"/"+str(idd)+"/history"
        header = { 'Accept': 'application/xml' }
        r = requests.get(url, headers=header)
       
        
        tree =  ET.ElementTree(ET.fromstring(r.content))

        root = tree.getroot()
        retorno=''
        user={}
        version=[]
        for i in root:
            data=datetime.strptime(i.get('timestamp'), "%Y-%m-%dT%H:%M:%SZ")
            # < se quiser data maxima, > se quiser data minima
        
            user[str(i.get('user'))]=1
            version.append(int(i.get('version')))
            
        retorno=str(len(user))
          
    except :
        print("ERRO ID: "+str(idd), "NÃO LOCALIZADO")
        retorno=''

    return retorno
ids =[]

layer_agregacao = QgsProject.instance().mapLayersByName('Grade')[0]

if layer_agregacao.dataProvider().fieldNameIndex("n_colab") == -1:
    layer_agregacao.dataProvider().addAttributes([QgsField("n_colab", QVariant.Int)])
    layer_agregacao.updateFields()
    layer_agregacao.commitChanges()

for layer in QgsProject.instance().mapLayers().values():
    if str(layer.type())=='QgsMapLayerType.RasterLayer':
        print(layer.type()) ## 1 e ponto
#    if layer.dataProvider().fieldNameIndex("osm_id") == -1:
#        continue
#    layer.startEditing()
#    if layer.dataProvider().fieldNameIndex("n_colab") == -1:
#        layer.dataProvider().addAttributes([QgsField("n_colab", QVariant.Int)])
#        layer.updateFields()
#    layer.commitChanges()
##    id= layer.fields().indexOf('osm_id')
##    ids_unicos = layer.uniqueValues(id)
#    for feat in layer.getFeatures():
#        i =feat['osm_id']
#        n_colab = coleta(i,feat['osm_type'])
#        layer.startEditing()
#        layer.selectByExpression( "\"osm_id\"="+i )
#        selection = layer.selectedFeatures()
#        selection[0]['n_colab'] = int(n_colab)
#        layer.updateFeature(selection[0])
#        layer.commitChanges()
#        
#    
#    parameter_contagem ={'INPUT':layer_agregacao ,'JOIN':layer ,'PREDICATE':[0,1,5,6], 'JOIN_FIELS':["n_colab"],'SUMMARIES':[5],'OUTPUT':'memory:grade_agregada' }
#    layer_joined = processing.run("qgis:joinbylocationsummary", parameter_contagem)
#    layer_agregacao.startEditing()
#    for feature in layer_joined['OUTPUT'].getFeatures():
#        n_colab=feature['n_colab_sum']
#        id_layer_joined = feature['id']
#        layer_agregacao.selectByExpression( "\"id\"="+str(id_layer_joined) )
#        selection = layer_agregacao.selectedFeatures()
#        selection_value= selection[0]['n_colab']
#        if selection_value==NULL:
#            selection_value=0
#        if n_colab==NULL:
#            n_colab=0
#        
#        selection[0]['n_colab'] = n_colab+selection_value
#        layer_agregacao.updateFeature(selection[0])
#    layer_agregacao.commitChanges()
