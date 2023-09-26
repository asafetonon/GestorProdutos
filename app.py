from tkinter import ttk
from tkinter import *
import sqlite3

class Produto:
    db = 'database/produtos.db'
    def __init__(self, root):
        self.janela = root
        self.janela.title("App Gestor de Produtos") # Título da janela
        self.janela.resizable(1,1) # Ativar a redimensionamento da janela. Para desativá-la: (0,0)
        self.janela.wm_iconbitmap('recursos/icon.ico')

        # Criação do recipiente Frame principal
        frame = LabelFrame(self.janela, text = "Registrar um novo Produto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nome
        self.etiqueta_nome = Label(frame, text="Nome: ", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_nome.grid(row=1, column=0) # Posicionamento através de grid

        # Entry Nome (caixa de texto que irá receber o nome)
        self.nome = Entry(frame, font=('Calibri', 13)) # Caixa de texto (input de texto) localizada no frame
        self.nome.focus() # Para que o foco do rato vá a esta Entry no inicio
        self.nome.grid(row=1, column=1)

        # Label Preço
        self.etiqueta_preco = Label(frame, text="Preço: ", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_preco.grid(row=2, column=0)

        # Entry Preço (caixa de texto que irá receber o preço)
        self.preco = Entry(frame, font=('Calibri', 13)) # Caixa de texto (input de texto) localizada no frame
        self.preco.grid(row=2, column=1)

        # Botão Adicionar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text = "Guardar Produto", command = self.add_produto, style='my.TButton')
        self.botao_adicionar.grid(row = 3, columnspan = 2, stick = W + E)

        # Mensagem informativa para o utilizador
        self.mensagem = Label(text = '', fg = 'red')
        self.mensagem.grid(row = 3, column = 0, columnspan = 2, stick = W + E)

        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri, 11')) # MOdifica-se a fonte da tabela
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold')) # Modifica-se a fonte das cabeceiras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'stick': 'nswe'})]) # Eliminar as bordas

        # Estrutura da Tabela
        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        self.tabela.heading('#0', text = 'Nome', anchor = CENTER) # Cabeçalho 0
        self.tabela.heading('#1', text = 'Preco', anchor = CENTER) # Cabeçalho 1

        # Botão de Eliminar e Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        botao_eliminar = ttk.Button(text = 'ELIMINAR', command = self.del_produto, style='my.TButton')
        botao_eliminar.grid(row = 5, column = 0, sticky = W + E)
        botao_editar = ttk.Button(text = 'EDITAR', command = self.edi_produto, style='my.TButton')
        botao_editar.grid(row = 5, column = 1, sticky = W + E)

        # Chamada ao método get_produtos() para obter a listagem de produtos ao ínicio da app
        self.get_produtos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con: # Iniciamos uma conexão com a base de dados(alias com)
            cursor = con.cursor() # Criamos um cursor da conexão para poder operar na base de dados
            resultado = cursor.execute(consulta, parametros) # Preparar a consulta SQL (com parametro se os há)
            con.commit() # Executar a consulta SQL preprarada anteriormente
        return resultado # Restituir o resultado da consulta SQL

    def get_produtos(self):
        # O primeiro, ao indicar a app, vamos limpar a tabela se tiver dados residuais ou antigos
        registros_tabela = self.tabela.get_children() # Obter todos os dados da tabela
        for linha in registros_tabela:
            self.tabela.delete(linha)

        # Consulta SQL
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registros_db = self.db_consulta(query) # Faz-se a chamada ao método db_consulta

        # Escrever os dados no ecrã
        for linha in registros_db:
            print(linha) # print para verificar por consola os dados
            self.tabela.insert('', 0, text = linha[1], values = linha[2])
    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)' # Consulta SQL (sem os dados)
            parametros = (self.nome.get(), self.preco.get()) # Parametro da consulta SQL
            self.db_consulta(query, parametros)
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get()) # Label localizada entre o botão e a tabela
            self.nome.delete(0, END) # Apagar o campo nome do formulaário
            self.preco.delete(0, END) # Apagar o campo preço do formulário

            # Para debug
            #print(self.nome.get())
            #print(self.preco.get())
        elif self.validacao_nome() and self.validacao_preco() == False:
            print("O preço é obrigatório")
            self.mensagem['text'] = 'O preço é obrigatório'
        elif self.validacao_nome() == False and self.validacao_preco():
            print("O nome é obrigatório")
            self.mensagem['text'] = 'O nome é obrigatório'
        else:
            print("O nome e o preço são obrigatórios")
            self.mensagem['text'] = 'O nome e o preço são obrigatórios'

        self.get_produtos() # Quando se finalizar a inserção de dados voltamos a invocar este método para atualizar o conteúdo e ver as alterações

    def del_produto(self):
        print(self.tabela.item(self.tabela.selection()))
        print(self.tabela.item(self.tabela.selection())['text'])
        print(self.tabela.item(self.tabela.selection())['values'])
        print(self.tabela.item(self.tabela.selection())['values'][0])

        self.mensagem['text'] = '' # Mensagem inicialmente vazio
        # Comprovação de que se selecione um produto para poder eliminá-lo
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = 'DELETE FROM produto WHERE nome = ?' # Consulta SQL
        self.db_consulta(query, (nome,)) # Executar a consulta
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        self.get_produtos() # Atualizar a tabela de produto

    def edi_produto(self):
        self.mensagem['text'] = '' # Mensagem inicialmente vazia
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        nome = self.tabela.item((self.tabela.selection()))['text']
        old_preco = self.tabela.item(self.tabela.selection())['values'][0] # preço encontra-se dentro de uma lista

        # Janela nova (editar produto)
        self.janela_editar = Toplevel() # Criar uma janela à frente da principal
        self.janela_editar.title("Editar Produto") # Título da janela
        self.janela_editar.resizable(1,1) # Ativar a redimensão da janela. Para desativá-la: (0,0)
        self.janela_editar.wm_iconbitmap('recursos/icon.ico') # Ícone da janela

        titulo = Label(self.janela_editar, text='Edição de Produtos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Criação do recipiente Frame da janela de Editar Produto
        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto", font=('Calibri', 16, 'bold')) # frame_ep: Frame Editar Produto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nome antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_nome_antigo.grid(row=2, column=0) # Posicionamento através de grid
        # Entry Nome antigo ( texto que não se poderá modificar)
        self.input__nome__antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome), state='readonly', font=('Calibri', 13))
        self.input__nome__antigo.grid(row=2, column=1)

        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ", font=('Calibri', 13))
        self.etiqueta_nome_novo.grid(row=3, column=0)
        # Entry Nome novo (texto que se poderá modificar)
        self.input__nome__novo = Entry(frame_ep, font=('Calibri', 13))
        self.input__nome__novo.grid(row=3, column=1)
        self.input__nome__novo.focus() # Para que a seta do rato vá a esta Entry ao inicio

        # Label Preço antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ", font=('Calibri', 13)) # Etiqueta de texto localizada no frame
        self.etiqueta_preco_antigo.grid(row=4, column=0) # Posicionamento através de grid
        # Entry Preço antigo (texto que se poderá modificar)
        self.input__preco__antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco), state='readonly', font=('Calibri', 13))
        self.input__preco__antigo.grid(row=4, column=1)

        # Label Preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ", font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (texto que se poderá modificar)
        self.input__preco__novo = Entry(frame_ep, font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", style='my.TButton', command=lambda:
                                          self.atualizar_produtos(self.input__nome__novo.get(),
                                                                  self.input__nome__antigo.get(),
                                                                  self.input__preco__antigo.get()))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (tetxo que se poderá modificar)
        self.input__preco__novo = Entry(frame_ep)
        self.input__preco__novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", style='my.TButton', command=lambda:
                                          self.atualizar_produto(self.input__nome__novo.get(),
                                                                  self.input__nome__antigo.get(),
                                                                  self.input__preco__novo.get(),
                                                                  self.input__preco__antigo.get()))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)

    def atualizar_produto(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '' and novo_preco != '':
            # Se o utulizador escreve novo nome e novo preco, mudam-se ambos
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            # Seo o utilizador deixa vazio o novo preço, mantém-se o preço anterior
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            # Se o utilizador deixa vazio o novo nome, mantem-se o nome anterior
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True

        if (produto_modificado):
            self.db_consulta(query, parametros) # Executar a consulta
            self.janela_editar.destroy() # Fechar a janela de edição de produtos
            self.mensagem['text'] = 'O produto {} foi atualizado com êxito'.format(antigo_nome) # Mostrar mensagem para o utilizador
            self.get_produtos() # Atualizar a tabela de produtos
        else:
            self.janela_editar.destroy() # Fechar a janela de edição de produtos
            self.mensagem['text'] = 'O produto {} NÃO foi atualizado'.format(antigo_nome) # Mostrar mensagem para o utilizador


if __name__ == '__main__':
    root = Tk() # Instância da janela principal
    app = Produto(root) # Envia=se para a classe Produto o controle sobre a janela root
    root.mainloop() # Começamos o ciclo de aplicação, é como um while True

