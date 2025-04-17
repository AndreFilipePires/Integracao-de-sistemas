from concurrent import futures
import grpc
import jogotipo_pb2
import jogotipo_pb2_grpc
import xml.etree.ElementTree as ET





class jogoServiceServicer(jogotipo_pb2_grpc.jogoServiceServicer):
    def Procurarjogo(self, request, context):
        titulo_procurado = request.titulo.strip().lower()

        try:
            tree = ET.parse("/data/jogos.xml")
            root = tree.getroot()
            for jogo in root.findall("jogo"):
                titulo = jogo.find("titulo").text.strip()
                if titulo.lower() == titulo_procurado:
                    desenvolvedora = jogo.find("desenvolvedora").text.strip()
                    publicadora = jogo.find("publicadora").text.strip()
                    preco = float(jogo.find("preco").text.strip())
                    return jogotipo_pb2.jogoResponse(titulo=titulo, desenvolvedora=desenvolvedora, publicadora=publicadora, preco=preco)

            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("jogo não encontrado.")
            return jogotipo_pb2.jogoResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Erro ao ler o XML: {str(e)}")
            return jogotipo_pb2.jogoResponse()





def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jogotipo_pb2_grpc.add_jogoServiceServicer_to_server(jogoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    servir()