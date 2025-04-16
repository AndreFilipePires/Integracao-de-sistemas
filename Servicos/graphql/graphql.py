
import xml.etree.ElementTree as ET  
from flask import Flask  
from flask_graphql import GraphQLView  
import graphene  


XML_PATH = "/data/jogos.xml"









class Resultado(graphene.ObjectType):
    sucesso = graphene.Boolean()  
    mensagem = graphene.String()   














class apagarJogo(graphene.Mutation):
    class Arguments:
        nome = graphene.String(required=True)  

    Output = Resultado  

    def mutate(root, info, nome):
        try:
          
            tree = ET.parse(XML_PATH)
            root_xml = tree.getroot()
            jogos = root_xml.findall("jogo")

           
            encontrados = 0
            for jogo in jogos:
                if jogo.find("nome").text.strip().lower() == nome.strip().lower():
                    root_xml.remove(jogo)
                    encontrados += 1


            if encontrados > 0:
                tree.write(XML_PATH, encoding="utf-8", xml_declaration=True)
                return Resultado(sucesso=True, mensagem=f"{encontrados} jogo(s) removido(s).")
            else:
                return Resultado(sucesso=False, mensagem="jogo não encontrado.")

        except Exception as e:
            return Resultado(sucesso=False, mensagem=f"Erro: {str(e)}")














class Mutation(graphene.ObjectType):
    apagar_jogo = apagarJogo.Field() 

schema = graphene.Schema(mutation=Mutation)










app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True  
    ),
)












if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)  