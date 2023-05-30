#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10000

information_interface = 'Bem vindo, voce e um cliente nesse sistema\nSuas possiveis interacoes sao as seguintes:\n- consult (entra na interface de consulta)\n- remove (entra na interface de remoção)\n- write (entra na interface de escrita)\n- fim (encerra a conexao com o servidor)\n- help (mostra novamente esta mensagem)\n'

def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	while True: 
		comando = input("Digite um comando:")
		if comando == 'fim': break 
		elif (comando == 'consult'):
			key = input('Digite a chave a ser consultada (apenas a chave):')
			msg = conn.root.exposed_consult(key)
			
		elif (comando == 'write'):
			key = input('Digite da chave (apenas uma):')
			value = input('Digite um valor (apenas um):')
			msg = conn.root.exposed_write(key, value)

		elif (comando == 'remove'):
			key = input('Digite a chave a ser removida (apenas a chave):')
			msg = conn.root.exposed_remove(key)

		elif (comando == 'help'):
			msg = information_interface
		else: 
			msg = 'Comando nao reconhecido'

		print(msg)

	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	print(information_interface)
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()
 
