# Importação das bibliotecas necessárias
import os
import xml.etree.ElementTree as ET
from flask import Flask, request, Response


app = Flask(__name__)

XML_FILE_PATH = "/data/jogos.xml"







def inicializar_xml():
    xml_dir = os.path.dirname(XML_FILE_PATH)
    os.makedirs(xml_dir, exist_ok=True)
    if not os.path.exists(XML_FILE_PATH):
        root = ET.Element("jogos")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)






def atualizar_jogo_xml(titulo, novo_desenvolvedora=None, novo_publicadora=None, novo_preco=None):

  

    inicializar_xml()
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    updated = False

 
    for jogo in root.findall("jogo"):
        if jogo.findtext("titulo", "").strip().lower() == titulo.strip().lower():
            if novo_desenvolvedora:
                jogo.find("desenvolvedora").text = novo_desenvolvedora
            if novo_publicadora:
                jogo.find("publicadora").text = novo_publicadora
            if novo_preco is not None:
                jogo.find("preco").text = str(novo_preco)
            updated = True
            break


    if updated:
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
    return updated







@app.route('/soap', methods=['POST'])
def soap_service():
    xml_request = request.data.decode('utf-8')
    try:
       
        root_req = ET.fromstring(xml_request)
        body = root_req.find("Body")
        if body is None:
            raise ValueError("Elemento Body não encontrado.")

      
        jogo_update = body.find("jogoUpdateRequest")
        if jogo_update is not None:
            
            titulo = jogo_update.findtext("titulo")
            novo_desenvolvedora = jogo_update.findtext("desenvolvedora")
            novo_publicadora = jogo_update.findtext("publicadora")
            novo_preco_text = jogo_update.findtext("preco")
            novo_preco = float(novo_preco_text) if novo_preco_text else None
            

          
            if not titulo or (not novo_desenvolvedora and novo_preco is None):
                raise ValueError("Dados insuficientes para atualização via SOAP.")

           
            if atualizar_jogo_xml(titulo, novo_desenvolvedora, novo_publicadora, novo_preco):
                response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                        <soapenv:Body>
                            <jogoUpdateResponse>
                                <mensagem>jogo atualizado com sucesso!</mensagem>
                            </jogoUpdateResponse>
                        </soapenv:Body>
                    </soapenv:Envelope>"""
                return Response(response_xml, mimetype="text/xml")
            else:
                raise ValueError("jogo não encontrado para atualização.")
        else:
            raise ValueError("Operação não reconhecida. Use jogoUpdateRequest para atualizar.")

   
    except Exception as e:
        fault_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Body>
                    <soapenv:Fault>
                        <faultcode>SOAP-ENV:Client</faultcode>
                        <faultstring>{str(e)}</faultstring>
                    </soapenv:Fault>
                </soapenv:Body>
            </soapenv:Envelope>"""
        return Response(fault_xml, status=400, mimetype="text/xml")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)