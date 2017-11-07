#coding: utf-8

from appJar import gui
import MySQLdb

def entrar(btn):
	global cursor
	global conexao

	host = login.getEntry("Host")
	usuario = login.getEntry("Usuario")
	senha = login.getEntry("Senha")

	try:
		conexao = MySQLdb.connect(host, usuario, senha, "mundo")
		cursor = conexao.cursor()

	except MySQLdb.Error as err:
		print err

	login.stop()

login = gui("Login", "400x200")

login.addLabelEntry("Host")
login.addLabelEntry("Usuario")
login.addSecretLabelEntry("Senha")

login.addButton("Entrar", entrar)

login.go()



#conexao = MySQLdb.connect("192.168.56.104","va1-user","va1-user","mundo")
# conexao.select_db("mundo")
#cursor = conexao.cursor()

#cursor.execute("SELECT * FROM Pais;")
# pegar o primeiro resultado
#result1 = cursor.fetchone()
# pegar todos os resultados
#result = cursor.fetchall()

app = gui("Conexao Mundo","600x300")

def usando(btn):
	# print "Você me usou!"
	pass


def exibir(btn):
	cursor.execute(
		"SELECT NCidade, NEstado, NPais FROM Cidade " +
		"INNER JOIN Estado ON Estado.idEstado = Cidade.Estado_idEstado " +
		"INNER JOIN Pais ON Estado.Pais_idPais = idPais;"

	)

	rs = cursor.fetchall()

	app.clearListBox("lBusca")

	for x in rs:
		app.addListItem("lBusca", x[0] + ' - ' + x[1] + ' - ' + x[2])

def atualizar(btn):
	app.showSubWindow("atualizar_pesquisa")

def atualizar_estado(btn):
	pesquisa_antiga = app.getEntry("pesquisa_antiga")
	pesquisa_nova = app.getEntry("pesquisa_nova")
	id_pesquisa = app.getEntry("id_pesquisa")

	cursor.execute(
		"SELECT idCidade, NCidade FROM Cidade WHERE NCidade LIKE '%" + pesquisa_antiga + "%'"
	)

	rs = cursor.fetchone()

	app.clearListBox("lBusca")

	app.addListItem("lBusca", "A cidade " + rs[1] + " foi atualizada para " + pesquisa_nova + " com o ID Estado" + id_pesquisa + " !")

	cursor.execute(
		"UPDATE Cidade "+
		"SET Estado_idEstado = " + id_pesquisa + ", NCidade = '" + pesquisa_nova + "'"
		"WHERE idCidade = " + str(rs[0])
	)

	conexao.commit()

	app.hideSubWindow("atualizar_pesquisa")






def inserir(btn):
	app.showSubWindow('janela_inserir')

def salvar_estado(btn):
	Cidade = app.getEntry('txtcidade')
	idEstado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (NCidade, Estado_idEstado) VALUES('{}',{})".format(Cidade,idEstado))
	#cursor.execute("INSERT INTO Cidade (NCidade, Estado_idEstado) VALUES('%s',%s)" % (Cidade,idEstado))
	conexao.commit()

	app.clearListBox("lBusca")
	app.addListItem("lBusca", "A cidade " + Cidade + " foi inserida com sucesso!")

	app.hideSubWindow('janela_inserir')

def excluir(btn):
	app.showSubWindow("excluir_cidade")

def excluir_estado(btn):
	ncidade_excluir = app.getEntry("cidadeExcluir")

	cursor.execute(
		"SELECT idCidade, NCidade FROM Cidade WHERE NCidade LIKE '%" + ncidade_excluir + "%'"
	)

	rs = None
	rs = cursor.fetchone()

	app.clearListBox("lBusca")

	app.addListItem("lBusca", "A cidade " + rs[1] + " foi excluida!")

	cursor.execute(
		"DELETE FROM Cidade WHERE idCidade = %s" % (rs[0])
	)

	conexao.commit()

	app.hideSubWindow("excluir_cidade")

def pesquisar(btn):
	termo = app.getEntry("txtBusca")
	if  termo == '':
		app.errorBox("Erro",'Informe um termo para pesquisar!')
	else:
		# SELECT * FROM Cidade WHERE NomeCidade LIKE '%Belo%'
		cursor.execute("SELECT NCidade,NEstado FROM Cidade "+
			"INNER JOIN Estado ON Estado.idEstado = Cidade.Estado_idEstado "
			+ "WHERE NCidade LIKE '%" + termo + "%'" )
		rs = cursor.fetchall()


		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca",x[0] + ' - ' + x[1])
		#app.addListItems("lBusca",rs)

	
# this is a pop-up (Abrir janela inserir)
app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()

#menu
app.addLabel("lNome",'',0,0,2)

app.addButton("Exibir dados",exibir,1,0)
app.addButton("Inserir dado",inserir,1,1)
app.addButton("Atualizar dado",atualizar,2,0)
app.addButton("Excluir dado",excluir,2,1)

app.addEntry("txtBusca",3,0,2)
app.setEntryDefault("txtBusca", "Digite o termo...")
app.addButton("Pesquisar",pesquisar, 4,0,2)
app.addListBox("lBusca",[],5,0,2)
app.setListBoxRows("lBusca",5)
#x = app.textBox("Nome", "Informe seu nome")
#app.setLabel("lNome","Bem-vindo "+x)

#Janela Atualizar ---------------
app.startSubWindow("atualizar_pesquisa", modal=True)

app.addLabel("lUpdate", "Atualizar cidade: ")

app.addEntry("pesquisa_antiga")
app.addEntry("pesquisa_nova")
app.addEntry("id_pesquisa")

app.addButton("Atualizar Cidade", atualizar_estado)

app.setEntryDefault("pesquisa_antiga", "Cidade para alterar")
app.setEntryDefault("pesquisa_nova", "Novo Nome")
app.setEntryDefault("id_pesquisa", "Novo ID Estado")

app.stopSubWindow()

# Janela Excluir
app.startSubWindow("excluir_cidade", modal=True)

app.addLabel("lExcluir", "Excluir cidade: ")

app.addEntry("cidadeExcluir")
app.addButton("Excluir Cidade", excluir_estado)
app.setEntryDefault("cidadeExcluir", "Nome Cidade")

app.stopSubWindow()



app.go()
