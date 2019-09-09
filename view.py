#imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import*
from time import strftime
#from PIL import Image, ImageTk
import main
import webbrowser


HEIGHT = 768
WIDTH = 1366

NORM_FONT= ("Verdana", 10)

root = tk.Tk()
root.title("SimNor 1.0 - Em desenvolvimento")
root.geometry('1366x768')
ico = PhotoImage(file = 'post.png')
root.tk.call('wm', 'iconphoto', root._w, ico)



# def resize_image(event):
# 	new_width = event.width
# 	new_height = event.height
# 	image = copy_of_image.resize((new_width, new_height))
# 	photo = ImageTk.PhotoImage(image)
# 	label.config(image = photo)
# 	label.image = photo

# image = Image.open('post-nuvem.png')
# copy_of_image = image.copy()
# photo = ImageTk.PhotoImage(image)
# label = Label(root, image = photo)
# label.bind('<Configure>', resize_image)
# label.pack(fill=BOTH, expand = YES)


canvas = tk.Canvas(root, bg ='#FDF5E6', height=HEIGHT, width=WIDTH)
canvas.pack(expand = YES, fill = BOTH)

FONT_T = IntVar()
FONT_T.set(10)
var = IntVar()
var.set(1)



varDebug = BooleanVar()
varDebug.set(False)


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

def openArquivo():
	try:
		fileName = filedialog.askopenfilename(title = "Select File",filetypes = (("txt files","*.txt"),("all files","*.*")))
		code = main.readFile(fileName)
		textinput.delete('1.0', 'end-1c')
		textinput.insert("end-1c", code)
	except Exception as e:
		popupmsg('Erro ao abrir o ARQUIVO')

def saveArquivo():

	try:
		fileName = filedialog.asksaveasfile(title = 'Save File',mode = 'w', confirmoverwrite = True, defaultextension = '.txt', filetypes = (("txt files","*.txt"),("all files","*.*")))
		code = textinput.get("1.0", 'end-1c')
		fileName.write(code.rstrip())
	except Exception as e:
		popupmsg('Erro ao salvar o ARQUIVO')





def lerRegraB():
	info = 'Regras Basicas. \n\n\n  O simulador trabalha com dois conjuntos de regras lógicas! \n\n As Regras Básicas e  Regras Avançadas!. \n\n\n Dentro do conjunto de regras basicas tem-se os operadores codicionais \n \n "== " Que verifica a igualdade entre dois elementos retornado True ou False. \n \n" != "Que verifica se dois elementos são diferentes, retornado True ou False.\n\n\n OBS: Somente é possivel usar == ou != em conjunto com if (a==b) ou while(a != 0).'
	popupmsg_regras(info)

def lerRegraA():
	info = 'Regras Avançadas. \n\n\n  O simulador trabalha com dois conjuntos de regras lógicas!\n\n As Regras Básicas e as Regras Avançadas!. \n\n\n Dentro do conjunto de regras avançados tem-se os operadores codicionais \n \n "== " Que verifica a igualdade entre dois elementos retornado True ou False. \n \n" != "Que verifica se dois elementos são diferentes, retornado True ou False. \n\n "<" Que verifica se  a é menor que b, "a < b", retornado True ou False. \n\n ">" Que verifica se "a" é maior que "b", isto é, "a > b", retornado True ou False. \n\n "<=" Que verifica se "a" é menor igual que "b", isto é " a <= b " retornado True ou False. \n\n ">=" Que verifica se "a" é maior ou igual a "b", isto é " a >= b ", retornado True ou False. \n\n OBS: Somente é possivel usar == , !=  <, >, <= ou >= em conjunto com if (a==b) ou while(a != 0).\n\n'
	popupmsg_regras(info)



# def zoom_Mais():
# 	t = FONT_T.get()
# 	t += 1
# 	FONT_T.set(t)
# 	code = textinput.get("1.0", 'end-1c')

# 	clearCode()
# 	label = Label(, text = code, font = ('Verdana',FONT_T.get()))
# 	textinput.insert("end-1c", code)
# 	label['text'] = FONT_T.get()

# def zoom_Menos():
# 	t = FONT_T.get()
# 	t -= 1
# 	FONT_T.set(t)
# 	code = textinput.get("1.0", 'end-1c')
# 	clearCode()
# 	label = Label(textinput, text = code, font = ('Verdana', FONT_T.get()))
# 	textinput.insert("end-1c", label)
# 	label['text'] = label
	



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
	result = ' \n ************************************* SimNor ************************************* \n'  + '>>Return main::  '+ str(main.executa(code, var.get()))
	label.insert("end-1c", result)




def debugButtom(debug):
	dado = '\n'
	if debug == 1 :
		varDebug.set(False)
	else:
		varDebug.set(True)
	dado+= str(varDebug.get())
	label.insert("end-1c",dado)



#creating tkinter window



#creantin Menubar
menubar = tk.Menu(root)


#Adding file Menu and commands

file = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'File', menu = file, font = NORM_FONT)
file.add_command(label = 'Clear', font = NORM_FONT, command = lambda: clearCode())
file.add_command(label = 'Open',  font = NORM_FONT, command = lambda: openArquivo())
file.add_command(label = 'Save',  font = NORM_FONT, command = lambda: saveArquivo())
file.add_separator()
file.add_command(label = 'Exit',  font = NORM_FONT, command = root.destroy)



#Adding Regras 
regra = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Regras', menu = regra, font = NORM_FONT)
regra.add_command(label = 'R. Avançadas', font = NORM_FONT ,command = lambda: lerRegraA())
regra.add_command(label = 'R. Básicas', font = NORM_FONT, command = lambda: lerRegraB())


#Adding Zoom +
# Zoom_1 = tk.Menu(menubar, tearoff = 0)
# menubar.add_cascade(label = 'Zoom', font = NORM_FONT,  menu = Zoom_1)
# Zoom_1.add_command(label = 'Zoom +', font = NORM_FONT, command = lambda: zoom_Mais())
# Zoom_1.add_command(label = 'Zoom -', font = NORM_FONT, command = lambda: zoom_Menos())




#Adding Help Menu and commands

help_ = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Help', font = NORM_FONT,  menu = help_)
help_.add_command(label = 'Sintaxe', font = NORM_FONT,  command = lambda: webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/wiki/Sintaxe---SIMNOR'))
help_.add_command(label = 'Exemplos', font = NORM_FONT, command = lambda : webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/wiki/Exemplos'))
help_.add_separator()
help_.add_command(label = 'Issues/Git', command = lambda : webbrowser.open('https://github.com/GuilhermeSSouza/SimNor/issues'))




label2 = tk.Label(root, text = " CÓDIGO-FONTE ", bg='#FDF5E9')
label2.place(relx=0.40, rely=0.01)


label2 = tk.Label(root, text = " RESULTADO MAIN", bg='#FDF5E9')
label2.place(relx=0.40, rely=0.75)

frame = tk.Frame(root, bg='#FDF5E9', bd=5)
frame.place(relx=0.53, rely=0.03, relwidth=0.85, relheight=0.7, anchor='n')



#background_image = tk.PhotoImage(file="post-nuvem.png")
#background_label = tk.Label(canvas, image=background_image)
#background_label.place(relwidth=0, relheight=0)




#RadioButtom
R2 = Radiobutton(root, text="R. Avançada", variable=var, value=2, command=getRadio)
R2.place(relx = 0.01, rely = 0.04, anchor = NW )


R1 = Radiobutton(root,text="R. Básica", variable=var, value=1, command=getRadio)
R1.place(relx = 0.01, rely = 0.08, anchor = NW )











#Input text code

textinput = tk.Text(frame, font=(NORM_FONT, 15) )
textinput.place(relwidth=0.80, relheight=1)

scrollBar_input = tk.Scrollbar(frame)
scrollBar_input.place(relx=0.81, rely = 0.01, relwidth=0.03)

scrollBar_input.config(command=textinput.yview)
textinput.config(yscrollcommand=scrollBar_input.set)



#main buutoms simulador

button = tk.Button(frame, bg = '#32CD32', text="Executar", font=(NORM_FONT, 15), command = inputUse)
button.place(relx=0.85, rely = 0.85, relheight=0.15, relwidth=0.15)
button = tk.Button(frame, bg = '#FFFF00', text="Verificar", font=(NORM_FONT, 15), command = None)
button.place(relx=0.85, rely = 0.45, relheight=0.15, relwidth=0.15)
button = tk.Button(frame, bg = '#FF0000', text="Debug", font=(NORM_FONT, 15), command = lambda: debugButtom(varDebug.get()))
button.place(relx=0.85, rely = 0, relheight=0.15, relwidth=0.15)




#Show result code compile
lower_frame = tk.Frame(root, bg='#FDF5E9', bd=3)
lower_frame.place(relx=0.53, rely=0.78, relwidth=0.85, relheight=0.2, anchor='n')

label = tk.Text(lower_frame, bg = '#ffffff', font = (NORM_FONT, 15))
label.place(relwidth=0.80, relheight=1)


scrollBar = tk.Scrollbar(lower_frame)
scrollBar.place(relx=0.81, rely = 0.01, relwidth=0.03)

scrollBar.config(command=label.yview)
label.config(yscrollcommand=scrollBar.set)



button = tk.Button(lower_frame, bg = '#BDB76B', text="Clear", font=(NORM_FONT, 15), command = lambda: clear_lower())
button.place(relx=0.85, rely = 0.45, relheight=0.55, relwidth=0.15)






root.config(menu = menubar)
root.mainloop()