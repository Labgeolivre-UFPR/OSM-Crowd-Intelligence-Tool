# -*- coding: utf-8 -*-
import requests
import datetime
import xml.etree.ElementTree as ET
import processing
import sys


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
#            data=datetime.strptime(i.get('timestamp'), "%Y-%m-%dT%H:%M:%SZ")
            # < se quiser data maxima, > se quiser data minima
        
            user[str(i.get('user'))]=1
            version.append(int(i.get('version')))
            
        retorno=str(len(user))
          
    except Exception as error :
        print(error)
        print("ERRO ID: "+str(idd), "NÃO LOCALIZADO")
        retorno=-1

    return retorno
id =''

layer_agregacao = QgsProject.instance().mapLayersByName('Grid')[0]
if layer_agregacao.dataProvider().fieldNameIndex("id") != -1:
    id='id'
elif layer_agregacao.dataProvider().fieldNameIndex("gid") != -1:
    id='gid'
else:
    sys.exit("need identify collumn id or gid")
    
if layer_agregacao.dataProvider().fieldNameIndex("n_colab") == -1:
    layer_agregacao.dataProvider().addAttributes([QgsField("n_colab", QVariant.Double)])
    layer_agregacao.updateFields()
    layer_agregacao.commitChanges()

for layer in QgsProject.instance().mapLayers().values():
    if str(layer.type())=='QgsMapLayerType.RasterLayer':
        continue
    if layer.dataProvider().fieldNameIndex("osm_id") == -1:
        continue
    layer.startEditing()
    if layer.dataProvider().fieldNameIndex("n_colab") == -1:
        layer.dataProvider().addAttributes([QgsField("n_colab", QVariant.Double)])
        layer.updateFields()
    layer.commitChanges()
    if layer.wkbType() != 1:
        parameter_cross ={'INPUT':layer ,'JOIN':layer_agregacao ,'PREDICATE':[0,1], 'JOIN_FIELDS':[id],'SUMMARIES':[0],'OUTPUT':'memory:count_intersct' }
        layer_agregacao_interse = processing.run("qgis:joinbylocationsummary", parameter_cross)
        layer=layer_agregacao_interse['OUTPUT']
#        l = QgsVectorLayer(layer,'teste',"memory")
#        QgsProject.instance().addMapLayer(l)
       
        

    
#    id= layer.fields().indexOf('osm_id')
#    ids_unicos = layer.uniqueValues(id)
    for feat in layer.getFeatures():
        i =feat['osm_id']
     
        n_colab = coleta(i,feat['osm_type'])
        if(n_colab==-1):
            
            continue;
        layer.startEditing()
        layer.selectByExpression( "\"osm_id\"="+i )
        selection = layer.selectedFeatures()
       
        valor = 0
        if layer.wkbType() != 1:
            if int(n_colab)/float(selection[0][id+'_count']) >0:
                selection[0]['n_colab'] = int(n_colab)/float(selection[0][id+'_count'])
                valor = int(n_colab)/float(selection[0][id+'_count'])
            else:
                selection[0]['n_colab'] = int(n_colab)
                valor =int(n_colab)
        else:
            selection[0]['n_colab'] = int(n_colab)
            valor =int(n_colab)
        print(valor)
        
        layer.updateFeature(selection[0])
        layer.commitChanges()
        b=10.0+8.0+2.0+3.0+3.0+0.5+1.0+1.0+1.0+1.0+1.0+1.0+5.0+1.0+1.0+1.0+1.0
        
    
    parameter_contagem ={'INPUT':layer_agregacao ,'JOIN':layer ,'PREDICATE':[0,1,5,6], 'JOIN_FIELS':["n_colab"],'SUMMARIES':[5],'OUTPUT':'memory:grade_agregada' }
    layer_joined = processing.run("qgis:joinbylocationsummary", parameter_contagem)
    layer_agregacao.startEditing()
    for feature in layer_joined['OUTPUT'].getFeatures():
       
        n_colab=feature['n_colab_sum']
        id_layer_joined = feature['id']
        layer_agregacao.selectByExpression( "\"id\"="+str(id_layer_joined) )
        selection = layer_agregacao.selectedFeatures()
        selection_value= selection[0]['n_colab']
        if selection_value==NULL:
            selection_value=0
        if n_colab==NULL:
            n_colab=0
        
        selection[0]['n_colab'] = n_colab+selection_value
        layer_agregacao.updateFeature(selection[0])
    layer_agregacao.commitChanges()
