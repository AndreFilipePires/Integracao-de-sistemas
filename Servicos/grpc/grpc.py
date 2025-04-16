
from concurrent import futures
import grpc
import jogo_pb2
import jogo_pb2_grpc
import xml.etree.ElementTree as ET






class jogoServiceServicer(jogo_pb2_grpc.jogoServiceServicer):
    def Procurarjogo(self, request, context):
        nome_procurado = request.nome.strip().lower()

        try:
            tree = ET.parse("/data/jogos.xml")
            root = tree.getroot()

            for jogo in root.findall("jogo"):
                nome = jogo.find("nome").text.strip()
                if nome.lower() == nome_procurado:
                    autor = jogo.find("autor").text.strip()
                    preco = float(jogo.find("preco").text.strip())
                    return jogo_pb2.jogoResponse(nome=nome, autor=autor, preco=preco)

            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("jogo não encontrado.")
            return jogo_pb2.jogoResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro ao ler o XML: {str(e)}")
            return jogo_pb2.jogoResponse()





def executar():
  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 
    jogo_pb2_grpc.add_jogoServiceServicer_to_server(jogoServiceServicer(), server)
  
    server.add_insecure_port('[::]:50051')
   
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    executar()