import tkinter as tk
from tkinter import ttk
import requests
import xml.etree.ElementTree as ET
import grpc
import jogo_pb2
import jogo_pb2_grpc


SOAP_URL = "http://localhost:8000/soap"
REST_URL = "http://localhost:5001/rest"
GRPC_HOST = "localhost"
GRPC_PORT = 50051
GRAPHQL_URL = "http://localhost:4000/graphql"





def mostrar_resposta(mensagem):
    text_resposta.configure(state="normal")
    text_resposta.insert("end", mensagem + "\n\n")
    text_resposta.see("end")
    text_resposta.configure(state="disabled")





def limpar_campos():
    entry_titulo.delete(0, "end")
    entry_desenvolvedora.delete(0, "end")
    entry_publicadora.delete(0, "end")
    entry_preco.delete(0, "end")





def enviar_jogo():
    titulo = entry_titulo.get().strip()
    desenvolvedora = entry_desenvolvedora.get().strip()
    publicadora = entry_publicadora.get().strip()
    preco_text = entry_preco.get().strip()

    if not titulo or not desenvolvedora or not preco_text or not publicadora:
        mostrar_resposta("[REST] Erro: Preencha todos os campos.")
        return

    try:
        preco = float(preco_text)
    except ValueError:
        mostrar_resposta("[REST] Erro: O preço deve ser um número.")
        return

    jogo = {"titulo": titulo, "desenvolvedora": desenvolvedora, "preco": preco, "publicadora": publicadora}

    try:
        resposta = requests.post(REST_URL, json=jogo)
        if resposta.status_code == 201:
            mostrar_resposta(f"[REST] Jogo inserido com sucesso: {jogo}")
        else:
            erro = resposta.json().get('erro', 'Erro desconhecido')
            mostrar_resposta(f"[REST] Erro: {erro}")
    except Exception as e:
        mostrar_resposta(f"[REST] Erro de comunicação: {str(e)}")

    limpar_campos()




def modificar_jogo():
    titulo = entry_titulo.get().strip()
    desenvolvedora = entry_desenvolvedora.get().strip()
    publicadora = entry_publicadora.get().strip()
    preco_text = entry_preco.get().strip()

    if not titulo:
        mostrar_resposta("[SOAP] Erro: O título é obrigatório.")
        return

    preco = None
    if preco_text:
        try:
            preco = float(preco_text)
        except ValueError:
            mostrar_resposta("[SOAP] Erro: O preço deve ser um número.")
            return

    envelope = ET.Element("Envelope")
    body = ET.SubElement(envelope, "Body")
    req = ET.SubElement(body, "jogoUpdateRequest")
    ET.SubElement(req, "titulo").text = titulo

    if desenvolvedora:
        ET.SubElement(req, "desenvolvedora").text = desenvolvedora
    if publicadora:
        ET.SubElement(req, "publicadora").text = publicadora
    if preco is not None:
        ET.SubElement(req, "preco").text = str(preco)

    xml_str = ET.tostring(envelope, encoding='utf-8')
    headers = {"Content-Type": "application/xml"}

    try:
        resposta = requests.post(SOAP_URL, data=xml_str, headers=headers)
        if resposta.status_code == 200 and "sucesso" in resposta.text.lower():
            mostrar_resposta(f"[SOAP] Jogo modificado: {titulo}, desenvolvedora: {desenvolvedora}, preço: {preco}, publicadora: {publicadora}")
        else:
            mostrar_resposta(f"[SOAP] Falha ao modificar jogo: {resposta.text}")
    except Exception as e:
        mostrar_resposta(f"[SOAP] Erro de comunicação: {str(e)}")

    limpar_campos()





def procurar_jogo():
    titulo = entry_titulo.get().strip()
    if not titulo:
        mostrar_resposta("[gRPC] Erro: Introduza o título do jogo.")
        return

    try:
        with grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}") as channel:
            stub = jogo_pb2_grpc.jogoServiceStub(channel)
            request = jogo_pb2.jogoRequest(titulo=titulo)
            response = stub.Procurarjogo(request)

            resultado = f"[gRPC] Resultado:\nTítulo: {response.titulo}\nDesenvolvedora: {response.desenvolvedora}\nPreço: {response.preco:.2f}€\nPublicadora: {response.publicadora}"
            mostrar_resposta(resultado)
    except grpc.RpcError as e:
        erro = e.details() if hasattr(e, 'details') else str(e)
        mostrar_resposta(f"[gRPC] Erro: {erro}")

    limpar_campos()




def eliminar_jogo():
    titulo = entry_titulo.get().strip()
    if not titulo:
        mostrar_resposta("[GraphQL] Erro: Introduza o título do jogo.")
        return

    query = {
        "query": f"""
        mutation {{
            eliminarjogo(titulo: \"{titulo}\") {{
                sucesso
                mensagem
            }}
        }}
        """
    }

    try:
        resposta = requests.post(GRAPHQL_URL, json=query)
        dados = resposta.json()

        if "errors" in dados:
            erro = dados['errors'][0]['message']
            mostrar_resposta(f"[GraphQL] Erro: {erro}")
            return

        resultado = dados["data"]["eliminarjogo"]
        mostrar_resposta(f"[GraphQL] {resultado['mensagem']}")
    except Exception as e:
        mostrar_resposta(f"[GraphQL] Erro de comunicação: {str(e)}")

    limpar_campos()





root = tk.Tk()
root.title("Cliente Jogos - REST, SOAP, gRPC, GraphQL")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)


ttk.Label(frame, text="Título:").grid(row=0, column=0, sticky="w")
entry_titulo = ttk.Entry(frame)
entry_titulo.grid(row=0, column=1, sticky="ew")

ttk.Label(frame, text="Desenvolvedora:").grid(row=1, column=0, sticky="w")
entry_desenvolvedora = ttk.Entry(frame)
entry_desenvolvedora.grid(row=1, column=1, sticky="ew")

ttk.Label(frame, text="Publicadora:").grid(row=2, column=0, sticky="w")
entry_publicadora = ttk.Entry(frame)
entry_publicadora.grid(row=2, column=1, sticky="ew")

ttk.Label(frame, text="Preço:").grid(row=3, column=0, sticky="w")
entry_preco = ttk.Entry(frame)
entry_preco.grid(row=3, column=1, sticky="ew")




ttk.Button(frame, text="Inserir jogo (REST)", command=enviar_jogo).grid(row=4, column=0, columnspan=2, sticky="ew", pady=2)
ttk.Button(frame, text="Modificar jogo (SOAP)", command=modificar_jogo).grid(row=5, column=0, columnspan=2, sticky="ew", pady=2)
ttk.Button(frame, text="Procurar jogo (gRPC)", command=procurar_jogo).grid(row=6, column=0, columnspan=2, sticky="ew", pady=2)
ttk.Button(frame, text="Eliminar jogo (GraphQL)", command=eliminar_jogo).grid(row=7, column=0, columnspan=2, sticky="ew", pady=2)





text_resposta = tk.Text(frame, height=12, wrap="word", state="disabled", bg="#f0f0f0")
text_resposta.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")





frame.columnconfigure(1, weight=1)
frame.rowconfigure(8, weight=1)

root.mainloop()
