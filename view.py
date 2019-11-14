####################################################################################################################
#
#
#			SIMULADOR DE MÁQUINA NORMA
#
#Desenvolvido por: guilthys@gmail.com
#Trabalho de TCC - ES - Unipampa/Alegrete 2019
#
#
#Esse Codigo  não tem restrições de uso - Desenvolvido com fins academicos e de Ensino
#
# Sinta-se livre para altera a sintaxe, as funcionalidades, e que isso sirva a seu aprendizado.
# Existem limitações e cenarrios não testado(Explorar todos é inviavel devido a tempo),
# portanto erros podem ocorrer durate sua utilização
####################################################################################################################



#imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import*
from time import strftime
from PIL import Image
from PIL import ImageTk
import main
import webbrowser


HEIGHT = 768
WIDTH = 1366

NORM_FONT= ("Symbol", 8)
root = tk.Tk()
root.title("SimNor 1.0")
root.geometry('1366x768')
ico = PhotoImage(file = 'icones/post.png')
root.tk.call('wm', 'iconphoto', root._w, ico)



canvas = tk.Canvas(root, bg ='#FDF5E6', height=HEIGHT, width=WIDTH)
canvas.pack(expand = YES, fill = BOTH)


FONT_T = IntVar()
FONT_T.set(10)
var = IntVar()
var.set(1)



varDebug = BooleanVar()
varDebug.set(False)









# ------------- Functions Interface ----------------------------------------------

def getRadio():
	selection = '\n  O simulador está usando as Regras Lógicas:  '
	if var.get() == 1: 
		selection += ' Básicas.'
	else: 
		selection += ' Avançadas.'
	label.insert("end-1c", selection)



def clearCode():
	textinput.delete('1.0', 'end-1c')



def clear_lower():
	label.delete('1.0', 'end-1c')


#Se except criar erro (Erro basico ao fechar ignorado)
def openArquivo():
	try:
		fileName = filedialog.askopenfilename(title = "Select File",filetypes = (("txt files","*.txt"),("all files","*.*")))
		if fileName != '':
			code = main.readFile(fileName)
			textinput.delete('1.0', 'end-1c')
			textinput.insert("end-1c", code)
	except Exception as e:
		pass

def saveArquivo():

	try:
		fileName = filedialog.asksaveasfile(title = 'Save File',mode = 'w', confirmoverwrite = True, defaultextension = '.txt', filetypes = (("txt files","*.txt"),("all files","*.*")))
		if fileName != '':
			code = textinput.get("1.0", 'end-1c')
			fileName.write(code.rstrip())
	except Exception as e:
		pass
		





def lerRegraB():
	info = 'Regras Basicas. \n\n\n  O simulador trabalha com dois conjuntos de regras lógicas! \n\n As Regras Básicas e  Regras Avançadas!. \n\n\n Dentro do conjunto de regras basicas tem-se os operadores codicionais \n \n "== " Que verifica a igualdade entre dois elementos retornado True ou False. \n \n" != "Que verifica se dois elementos são diferentes, retornado True ou False.\n\n\n OBS: Somente é possivel usar == ou != em conjunto com if (a==b) ou while(a != 0).'
	popupmsg_regras(info)

def lerRegraA():
	info = 'Regras Avançadas. \n\n\n  O simulador trabalha com dois conjuntos de regras lógicas!\n\n As Regras Básicas e as Regras Avançadas!. \n\n\n Dentro do conjunto de regras avançados tem-se os operadores codicionais \n \n "== " Que verifica a igualdade entre dois elementos retornado True ou False. \n \n" != "Que verifica se dois elementos são diferentes, retornado True ou False. \n\n "<" Que verifica se  a é menor que b, "a < b", retornado True ou False. \n\n ">" Que verifica se "a" é maior que "b", isto é, "a > b", retornado True ou False. \n\n "<=" Que verifica se "a" é menor igual que "b", isto é " a <= b " retornado True ou False. \n\n ">=" Que verifica se "a" é maior ou igual a "b", isto é " a >= b ", retornado True ou False. \n\n OBS: Somente é possivel usar == , !=  <, >, <= ou >= em conjunto com if (a==b) ou while(a != 0).\n\n'
	popupmsg_regras(info)



def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("Erro")
	label = Label(popup, text=msg, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = Button(popup, text="Ok", command = popup.destroy)
	B1.pack()
	popup.mainloop()




def popupmsg_regras(msg):
	popup = tk.Tk()
	popup.wm_title("Regras Simulador")
	label = Label(popup, text=msg, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = Button(popup, text="Ok", command = popup.destroy)
	B1.pack()
	popup.mainloop()


def inputUse():
	entrada = textinput.get("1.0", 'end-1c')
	execultaSimuldor(entrada)


def execultaSimuldor(code):
	try:
		result = ' \n ************************************* SimNor ************************************* \n'  + '>>Return main::  '+ str(main.executa(code, var.get()))
		label.insert("end-1c", result)
	except RuntimeError as e:
		label.insert("end-1c", ' \n ************************************* SimNor ************************************* \n'+ '>>Return main::  ' +str(e))
	except Exception as e:
		label.insert("end-1c", ' \n ************************************* SimNor ************************************* \n'+ '>>Return main::  ' +str(e))


def execultaSimuldorVerificar(code):
	try:
		result = ' \n ************************************* SimNor ************************************* \n'  + '>>Return main::  '+ str(main.executaVerificar(code, var.get()))
		label.insert("end-1c", result)
	except RuntimeError as e:
		label.insert("end-1c", ' \n ************************************* SimNor ************************************* \n'+ '>>Return main::  ' +str(e))
	except Exception as e:
		label.insert("end-1c", ' \n ************************************* SimNor ************************************* \n'+ '>>Return main::  ' +str(e))



def verificar():
	entrada = textinput.get("1.0", 'end-1c')
	execultaSimuldorVerificar(entrada)



def undo():
	textinput.event_generate("<<Undo>>")
	return

def redo():
	textinput.event_generate("<<Redo>>")
	return


def debug():
	try:
		entrada = textinput.get("1.0", 'end-1c')
		main.execultaDebug(entrada, var.get())

		
		debug_message  = main.readFile('parselog.txt')


		root2 = tk.Tk()
		root2.title("SimNor 1.0")
		root2.geometry('1366x768')
		
		ico2 = PhotoImage(file = 'post.png')
		root2.tk.call('wm', 'iconphoto', root2._w, ico2)
		canvas = tk.Canvas(root2, bg ='#FDF5E6', height=HEIGHT, width=WIDTH)
		canvas.pack(expand = YES, fill = BOTH)



		label3 = tk.Label(root2, text = " DEBUG PLY ", bg='#FDF5E9')
		label3.place(relx=0.40, rely=0.01)
		frame1 = tk.Frame(root2, bg='#FDF5E9', bd=5)
		frame1.place(relx=0.53, rely=0.03, relwidth=0.95, relheight=0.95, anchor='n')

		textinput1 = tk.Text(frame1, font=(NORM_FONT, 15))
		textinput1.place(relwidth=0.95, relheight=0.95)

		textinput1.insert("end-1c", debug_message)


		scrollBar_input1 = tk.Scrollbar(frame1 )
		scrollBar_input1.place(relx=0.96, rely = 0.01, relwidth=0.018)

		scrollBar_input1.config(command=textinput1.yview)
		textinput1.config(yscrollcommand=scrollBar_input1.set)



		root2.mainloop()



		
	except Exception as e:
		label.insert("end-1c", ' \n ************************************* SimNor ************************************* \n'+ '>>Return main::  ' +str(e))

	






#creantin Menubar
menubar = tk.Menu(root, bd=2)


#Adding file Menu and commands


icone_file = PhotoImage(file = 'icones/iconfinder_file-code.png')
icone_open = PhotoImage(file = 'icones/iconfinder_open-file.png')
icone_save = PhotoImage(file = 'icones/iconfinder_floppy.png')
icone_git = PhotoImage(file = 'icones/iconfinder_github.png')
icone_docum = PhotoImage(file = 'icones/iconfinder_document.png')
icone_exit = PhotoImage(file = 'icones/iconfinder_Cancel.png')
icone_help = PhotoImage(file = 'icones/iconfinder_help.png')
icone_regras = PhotoImage(file = 'icones/iconfinder_weather.png')
icone_undo = PhotoImage(file = 'icones/iconfinder_Undo.png')
icone_redo = PhotoImage(file = 'icones/iconfinder_Redo.png')





file = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'ARQUIVO', compound= tk.LEFT, menu = file, font = NORM_FONT)
file.add_command(label = 'NOVO ARQUIVO', image = icone_file, compound = tk.LEFT, font = NORM_FONT, command = lambda: clearCode())
file.add_command(label = 'ABRIR', image = icone_open, compound = tk.LEFT, font = NORM_FONT, command = lambda: openArquivo())
file.add_command(label = 'SALVAR',  image = icone_save, compound = tk.LEFT,font = NORM_FONT, command = lambda: saveArquivo())
file.add_separator()
file.add_command(label = 'EXIT', image =icone_exit, compound=tk.LEFT, font = NORM_FONT, command = root.destroy)



#Adding Regras 
regra = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='REGRAS', compound=tk.LEFT, menu = regra, font = NORM_FONT)
regra.add_command(label = 'R. AVANÇADA', font = NORM_FONT ,command = lambda: lerRegraA())
regra.add_command(label = 'R. BÁSICA', font = NORM_FONT, command = lambda: lerRegraB())




#Adding Help Menu and commands

help_ = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'AJUDA', compound=tk.LEFT, font = NORM_FONT,  menu = help_)
help_.add_command(label = 'SINTAXE', font = NORM_FONT,  command = lambda: webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/wiki/Sintaxe---SIMNOR'))
help_.add_command(label = 'EXEMPLOS', font = NORM_FONT, command = lambda : webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/wiki/Exemplos'))
help_.add_separator()
help_.add_command(label = 'ISSUES/GIT',  image = icone_git, compound = tk.LEFT, command = lambda : webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/issues'))


#__________________________________________________________________________________________________________

#Icones menu com imagens






icone_exec = PhotoImage(file = 'icones/iconfinder_play.png')
icone_verifica = PhotoImage(file = 'icones/iconfinder_ok.png')
icone_bug = PhotoImage(file='icones/iconfinder_bug.png')
icone_broom = PhotoImage(file='icones/broom-icon.png')



menubar.add_command(image= icone_undo, command= undo)
menubar.add_command(image = icone_redo, command= redo)
menubar.add_command(label ='MAIN',compound=tk.LEFT, font=NORM_FONT, image = icone_broom, command= clear_lower)
menubar.add_command(label= '                             ', state = DISABLED)
menubar.add_command(label= 'VERIFICAR'  , font= NORM_FONT, compound = tk.LEFT, image =icone_verifica,command=verificar)
menubar.add_command(label= 'EXECUTAR', font= NORM_FONT, compound = tk.LEFT, image =icone_exec, command=inputUse)
menubar.add_command(label='DEBUG',font= NORM_FONT, compound = tk.LEFT, image =icone_bug, command=debug)

#___________________________________________________________

















label2 = tk.Label(root, text = " CÓDIGO-FONTE ", font =("Symbol", 12), bg='#FDF5E9')
label2.place(relx=0.40, rely=0.008)


#label4 = tk.Label(root, text = "______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________", bg='#FDF5E9')
#label4.place(relx=0.0, rely=0.745)


label2 = tk.Label(root, text = " RESULTADO MAIN",  font =("Symbol", 12), bg='#FDF5E9')
label2.place(relx=0.40, rely=0.75)



label3 = tk.Label(root, text = " @Licença livre: Desenvolvido por GuilhermeSSouza - Software Engineer", bg='#FDF5E9')
label3.place(relx=0.30, rely=0.976)

frame = tk.Frame(root, bg='#FDF5E9', bd=5)
frame.place(relx=0.53, rely=0.03, relwidth=0.85, relheight=0.7, anchor='n')



sty = ttk.Style()
sty.configure('Wild.TRadiobutton',    # First argument is the name of style. Needs to end with: .TRadiobutton
        background='#FDF5E9',         # Setting background to our specified color above
        foreground='black',
        font = ("Symbol", 8)
        )


#RadioButtom
R2 = Radiobutton(root, text="R.AVANÇADA",  variable=var, value=2, command=getRadio, style = 'Wild.TRadiobutton')
R2.place(relx = 0, rely = 0.04, anchor = NW)


R1 = Radiobutton(root,text="R.BÁSICA", variable=var, value=1, command=getRadio, style = 'Wild.TRadiobutton')
R1.place(relx = 0, rely = 0.08, anchor = NW )











#Input text code

textinput = tk.Text(frame, font=("Times", "17", "bold italic"), undo=True, autoseparators=True, maxundo=-1)
textinput.place(relwidth=0.96, relheight=1)




scrollBar_input = tk.Scrollbar(frame)
scrollBar_input.place(relx=0.97, rely = 0, relwidth=0.018)

scrollBar_input.config(command=textinput.yview)
textinput.config(yscrollcommand=scrollBar_input.set)



#Show result code compile
lower_frame = tk.Frame(root, bg='#FDF5E9', bd=3)
lower_frame.place(relx=0.53, rely=0.78, relwidth=0.85, relheight=0.2, anchor='n')

label = tk.Text(lower_frame, bg = '#ffffff', font = (NORM_FONT, 15))
label.place(relwidth=0.96, relheight=1)



scrollBar = tk.Scrollbar(lower_frame)
scrollBar.place(relx=0.97, rely = 0.01, relwidth=0.018)

scrollBar.config(command=label.yview)
label.config(yscrollcommand=scrollBar.set)



root.config(menu = menubar)
root.mainloop()