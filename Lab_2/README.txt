Atividade 1
	(i)  Nosso estilo arquitetural vai ser o de camadas
	(ii) Os componentes basicos e suas funcionalidades seguem:
		- arquivo txt utilizando a biblioteca json do python
      - armazenar um dicionario no disco
      - acessado pela biblioteca json
    - dicionario global server_dict
      - capaz de ser alterado adicionando, incrementando e removendo itens
      - acessado por dentro do programa
    - interface
      - serie de mensagens que podem ser mostradas aqueles que acessam o sistema
      - acessao por dentro do programa
    - funções de atendimento
      - interpretam mensagens recebidas
      - devolvem resultados
      - sinalizam erros
      - acessado por dentro do programa
      
Atividade 2
	Servidor
		arquivo txt
    server_dict
    interface
    funcoes de atendimento
	
	Cliente
		interface
    funcoes de atendimento
   
  Troca de mensagems
    - Inicialmente não há troca de mensagens, quando inicializado o servidor recebe uma mensagem padrao assim como o cliente, porém são dadas localmente, sem comunicação.
    - O cliente é oferecido a executar um comando, sendo que destes o 'consult' e 'write' geram uma comunicação
      - o servidor vai ler a mensagem recebida pelos comandos citados e trata-la. Independente de erro ou sucesso o servidor entra em contato com uma respsta
      - o cliente recebe essa resposta e imprime, podendo voltar a enviar um comando.
    - A comunicação se mantém nesse loop.
    
    Tratando de comunicações especificas
      - consult
        - Servidor checa se foram enviadas instrucoes corretas (apenas uma chave)
          - se não, manda mensagem de erro e volta a esperar
        - Servidor faz lock() no server_dict
        - Servidor faz a consulta
        - Servidor libera o lock()
        - Servidor envia os dados
        
      - write
        - Servidor checa se foram enviadas instrucoes corretas (apenas uma chave e um valor)
          - se não, manda mensagem de erro e volta a esperar
        - Servidor faz lock() no server_dict
        - Servidor faz a adição ou incremento
        - Servidor libera o lock()
        - Servidor envia a mensagem sinalizando a ação feita
        
      Não sei se é uma comunicação, porém envolve o server_dict
      - remove
        - Servidor checa se a chave existe no dicionario
          - se não, manda mensagem de erro e volta a esperar
        - Servidor faz lock() no server_dict
        - Servidor faz a remoção
        - Servidor manda mensagem de sucesso
        - Servidor libera o lock()
        
