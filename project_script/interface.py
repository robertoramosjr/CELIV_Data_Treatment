from tkinter import ttk, Frame, Label, filedialog as fd, Tk, Button, Entry, LabelFrame
from tkinter.ttk import Notebook
from ramp_time_treatment import *
from light_intensity_and_delay_time_treatment import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def file_path_dark():
    global filedark1
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    filedark1 = fd.askopenfilename(title='Open dark CELIV file', initialdir='/',
                                   filetypes=filetypes).replace('/', '\\')
    return filedark1


def file_path_photo():
    global filephoto1
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    filephoto1 = fd.askopenfilename(title='Open Photo-CELIV file',
                                    initialdir='/', filetypes=filetypes).replace('/', '\\')
    return filephoto1


def file_path_light_intensity():
    global filelight
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    filelight = fd.askopenfilename(title='Open light intensity CELIV file', initialdir='/',
                                   filetypes=filetypes).replace('/', '\\')
    return filelight


def file_path_outrace():
    global fileoutrace
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    fileoutrace = fd.askopenfilename(title='Open outrace CELIV file', initialdir='/',
                                     filetypes=filetypes).replace('/', '\\')
    return fileoutrace


def get_input_valeues():
    global area, espessura2
    initialr = int(entryvar.get())
    finalr = int(entryvar2.get())
    rampr = int(entryvar3.get())
    archiven = int(entryvar4.get())
    area = float(secao_transversal.get())
    espessura2 = float(espessura.get())
    arqdark = savefile1.get()
    arqphoto = savefile2.get()
    fig2 = calculos(area, espessura2, initialr, finalr, rampr, archiven, filedark1, filephoto1, arqdark, arqphoto)
    grafico(fig2)


def grafico(fig2):
    imgplot = FigureCanvasTkAgg(fig2, framePlot1)
    imgplot.get_tk_widget().pack(expand=1, fill="both")


def get_input_velues1():
    rate = float(entryframevar1.get())
    lightintensities = int(entryframevar21.get())
    measuremeants1 = int(entryframevar31.get())
    firstdelay = float(entryframevar.get())
    lastdelay = float(entryframevar2.get())
    howmanydelays = int(entryframevar3.get())
    measuremeants2 = int(entryframevar4.get())
    area = float(secao_transversal.get())
    espessura2 = float(espessura.get())
    file1 = savedeltalight.get()
    file2 = savenulight.get()
    file3 = savedeltaoutrace.get()
    file4 = savenuoutrace.get()
    fig = calculos2(area, espessura2, rate,measuremeants1 ,lightintensities,measuremeants2,
                    firstdelay, lastdelay, howmanydelays, file1, file3, file2, file4,filelight,fileoutrace)
    grafico1(fig)


def grafico1(fig):
    imgplot1 = FigureCanvasTkAgg(fig, framePlot2)
    imgplot1.get_tk_widget().pack(fill="both", expand=1)


# Janela principal

Janela = Tk()
Janela.title("CELIV DATA PROCESSING")
Janela.geometry("1000x600")
Janela.resizable(0,0)
Janela.configure(background="white")

tabControl: Notebook = ttk.Notebook(Janela)
tabControl.pack(expand=1, fill="both")

tab1 = Frame(tabControl, bg="white", relief="solid")
tab2 = Frame(tabControl, bg="white", relief="solid")
tab3 = Frame(tabControl, bg="white", relief="solid")

tab1.pack(expand=1, fill="both")
tab2.pack(expand=1, fill="both")
tab3.pack(expand=1, fill="both")

# aba "ramp time"

tabControl.add(tab1, text="Ramp time")

labelFrameFile1 = Label(tab1, text="Ramp Time Processing", font=('Times 20 bold'), bg="white")
labelFrameFile1.grid(row=0, column=0, padx=20, pady=10)

frameVar1 = Frame(tab1, borderwidth=1, relief="groove", bg="white")
frameFile1 = Frame(tab1, borderwidth=1, relief="groove", bg="white")
framePlot1 = Frame(tab1, borderwidth=1, relief="groove", bg="white")

frameVar1.place(x=20, y=50, width=400, height=350)
frameFile1.place(x=20, y=415, width=400, height=120)
framePlot1.place(x=440, y=50, width=540, height=485)

nomeFile1 = Label(frameFile1, text="Select a Dark-CELIV file:", font="Tmes 12", bg="white")
nomeFile2 = Label(frameFile1, text="Select a Photo-CELIV file:", font="Tmes 12", bg="white")
nomeFile1.place(x=10, y=5)
nomeFile2.place(x=10, y=60)

open_button = Button(frameFile1, text='Open Files', command=file_path_dark, width=20)
open_button2 = Button(frameFile1, text='Open Files', command=file_path_photo, width=20)
open_button.place(x=20, y=30)
open_button2.place(x=20, y=85)

frameVar1label = Label(frameVar1, text="Ramp Time Variables:", font=('Times 18'), bg="white").place(x=7, y=10)
frameVar1label1 = Label(frameVar1, text="Inform the first ramp value :", font=('Times 13'), bg="white").place(x=10,
                                                                                                              y=60)
frameVar1label2 = Label(frameVar1, text="Inform the last ramp value :", font=('Times 13'), bg="white").place(x=10,
                                                                                                             y=130)
frameVar1label3 = Label(frameVar1, text="Inform the ramp rate :", font=('Times 13'), bg="white").place(x=10, y=200)
frameVar1label4 = Label(frameVar1, text="How many measurements there is in the file?", font=('Times 13'),
                        bg="white").place(x=10, y=260)

unidade = Label(frameVar1, text="(V/s)", font=('Times 13'), bg="white").place(x=160, y=160)
unidade2 = Label(frameVar1, text="(V/s)", font=('Times 13'), bg="white").place(x=160, y=230)
unidade3 = Label(frameVar1, text="(V/s)", font=('Times 13'), bg="white").place(x=160, y=90)

entryvar = Entry(frameVar1, bg="#F2F2F2", borderwidth=2, font="Times 11")
entryvar2 = Entry(frameVar1, bg="#F2F2F2", borderwidth=2, font="Times 11")
entryvar3 = Entry(frameVar1, bg="#F2F2F2", borderwidth=2, font="Times 11")
entryvar4 = Entry(frameVar1, bg="#F2F2F2", borderwidth=2, font="Times 11")

entryvar.place(x=10, y=90)
entryvar2.place(x=10, y=160)
entryvar3.place(x=10, y=230)
entryvar4.place(x=10, y=300)

calcbutt1 = Button(frameFile1, text="Calculate", command=get_input_valeues)
calcbutt1.place(x=250, y=85)

# aba "light intensity and outrace"

tabControl.add(tab2, text="Light Intensity and Outrace")

labelFrameFile2 = Label(tab2, text="Light Intensity and Outrace Processing", font=('Times 20 bold'), bg="white")
labelFrameFile2.grid(row=0, column=0, padx=20, pady=10)

frameVar21 = Frame(tab2, borderwidth=1, relief="groove", bg="white")
frameVar22 = Frame(tab2, borderwidth=1, relief="groove", bg="white")
frameFile2 = Frame(tab2, borderwidth=1, relief="groove", bg="white")
framePlot2 = Frame(tab2, borderwidth=1, relief="groove", bg="white")

frameVar21.place(x=20, y=50, width=190, height=350)
frameVar22.place(x=220, y=50, width=190, height=350)
frameFile2.place(x=20, y=415, width=390, height=120)
framePlot2.place(x=420, y=50, width=560, height=485)

nomeFile1 = Label(frameFile2, text="Select a Light Intensity CELIV file:", font="Tmes 12 ", bg="white")
nomeFile2 = Label(frameFile2, text="Select a Outrace CELIV file:", font="Tmes 12", bg="white")
nomeFile1.place(x=10, y=5)
nomeFile2.place(x=10, y=60)

open_button = Button(frameFile2, text='Open Files', width=20, command= file_path_light_intensity)
open_button2 = Button(frameFile2, text='Open Files', width=20, command= file_path_outrace)
open_button.place(x=20, y=30)
open_button2.place(x=20, y=85)

frameVar21label = Label(frameVar22, text="Outrace Variables:", font=('Times 13'), bg="white")
frameVar21label1 = Label(frameVar22, text="Inform the frist delay time:", font=('Times 12'), bg="white")
frameVar21label2 = Label(frameVar22, text="Inform the last delay time:", font=('Times 12'), bg="white")
frameVar21label3 = Label(frameVar22, text="How many delay times \n were used? ", font=('Times 12'), bg="white")
frameVar21label4 = Label(frameVar22, text="How many measurements\n there is in the file?", font=('Times 12'),
                         bg="white")

frameVar21label.place(x=7, y=10)
frameVar21label1.place(x=10, y=60)
frameVar21label2.place(x=10, y=120)
frameVar21label3.place(x=10, y=180)
frameVar21label4.place(x=10, y=255)

entryframevar = Entry(frameVar22, bg="#F2F2F2", borderwidth=2, font=" Times 12")
entryframevar2 = Entry(frameVar22, bg="#F2F2F2", borderwidth=2, font=" Times 12")
entryframevar3 = Entry(frameVar22, bg="#F2F2F2", borderwidth=2, font=" Times 12")
entryframevar4 = Entry(frameVar22, bg="#F2F2F2", borderwidth=2, font=" Times 12")

entryframevar.place(x=10, y=90, )
entryframevar2.place(x=10, y=150)
entryframevar3.place(x=10, y=225)
entryframevar4.place(x=10, y=300)

frameVar22label = Label(frameVar21, text="Light Intensity Variables:", font=('Times 13'), bg="white")
frameVar22label1 = Label(frameVar21, text="Ramp rate (V/s):", font=('Times 12'), bg="white")
frameVar22label2 = Label(frameVar21, text="How many light \n intensities were used?", font=('Times 12'), bg="white")
frameVar22label3 = Label(frameVar21, text="How many measurements \n there is in the file?", font=('Times 12'),
                         bg="white")

frameVar22label.place(x=7, y=10)
frameVar22label1.place(x=10, y=65)
frameVar22label2.place(x=10, y=120)
frameVar22label3.place(x=10, y=200)

entryframevar1 = Entry(frameVar21, bg="#F2F2F2", borderwidth=2, font=" Times 12")
entryframevar21 = Entry(frameVar21, bg="#F2F2F2", borderwidth=2, font=" Times 12")
entryframevar31 = Entry(frameVar21, bg="#F2F2F2", borderwidth=2, font=" Times 12")

entryframevar1.place(x=10, y=95, )
entryframevar21.place(x=10, y=175)
entryframevar31.place(x=10, y=250)

calcbutt2 = Button(frameFile2, text="Calculate", command=get_input_velues1)
calcbutt2.place(x=250, y=85)

# aba "settins"

tabControl.add(tab3, text="Settings")

labelFrameFile3 = Label(tab3, text="Settings", font=('Times 20 bold'), bg="white")
labelFrameFile3.grid(row=0, column=0, padx=20, pady=10, stick="w")

frameVar3 = Frame(tab3, borderwidth=1, relief="groove", bg="white")
frameFile3 = LabelFrame(tab3, text="Ramp Time File Saving", borderwidth=1, relief="groove", bg="white")
frameFile32 = LabelFrame(tab3, text="Light Intensity and Outrace File Saving", borderwidth=1, relief="groove",
                         bg="white")

frameVar3.place(x=20, y=50, width=260, height=480)
frameFile3.place(x=300, y=42, width=680, height=200)
frameFile32.place(x=300, y=250, width=680, height=280)

nomestting1 = Label(frameVar3, text="Enter the cross-sectional area \n of the sample:", font="Tmes 12 ", bg="white")
nomesetting2 = Label(frameVar3, text="Enter the thickiness of the sample:", font="Tmes 12", bg="white")
nomestting1.place(x=10, y=5)
nomesetting2.place(x=10, y=83)

secao_transversal = Entry(frameVar3, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=25)
espessura = Entry(frameVar3, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=25)
secao_transversal.place(x=10, y=50)
espessura.place(x=10, y=120)

sla1 = Label(frameVar3, text="(cm^2)", bg="white")
sla2 = Label(frameVar3, text="(nm)", bg="white")
sla1.place(x=215, y=53)
sla2.place(x=220, y=123)

savefile1 = Entry(frameFile3, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savefile2 = Entry(frameFile3, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savefile1.place(x=15, y=50)
savefile2.place(x=15, y=120)

savefile11 = Label(frameFile3, text="Enter delta j save file name:", bg="white", font=" Times 14")
savefile22 = Label(frameFile3, text="Enter n and u save file name:", bg="white", font="Times 14")
savefile11.place(x=10, y=10)
savefile22.place(x=10, y=85)

savedeltalight = Entry(frameFile32, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savenulight = Entry(frameFile32, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savedeltaoutrace = Entry(frameFile32, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savenuoutrace = Entry(frameFile32, bg="#F2F2F2", borderwidth=2, font=" Times 12", width=80)
savedeltalight.place(x=15, y=50)
savenulight.place(x=15, y=120)
savedeltaoutrace.place(x=15, y=190)
savenuoutrace.place(x=15, y=260)

savename1 = Label(frameFile32, text="Enter light intendity delta j save file name:", bg="white", font=" Times 14")
savename2 = Label(frameFile32, text="Enter light intensity n and u save file name:", bg="white", font="Times 14")
savename3 = Label(frameFile32, text="Enter Outrace delta j save file name:", bg="white", font=" Times 14")
savename4 = Label(frameFile32, text="Enter Outrace n and u save file name:", bg="white", font="Times 14")
savename1.place(x=10, y=10)
savename2.place(x=10, y=85)
savename3.place(x=10, y=160)
savename4.place(x=10, y=235)

Janela.mainloop()
