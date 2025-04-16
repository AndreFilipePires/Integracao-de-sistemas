
import os
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from jsonschema import validate, ValidationError


app = Flask(__name__)
api = Api(app)


jogo_schema = {
    "type": "object",
    "properties": {
        "titulo": {"type": "string"},
        "desenvolvedora": {"type": "string"},
        "publicadora": {"type": "string"},
        "preco": {"type": "number"}
    },
    "required": ["titulo", "desenvolvedora", "preco"]
}


XML_FILE_PATH = "/data/jogos.xml"


def inicializar_xml():
 
    xml_dir = os.path.dirname(XML_FILE_PATH)
    os.makedirs(xml_dir, exist_ok=True)
    if not os.path.exists(XML_FILE_PATH):
        root = ET.Element("jogos")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)




def adicionar_jogo_xml(titulo, desenvolvedora, publicadora, preco):
    
    inicializar_xml()
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    
   
    jogo_elem = ET.Element("jogo")
    ET.SubElement(jogo_elem, "titulo").text = titulo
    ET.SubElement(jogo_elem, "desenvolvedora").text = desenvolvedora
    ET.SubElement(jogo_elem, "publicadora").text = publicadora
    ET.SubElement(jogo_elem, "preco").text = str(preco)
    root.append(jogo_elem)
    tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)






class jogoResource(Resource):
    def post(self):
        
        try:
            jogo = request.json
            validate(instance=jogo, schema=jogo_schema)
            adicionar_jogo_xml(jogo["titulo"], jogo["desenvolvedora"], jogo["publicadora"], jogo["preco"])
            return {"mensagem": "jogo adicionado com sucesso!"}, 201
        except ValidationError as e:
            return {"erro": f"Erro de validação: {e.message}"}, 400
        except Exception as e:
            return {"erro": f"Erro estranho : {str(e)}"}, 500


api.add_resource(jogoResource, '/rest')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)