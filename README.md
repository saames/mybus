# MyBus

O sistema "MyBus" será uma aplicação para consulta e gerenciamento de informações sobre o transporte público urbano, com acesso para usuários finais e administradores do sistema. Ele permitirá aos usuários visualizarem as rotas, os pontos de parada e consultar os horários programados de cada linha.  

O sistema considera a linha como a representação do serviço de transporte em sua totalidade, sendo sua identidade comercial e operacional. Assim, uma linha é composta pelas seguintes informações: um nome e um número. 

Além disso, uma linha precisa de, no mínimo, um caminho para operar (seja o de ida ou o de volta), e o sistema deve aceitar a inserção de ambos. Caso apenas um caminho seja informado, o outro será considerado o inverso do informado. Uma linha pode estar relacionada a várias rotas, que são esses caminhos propriamente ditos. 

A rota, por sua vez, é o caminho geográfico que um ônibus de uma determinada linha percorre em um sentido, representado por um traçado no mapa. Essa rota deve estar relacionada a uma, e somente uma, linha. 

A rota é composta por vários pontos. Cada ponto consiste em um conjunto ordenado de coordenadas (latitude e longitude) que, quando ligados em sequência, desenham a linha exata da rota no mapa. 

A aplicação exibirá mapas mostrando o trajeto dos ônibus e a localização das paradas. Para a gestão do sistema, um painel administrativo permitirá o cadastro e a manutenção de todas as rotas, a frota de ônibus, os pontos de parada e suas respectivas tabelas de horários. 

- [Documentação](https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2YvYy8yYmMxODc5YmQ4YzkwNjZmL0V2a3g1N0M5dGpwQ3JqUDJlMExEbldRQmVaLWxFREZ4NURXeXVESndpLVlCYWc%5FZT1iVkpxVkc&id=2BC1879BD8C9066F%21sb0e731f9b6bd423aae33f67b42c39d64&cid=2BC1879BD8C9066F) (Requisitos, casos de uso textuais etc.)

## Como instalar?

**1. Crie o ambiente virtual**

`python3 -m venv venv`

**2. Acesse o ambiente virtual**

- Windows: `.venv\Scripts\activate`
- Linux: `source .venv/bin/activate`

**3. Instale as bibliotecas necessárias:**

`pip install -r requirements.txt`
