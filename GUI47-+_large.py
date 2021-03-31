#なぜかわからないけど閉じれるようになった…(?)　
#終了ボタンつけておいた方がいいと思ったけど結局変化なし いい方法探す？
#２回よみこみver.一旦完成 +縦軸1元素で規格化 +増えてくプログレスバー +平均の範囲指定(三角グラフ) +カウント数範囲指定(三角グラフのとこのボックス参照)で組成分布
#                       +三角グラフ上の点押したらその点赤くなって誤差表示(ターミナルに1SD表示) +参照値 +表設置(値は適当 設置だけ)→邪魔だから一旦非表示 +三角グラフから範囲指定してそのデータのみをいじれる(黄色ウィンドウ)
#                       +頂点に元素和とれるように(緑色ウィンドウ) +三角グラフ上の点押したらその点の信号をグラフ表示(ブランク引いた値)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import pathlib
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import tkinter.filedialog
import pickle
import os
from tkinter import colorchooser
import sys
import glob
import re

#起動遅くなるから関数の中に持っていく？(めんどくさそう)
#アプリ化する時に下のやつに書き換える
f=open("c:/python/elementlist.binaryfile","rb")
element_list = pickle.load(f)
#print(element_list)
#アプリの絶対パスを取得してバイナリファイルを開く　elementlist.binaryfileをアプリ化したファイルに入れること！
#this_file = os.path.abspath("myapp.exe") #←アプリ名決まったら書き換える exeファイルは個々の名前と同じにする アプリ化の際pythonfileの名前も変えないと後からいじれない
#this_folder = this_file.replace("myapp.exe","")
#f = open("{}elementlist.binaryfile".format(this_folder),"rb")
#element_list = pickle.load(f)

Atomic_Symbol_list = list(set(element_list["Atomic Symbol"]))  #読み取れるようになればいらない(もういらなくなってると思う)

#ソフトの色とフォント変えるところ
color1="#ccccff" #背景
color2="#a3d1ff" #入力部分
color3="#b7ffb7" #三角グラフ背景
color4="#b7ffff" #三角柱グラフ背景
color5="#ffd6ad" #個数分布グラフ背景
color6="#ffbcff" #カウントグラフ背景
color7="#ffffc1" #新しいウィンドウ背景
color8="#ccffe5" #頂点編集するウィンドウ背景
label_font="Calibri"
label_font_jp="BIZ UDPゴシック"

#設定で変えられるものの初期値
color_fig="white"
color_axes_pre="white"#グラフ表示していない状態での軸とかの色
color_axes="black"#グラフ表示時の軸とかの色
graph_font="Arial"#グラフのフォント
color_plot="blue"#プロットの色
alpha_plot=0.5 #プロットの透明度(0-1)
color_bar="green"#棒グラフの色
bar_style="枠あり"#棒グラフの見た目 周り囲うかどうか
weight_font="bold"
size_plot=35 #プロットのサイズ

plt.rcParams["font.weight"] = weight_font #今は変えられない　変えられるようにするならフォントみたいにグラフかく関数それぞれに入れる
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams["axes.labelsize"] = 15
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"
plt.rcParams["xtick.major.size"] = 5
plt.rcParams["ytick.major.size"] = 5
plt.rcParams["xtick.major.pad"] = 2
plt.rcParams["ytick.major.pad"] = 2
plt.rcParams["xtick.major.width"] = 1.5
plt.rcParams["ytick.major.width"] = 1.5

#参照値リスト
sansyou_1_a = ""
sansyou_1_b = ""
sansyou_1_c = ""
sansyou_1_sa = ""
sansyou_1_sb = ""
sansyou_1_sc = ""
sansyou_2_a = ""
sansyou_2_b = ""
sansyou_2_c = ""
sansyou_2_sa = ""
sansyou_2_sb = ""
sansyou_2_sc = ""
sansyou_3_a = ""
sansyou_3_b = ""
sansyou_3_c = ""
sansyou_3_sa = ""
sansyou_3_sb = ""
sansyou_3_sc = ""

sansyou_4_1_a = ""
sansyou_4_1_b = ""
sansyou_4_1_c = ""
sansyou_4_1_sa = ""
sansyou_4_1_sb = ""
sansyou_4_1_sc = ""
sansyou_4_2_a = ""
sansyou_4_2_b = ""
sansyou_4_2_c = ""
sansyou_4_2_sa = ""
sansyou_4_2_sb = ""
sansyou_4_2_sc = ""
sansyou_4_3_a = ""
sansyou_4_3_b = ""
sansyou_4_3_c = ""
sansyou_4_3_sa = ""
sansyou_4_3_sb = ""
sansyou_4_3_sc = ""

#範囲指定リスト(機能してない気がする)
hanni_a_1 = ""
hanni_a_2 = ""
hanni_b_1 = ""
hanni_b_2 = ""
hanni_c_1 = ""
hanni_c_2 = ""
triangle_plot = ""

#頂点設定
#元素リスト
ele_p1 = "-"
ele_p2 = "-"
ele_p3 = "-"
ele_p4 = "-"
ele_p5 = "-"
ele_p6 = "-"
ele_p7 = "-"
ele_p8 = "-"
ele_p9 = "-"
ele_p10 = "-"
ele_p_list = []
#質量数リスト
mass_p1 = "-"
mass_p2 = "-"
mass_p3 = "-"
mass_p4 = "-"
mass_p5 = "-"
mass_p6 = "-"
mass_p7 = "-"
mass_p8 = "-"
mass_p9 = "-"
mass_p10 = "-"
mass_p_list = []
#補正項リスト
cor_p1 = ""
cor_p2 = ""
cor_p3 = ""
cor_p4 = ""
cor_p5 = ""
cor_p6 = ""
cor_p7 = ""
cor_p8 = ""
cor_p9 = ""
cor_p10 = ""
cor_p_list = []

root=tk.Tk()
root.title(u"分析ソフト")
root.geometry("1850x980")
root.configure(bg=color1)

frame3=tk.Canvas(root,width=315,height=285,bg=color2)
frame3.place(x=8,y=28)

textframe=tk.Frame(root,width=150,height=35,bg=color2)
textframe.place(x=120,y=40)
textBox2=tk.Entry(textframe)
textBox2.place(width=145,height=20,x=0,y=0)
scrollbar=tk.Scrollbar(textframe,command=textBox2.xview,orient=tk.HORIZONTAL)
scrollbar.place(width=145,height=12,x=0,y=22)
textBox2["xscrollcommand"]=scrollbar.set

combobox2=ttk.Combobox(root,state="readonly",values=[])
combobox2.place(width=40,height=20,x=120,y=145)
combobox3=ttk.Combobox(root,state="readonly",values=[])
combobox3.place(width=40,height=20,x=170,y=145)
combobox4=ttk.Combobox(root,state="readonly",values=[])
combobox4.place(width=40,height=20,x=220,y=145)

combobox5=ttk.Combobox(root,state='readonly',values=[])
combobox5.place(width=40,height=20,x=120,y=100)
combobox6=ttk.Combobox(root,state='readonly',values=[])
combobox6.place(width=40,height=20,x=170,y=100)
combobox7=ttk.Combobox(root,state='readonly',values=[])
combobox7.place(width=40,height=20,x=220,y=100)

combobox8=ttk.Combobox(root,state='readonly',values=[])
combobox8.place(width=40,height=20,x=110,y=550)
combobox9=ttk.Combobox(root,state='readonly',values=[])
combobox9.place(width=40,height=20,x=110,y=580)


frame1=tk.Canvas(root,width=652,height=652,bg=color3)
frame1.place(x=334,y=22)
frame4=tk.Canvas(root,width=610,height=321,bg=color5)
frame4.place(x=996,y=22)
frame5=tk.Canvas(root,width=610,height=321,bg=color6)
frame5.place(x=996,y=353)
frame1_5=tk.Canvas(root,width=550,height=290,bg=color3)
frame1_5.place(x=334,y=684)

frame6=tk.Canvas(root,width=71,height=20,bg=color3)
frame6.place(x=16,y=326)
frame7=tk.Canvas(root,width=84,height=20,bg=color4)
frame7.place(x=16,y=406)
frame8=tk.Canvas(root,width=61,height=20,bg=color5)
frame8.place(x=16,y=516)
frame9=tk.Canvas(root,width=84,height=20,bg=color6)
frame9.place(x=16,y=656)

fig5=plt.figure(figsize=(6,3.11))
fig5.subplots_adjust(bottom=0.2,left=0.16)
ax5=fig5.add_subplot(111)
ax5.spines['top'].set_color("w")
ax5.spines['bottom'].set_color("w")
ax5.spines['left'].set_color("w")
ax5.spines['right'].set_color("w")
ax5.tick_params(colors="w")
canvas5=FigureCanvasTkAgg(fig5,master=root)
canvas5.get_tk_widget().place(x=1003,y=29)
canvas5._tkcanvas.place(x=1003,y=29)

fig6=plt.figure(figsize=(6,3.11))
fig6.subplots_adjust(bottom=0.2,left=0.16)
ax6=fig6.add_subplot(111)
ax6.spines['top'].set_color("w")
ax6.spines['bottom'].set_color("w")
ax6.spines['left'].set_color("w")
ax6.spines['right'].set_color("w")
ax6.tick_params(colors="w")
canvas6=FigureCanvasTkAgg(fig6,master=root)
canvas6.get_tk_widget().place(x=1003,y=360)
canvas6._tkcanvas.place(x=1003,y=360)

fig1_5=plt.figure(figsize=(5.4,2.8))
fig1_5.subplots_adjust(bottom=0.2,left=0.15,right=0.75,top=0.9)
ax1_5=fig1_5.add_subplot(111)
ax1_5.spines['top'].set_color("w")
ax1_5.spines['bottom'].set_color("w")
ax1_5.spines['left'].set_color("w")
ax1_5.spines['right'].set_color("w")
ax1_5.tick_params(colors="w")
canvas1_5=FigureCanvasTkAgg(fig1_5,master=root)
canvas1_5.get_tk_widget().place(x=341,y=691)
canvas1_5._tkcanvas.place(x=341,y=691)

"""
list_1 = [0,1,2,3,4,5,6,7,8,9]
list_2 = [10,11,12,13,14,15,16,17,18,19]
list_3 = [20,21,22,23,24,25,26,27,28,29]
list_4 = [30,31,32,33,34,35,36,37,38,39]

num_hyou_list = len(list_1)

canvas_hyou0 = tkinter.Canvas(root,width=637,height=20,bg=color1)
canvas_hyou0.place(x=334,y=696)
canvas_hyou = tkinter.Canvas(root,width=637,height=145,bg=color1)
canvas_hyou.place(x=334,y=716)

vbar_hyou = tkinter.ttk.Scrollbar(root,orient=tkinter.VERTICAL)
vbar_hyou.place(x=971,y=716,height=145)

vbar_hyou.config(command=canvas_hyou.yview)
canvas_hyou.config(yscrollcommand=vbar_hyou.set)

sc_hgt = int(150/7*(num_hyou_list))
canvas_hyou.config(scrollregion=(0,0,500,sc_hgt))

def mousewheel(event):
    canvas_hyou.yview_scroll(int(-1*(event.delta/120)),"units")

canvas_hyou.bind_all("<MouseWheel>",mousewheel)

frame_hyou0 = tkinter.Frame(canvas_hyou0,bg=color1)
frame_hyou = tkinter.Frame(canvas_hyou,bg=color1)

canvas_hyou0.create_window((0,0),window=frame_hyou0,anchor=tkinter.NW,width=canvas_hyou0.cget("width"))
canvas_hyou.create_window((0,0),window=frame_hyou,anchor=tkinter.NW,width=canvas_hyou.cget("width"))

e0 = tkinter.Label(frame_hyou0,width=22,text="元素A (%)",background="white")
e0.grid(row=1,column=0,padx=0,pady=0,ipadx=0,ipady=0)
e1 = tkinter.Label(frame_hyou0,width=22,text="元素B (%)",background="white")
e1.grid(row=1,column=1,padx=0,pady=0,ipadx=0,ipady=0)
e2 = tkinter.Label(frame_hyou0,width=22,text="元素C (%)",background="white")
e2.grid(row=1,column=2,padx=0,pady=0,ipadx=0,ipady=0)
e3 = tkinter.Label(frame_hyou0,width=22,text="counts",background="white")
e3.grid(row=1,column=3,padx=0,pady=0,ipadx=0,ipady=0)

irow = 2
irow0 = 2
erow = num_hyou_list+irow0
while irow < erow:
    if irow%2==0:
        color="#cdfff7"
    else:
        color="white"
    
    a1 = str(list_1[irow-irow0])
    b1 = tkinter.Label(frame_hyou,width=22,text=a1+"±"+a1,background=color)
    b1.grid(row=irow,column=1,padx=0,pady=0,ipadx=0,ipady=0)
    a2 = str(list_2[irow-irow0])
    b2 = tkinter.Label(frame_hyou,width=22,text=a2+"±"+a2,background=color)
    b2.grid(row=irow,column=2,padx=0,pady=0,ipadx=0,ipady=0)
    a3 = str(list_3[irow-irow0])
    b3 = tkinter.Label(frame_hyou,width=22,text=a3+"±"+a3,background=color)
    b3.grid(row=irow,column=3,padx=0,pady=0,ipadx=0,ipady=0)
    a4 = list_4[irow-irow0]
    b4 = tkinter.Label(frame_hyou,width=22,text=a4,background=color)
    b4.grid(row=irow,column=4,padx=0,pady=0,ipadx=0,ipady=0)

    irow = irow+1
"""

def click_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes = [("CSV(*.csv)","*.csv")])
    print(file_path)
    textBox2.delete(0, tkinter.END)
    textBox2.insert(tkinter.END,file_path)    


def click_element():
    global combobox5
    global combobox6   
    global combobox7
    global ele_list_min
    global ele_list
    global mass_list

    if not textBox2.get()=="":
        try:
            data_csv = pd.read_csv(textBox2.get())
            """
            data_NaN=data_csv.loc[:,data_csv.iloc[1].isnull()]
            header=data_NaN.columns
            header_number=header[0].replace("Unnamed: ","")
            isotope_number=int(header_number)-1
            """
            #isotope_df=data_csv.iloc[1,1:isotope_number+1]
            isotope_df_0=data_csv.columns
            data_csv_skip_column = int(data_csv.columns.get_loc("skip"))
            #isotope_df=isotope_df_0[1:len(isotope_df_0)-1]
            isotope_df=isotope_df_0[1:data_csv_skip_column-1]
            isotope_list=isotope_df.values.tolist()
            print(isotope_list)
            ele_list=[]
            for i in range(0,len(isotope_list)):
                alpha_i="".join([s for s in isotope_list[i] if s.isalpha()])
                ele_list.append(alpha_i)
            print(ele_list)
            mass_list=[]
            for i in range(0,len(isotope_list)):
                digit_i="".join([s for s in isotope_list[i] if s.isdigit()])
                mass_list.append(digit_i)
            print(mass_list)
            ele_list_min=list(set(ele_list))
            ele_list_min.sort()
            print(ele_list_min)
            combobox5=ttk.Combobox(root,state='readonly',values=ele_list_min)
            combobox5.current(0)
            combobox5.place(width=40,height=20,x=120,y=100)
            combobox6=ttk.Combobox(root,state='readonly',values=ele_list_min)
            combobox6.current(0)
            combobox6.place(width=40,height=20,x=170,y=100)
            combobox7=ttk.Combobox(root,state='readonly',values=ele_list_min)
            combobox7.current(0)
            combobox7.place(width=40,height=20,x=220,y=100)
        except:
            messagebox.showerror('エラー','正しい形式のファイルを選択してください')    
    else:
        messagebox.showerror('エラー','ファイルを選択してください')

def click1():
   global combobox2
   global combobox3   
   global combobox4
   global mass_list_tB4
   global mass_list_tB5
   global mass_list_tB6

   if combobox5.get()=="" or combobox6.get()=="" or combobox7.get()=="":
       messagebox.showerror('エラー','元素を３か所すべてに入力してください') #多分絶対このエラー出ない
   elif combobox5.get()==combobox6.get() or combobox6.get()==combobox7.get() or combobox5.get()==combobox7.get():
       messagebox.showerror('エラー','元素を重複なく選択してください')
   elif not combobox5.get() in Atomic_Symbol_list or not combobox6.get() in Atomic_Symbol_list or not combobox7.get() in Atomic_Symbol_list: #読み取れるようになればいらない
       messagebox.showerror('エラー','元素を正しく入力してください') #多分絶対このエラー出ない
   else:
       iso_list_tB4 = [k for k, x in enumerate(ele_list) if x == combobox5.get()]
       mass_list_tB4=[]
       for i in range(0,len(iso_list_tB4)):
           iso_index_i = iso_list_tB4[i]
           mass_i = mass_list[int(iso_index_i)]
           mass_list_tB4.append(mass_i)
       print(mass_list_tB4) 
       iso_list_tB5 = [k for k, x in enumerate(ele_list) if x == combobox6.get()]
       mass_list_tB5=[]
       for i in range(0,len(iso_list_tB5)):
           iso_index_i = iso_list_tB5[i]
           mass_i = mass_list[int(iso_index_i)]
           mass_list_tB5.append(mass_i)
       print(mass_list_tB5) 
       iso_list_tB6 = [k for k, x in enumerate(ele_list) if x == combobox7.get()]
       mass_list_tB6=[]
       for i in range(0,len(iso_list_tB6)):
           iso_index_i = iso_list_tB6[i]
           mass_i = mass_list[int(iso_index_i)]
           mass_list_tB6.append(mass_i)
       print(mass_list_tB6) 
       combobox2=ttk.Combobox(root,state='readonly',values=mass_list_tB4)
       combobox2.current(0)
       combobox2.place(width=40,height=20,x=120,y=145)
       combobox3=ttk.Combobox(root,state='readonly',values=mass_list_tB5)
       combobox3.current(0)
       combobox3.place(width=40,height=20,x=170,y=145)
       combobox4=ttk.Combobox(root,state='readonly',values=mass_list_tB6)
       combobox4.current(0)
       combobox4.place(width=40,height=20,x=220,y=145)

def pbar():

    global barframe
    barframe = tk.Frame(root,width=315,height=100,bg=color1)
    barframe.place(x=10,y=850)

    sample_label_long = textBox2.get()
    print(sample_label_long)
    #sample_label  = sample_label_long[:-8]
    #ample_label  = sample_label_long[:-16]
    sample_label  = sample_label_long[:-22]
    print(sample_label)

    all_file = glob.glob(sample_label+"0*.csv")
    print(all_file)
    data_num = len(all_file)

    #sample = ["{}_{}_NP_events".format(sample_label, str(i)) for i in range(1,data_num+1)]
    sample = ["{}_{}_NP_events_large".format(sample_label, str(i)) for i in range(1,data_num+1)]
    print(sample)

    global progressbar
    global maximum_bar
    global value_bar
    progressbar=ttk.Progressbar(barframe,orient="horizontal",length=315,mode="determinate")
    progressbar.pack()
    maximum_bar=0
    value_bar=0
    progressbar.configure(maximum=maximum_bar,value=value_bar)
    
    global bar_text
    bar_text = tk.StringVar()
    bar_text.set("0/"+str(maximum_bar))
    bar_label = tk.Label(barframe,textvariable=bar_text,bg=color1,font=(label_font_jp,10))
    bar_label.pack()

def pb_update():
    progressbar.configure(maximum=maximum_bar,value=value_bar)
    if value_bar == maximum_bar:
        bar_text.set("読み込み中")
    else:
        bar_text.set(str(value_bar)+"/"+str(maximum_bar))
    progressbar.update()

def click2():

    pbar()

    global combobox8
    global combobox9
    global ele_list_min

    if textBox2.get()=="":
        messagebox.showerror('エラー','ファイルを選択してください')

    if combobox2.get()=="":
        messagebox.showerror('エラー','質量数を選択してください')    
    else:
        label4_get=combobox2.get()
        print("label4:"+label4_get)

        label5_get=combobox3.get()
        print("label5:"+label5_get)

        label6_get=combobox4.get()
        print("label6:"+label6_get)

    sample_label_long = textBox2.get()
    print(sample_label_long)
    #sample_label  = sample_label_long[:-8]
    #sample_label  = sample_label_long[:-16]
    sample_label  = sample_label_long[:-22]
    print(sample_label)

    #all_file = glob.glob(sample_label+"_*_NP_events.csv")
    all_file = glob.glob(sample_label+"_*_NP_events_large.csv")
    print(all_file)
    data_num = len(all_file)

    if textBox10.get()=="" or textBox11.get()=="" or textBox12.get()=="":
        messagebox.showerror('エラー','最低カウント数をすべて入力してください')

    #sample = ["{}{}".format(sample_label, str(i).zfill(4)) for i in range(1,data_num+1)]
    #sample = ["{}_{}_NP_events".format(sample_label, str(i)) for i in range(1,data_num+1)]
    sample = ["{}_{}_NP_events_large".format(sample_label, str(i)) for i in range(1,data_num+1)]
    print("sample")
    print(sample)
    print(len(sample))

    global maximum_bar
    maximum_bar = len(sample)

    global data_large
    global data
    
    data_large = pd.DataFrame()
    for run in range(0, len(sample)):
        datasheet1 = "{}.csv".format(sample[run])
        print("\n{}".format(datasheet1))
        try:
            df1 = pd.read_csv(datasheet1, low_memory=False)
            #meas_iso = df1.iloc[1:2, 1:meas_num+1].values.tolist()[0]
            #print("\nmeasured: {}".format(meas_iso))
            data_large = data_large.append(df1, ignore_index=True)
        except FileNotFoundError:
            messagebox.showerror('エラー','選択されたファイルが正しくありません')

    print(data_large)
    data_skip_column = int(data_large.columns.get_loc("skip"))
    data = data_large.iloc[:,0:data_skip_column]
    print(data)

    #tB4_data_1 = data["{}({})".format(combobox5.get(),combobox2.get())]
    #tB5_data_1 = data["{}({})".format(combobox6.get(),combobox3.get())]
    #tB6_data_1 = data["{}({})".format(combobox7.get(),combobox4.get())]
    tB4_data_1 = data["'[{}{}]+'".format(combobox2.get(),combobox5.get())]
    tB5_data_1 = data["'[{}{}]+'".format(combobox3.get(),combobox6.get())]
    tB6_data_1 = data["'[{}{}]+'".format(combobox4.get(),combobox7.get())]
    global data_gattai1
    data_gattai1=pd.concat([tB4_data_1,tB5_data_1,tB6_data_1],axis=1)
    data_gattai1.columns=["{}".format(combobox5.get()),"{}".format(combobox6.get()),"{}".format(combobox7.get())]
    print(data_gattai1)

    iso_list_tB4 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox5.get()]
    mass_list_tB4=[]
    for i in range(0,len(iso_list_tB4)):
        iso_index_i = iso_list_tB4[i]
        massnumber = element_list["Mass Number"]
        mass_i = massnumber[int(iso_index_i)]
        mass_list_tB4.append(mass_i)
    print(mass_list_tB4) 
    iso_list_tB5 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox6.get()]
    mass_list_tB5=[]
    for i in range(0,len(iso_list_tB5)):
        iso_index_i = iso_list_tB5[i]
        massnumber = element_list["Mass Number"]
        mass_i = massnumber[int(iso_index_i)]
        mass_list_tB5.append(mass_i)
    print(mass_list_tB5) 
    iso_list_tB6 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox7.get()]
    mass_list_tB6=[]
    for i in range(0,len(iso_list_tB6)):
        iso_index_i = iso_list_tB6[i]
        massnumber = element_list["Mass Number"]
        mass_i = massnumber[int(iso_index_i)]
        mass_list_tB6.append(mass_i)
    print(mass_list_tB6) 

    Iso_Compo_list = element_list["Isotopic Composition"]
    list_number_tB4 = mass_list_tB4.index(int(combobox2.get()))
    index_tB4 = iso_list_tB4[int(list_number_tB4)]
    iso_compo_tB4 = Iso_Compo_list[int(index_tB4)]
    print("iso_compo_tB4")
    print(iso_compo_tB4)
    list_number_tB5 = mass_list_tB5.index(int(combobox3.get()))
    index_tB5 = iso_list_tB5[int(list_number_tB5)]
    iso_compo_tB5 = Iso_Compo_list[int(index_tB5)]
    print(iso_compo_tB5)
    list_number_tB6 = mass_list_tB6.index(int(combobox4.get()))
    index_tB6 = iso_list_tB6[int(list_number_tB6)]
    iso_compo_tB6 = Iso_Compo_list[int(index_tB6)]
    print(iso_compo_tB6)

    print(textBox30.get())
    if textBox30.get()=="" and textBox31.get()=="" and textBox32.get()=="":
        textBox30.insert(tkinter.END,iso_compo_tB4)
        textBox31.insert(tkinter.END,iso_compo_tB5)
        textBox32.insert(tkinter.END,iso_compo_tB6)
        tB30=iso_compo_tB4
        tB31=iso_compo_tB5
        tB32=iso_compo_tB6
    else:
        tB30=textBox30.get()
        tB31=textBox31.get()
        tB32=textBox32.get()

    print(iso_compo_tB4)

    tB4_data_2 = data["'[{}{}]+'".format(combobox2.get(),combobox5.get())]/float(iso_compo_tB4)*float(textBox30.get())/float(tB30)
    tB5_data_2 = data["'[{}{}]+'".format(combobox3.get(),combobox6.get())]/float(iso_compo_tB4)*float(textBox30.get())/float(tB31)
    tB6_data_2 = data["'[{}{}]+'".format(combobox4.get(),combobox7.get())]/float(iso_compo_tB4)*float(textBox30.get())/float(tB32)
    global data_gattai2
    data_gattai2=pd.concat([tB4_data_2,tB5_data_2,tB6_data_2],axis=1)
    data_gattai2.columns=["{}".format(combobox5.get()),"{}".format(combobox6.get()),"{}".format(combobox7.get())]
    print(data_gattai2)    

    combobox8=ttk.Combobox(root,state='readonly',values=ele_list_min)#後で変える
    combobox8.current(0)      
    combobox8.place(width=40,height=20,x=110,y=550)
    combobox9=ttk.Combobox(root,state='readonly',values=ele_list_min)
    combobox9.current(1)      
    combobox9.place(width=40,height=20,x=110,y=580)

    label11_2=tk.Label(root,text=combobox5.get()+":",bg=color1,font=(label_font,12))
    label11_2.place(width=20,height=20,x=80,y=690)
    label14_2=tk.Label(root,text=combobox6.get()+":",bg=color1,font=(label_font,12))
    label14_2.place(width=20,height=20,x=80,y=720)
    label17_2=tk.Label(root,text=combobox7.get()+":",bg=color1,font=(label_font,12))
    label17_2.place(width=20,height=20,x=80,y=750)

    ax3.cla()
    ax5.cla()
    ax6.cla()
    ax3.spines['top'].set_color(color_axes_pre)
    ax3.spines['bottom'].set_color(color_axes_pre)
    ax3.spines['left'].set_color(color_axes_pre)
    ax3.spines['right'].set_color(color_axes_pre)
    ax3.tick_params(colors=color_axes_pre)
    ax5.spines['top'].set_color(color_axes_pre)
    ax5.spines['bottom'].set_color(color_axes_pre)
    ax5.spines['left'].set_color(color_axes_pre)
    ax5.spines['right'].set_color(color_axes_pre)
    ax5.tick_params(colors=color_axes_pre)
    ax6.spines['top'].set_color(color_axes_pre)
    ax6.spines['bottom'].set_color(color_axes_pre)
    ax6.spines['left'].set_color(color_axes_pre)
    ax6.spines['right'].set_color(color_axes_pre)
    ax6.tick_params(colors=color_axes_pre)
    canvas3.draw()
    canvas5.draw()
    canvas6.draw()

    barframe.destroy()
    messagebox.showinfo('確認',"ファイル読み込みが完了しました")

#三角柱プロット範囲指定なし
def clickA(): 

    plt.rcParams["font.family"] = graph_font

    #データ決め 
    SUM=data_gattai1[combobox5.get()]/float(textBox30.get())+data_gattai1[combobox6.get()]/float(textBox31.get())+data_gattai1[combobox7.get()]/float(textBox32.get())
    pX=data_gattai1[combobox5.get()]/float(textBox30.get())/SUM*100 
    pY=data_gattai1[combobox6.get()]/float(textBox31.get())/SUM*100
    pZ=data_gattai1[combobox7.get()]/float(textBox32.get())/SUM*100
    data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
    data_concat.columns=['X','Y','Z','SUM']

    data_z_SUM=data_gattai2[combobox5.get()]+data_gattai2[combobox6.get()]+data_gattai2[combobox7.get()]
    data_z_x=data_gattai2[combobox5.get()] #いらない列
    data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
    data_z.columns=['SUM','x']

    h = np.sqrt(3.0)*0.5
   
    #座標・軸決め
    zmax=data_z['SUM'].max()

    amari=zmax%10

    if amari==0:
        baisuu=zmax
    else:
        baisuu=zmax-amari+10

    NP1=np.linspace(0,baisuu,6,dtype=int)

    plotx1=(100-data_concat['Y'])/100-data_concat['X']/200
    ploty1=h*data_concat['X']/100
    plotz1=data_z['SUM']/baisuu 
    data_plot1=pd.concat([plotx1,ploty1,plotz1],axis=1)
    data_plot1.columns=['x1','y1','z1']

    #プロット場所決め
    fig1=plt.figure(figsize=(7.5,7.5))
    ax1=fig1.add_subplot(111,projection='3d')
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    plt.axis('off')
    ax1.view_init(elev=12,azim=-69)
    #三角グラフ描き

    fig1.set_facecolor(color_fig)
    ax1.set_facecolor(color_fig)

    for i in range(1,5):
        ax1.plot([i*2/20.0, 1.0-i*2/20.0],[h*2*i/10.0, h*i*2/10.0],[0,0],color='gray', lw=0.5)
        ax1.plot([i*2/20.0, i*2/10.0],[h*i*2/10.0, 0.0],[0,0], color='gray', lw=0.5)
        ax1.plot([0.5+i*2/20.0, i*2/10.0],[h*(1.0-i*2/10.0), 0.0],[0,0],color='gray', lw=0.5)

    ax1.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
    ax1.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
    ax1.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
    ax1.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
    ax1.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
    ax1.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
    ax1.text(0.5, h+0.15,-0.1, combobox5.get(), fontsize=20,ha="center", color=color_axes)
    ax1.text(-0.15*h, -0.15/2,-0.1, combobox6.get(), fontsize=20,ha="center", color=color_axes)
    ax1.text(1+0.15*h, -0.15/2,-0.1, combobox7.get(), fontsize=20,ha="center", color=color_axes)

    for i in range(1,5):
        ax1.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
        ax1.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
        ax1.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)

    ax1.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
    ax1.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
    ax1.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

    ax1.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

    for i in range(0,6):
       ax1.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

    for i in range(0,6):
       ax1.text(-0.078,-0.078,i/5-0.01,NP1[i],fontsize=20,ha="right", color=color_axes)

    ax1.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？
    
    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1)
    ax1.set_zlim(0,1)

    #プロット
    ax1.scatter(data_plot1["x1"],data_plot1["y1"],data_plot1["z1"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

    #範囲指定のところに値が入っていた場合に全体表示のどの範囲にあたるかを示す
    if not textBox15.get() == "" or not textBox16.get() == "" :
        if textBox15.get()=="":
           tB15="0"
        else:
           tB15=textBox15.get()

        if textBox16.get()=="":
           tB16=baisuu
        else:
           tB16=textBox16.get()

        tB15_range = int(tB15)/baisuu
        tB16_range = int(tB16)/baisuu   

        ax1.plot([0.0, 1.0],[0.0, 0.0],[tB15_range,tB15_range], color="red", lw=1.5)
        ax1.plot([0.0, 0.5],[0.0, h],[tB15_range,tB15_range], color="red", lw=1.5)
        ax1.plot([1.0, 0.5],[0.0, h],[tB15_range,tB15_range], color="red", lw=1.5)
        ax1.plot([0.0, 0.0],[0.0, 0.0],[tB15_range,tB16_range], color="red", lw=1.5)
        ax1.plot([1, 1],[0,0],[tB15_range,tB16_range], color="red", lw=1.5)
        ax1.plot([0.5, 0.5],[h, h],[tB15_range,tB16_range], color="red", lw=1.5)
        ax1.plot([0.0, 1.0],[0.0, 0.0],[tB16_range,tB16_range], color="red", lw=1.5)
        ax1.plot([0.0, 0.5],[0.0, h],[tB16_range,tB16_range], color="red", lw=1.5)
        ax1.plot([1.0, 0.5],[0.0, h],[tB16_range,tB16_range], color="red", lw=1.5)        

    fig1.show()



#三角柱プロット範囲指定あり
def clickD(): 

    plt.rcParams["font.family"] = graph_font

    SUM=data_gattai1[combobox5.get()]/float(textBox30.get())+data_gattai1[combobox6.get()]/float(textBox31.get())+data_gattai1[combobox7.get()]/float(textBox32.get())
    pX=data_gattai1[combobox5.get()]/float(textBox30.get())/SUM*100 
    pY=data_gattai1[combobox6.get()]/float(textBox31.get())/SUM*100
    pZ=data_gattai1[combobox7.get()]/float(textBox32.get())/SUM*100
    data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
    data_concat.columns=['X','Y','Z','SUM']

    data_z_SUM=data_gattai2[combobox5.get()]+data_gattai2[combobox6.get()]+data_gattai2[combobox7.get()]
    data_z_x=data_gattai2[combobox5.get()] #いらない列
    data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
    data_z.columns=['SUM','x']

    h = np.sqrt(3.0)*0.5
     
    #座標決め
    zmax=data_z['SUM'].max()

    amari=zmax%10
    if amari==0:
       baisuu=zmax
    else:
       baisuu=zmax-amari+10

    plotx4=(100-data_concat['Y'])/100-data_concat['X']/200
    ploty4=h*data_concat['X']/100

    if textBox15.get()=="":
       tB15="0"
    else:
       tB15=textBox15.get()

    if textBox16.get()=="":
       tB16=baisuu
    else:
       tB16=textBox16.get()

    if tB15=="0" and tB16==baisuu:
       zvalue=baisuu
       plotz4=data_z['SUM']/zvalue
       NP4=np.linspace(0,baisuu,6,dtype=int)
    else:
       zvalue=int(tB16)-int(tB15)
       plotz4=(data_z['SUM']-int(tB15))/zvalue
       NP4=np.linspace(int(tB15),int(tB16),6,dtype=int) #少数になっちゃう可能性ありそうだけどだいじょうぶかな

    data_plot4=pd.concat([plotx4,ploty4,plotz4],axis=1)
    data_plot4.columns=['x4','y4','z4']
    data_plot40=data_plot4[(data_plot4["z4"]>=0)&(data_plot4["z4"]<=1)]

    #プロット場所決め
    fig4=plt.figure(figsize=(7.5,7.5))
    ax4=fig4.add_subplot(111,projection='3d')
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.set_zticks([])
    plt.axis('off')
    ax4.view_init(elev=12,azim=-69)

    #三角グラフ描き
    fig4.set_facecolor(color_fig)
    ax4.set_facecolor(color_fig)

    for i in range(1,5):
        ax4.plot([2*i/20.0, 1.0-2*i/20.0],[h*2*i/10.0, h*2*i/10.0],[0,0],color='gray', lw=0.5)
        ax4.plot([2*i/20.0, 2*i/10.0],[h*2*i/10.0, 0.0],[0,0], color='gray', lw=0.5)
        ax4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[0,0], color='gray', lw=0.5)

    ax4.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
    ax4.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
    ax4.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
    ax4.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
    ax4.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
    ax4.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
    ax4.text(0.5, h+0.15,-0.1, combobox5.get(), fontsize=20,ha="center", color=color_axes)
    ax4.text(-0.15*h, -0.15/2,-0.1, combobox6.get(), fontsize=20,ha="center", color=color_axes)
    ax4.text(1+0.15*h, -0.15/2,-0.1, combobox7.get(), fontsize=20,ha="center", color=color_axes)

    for i in range(1,5):
        ax4.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
        ax4.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
        ax4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)

    ax4.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
    ax4.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
    ax4.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

    ax4.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

    for i in range(0,6):
       ax4.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

    for i in range(0,6):
       ax4.text(-0.078,-0.078,i/5-0.01,NP4[i],fontsize=20,ha="right", color=color_axes)

    ax4.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？

    ax4.set_xlim(0,1)
    ax4.set_ylim(0,1)
    ax4.set_zlim(0,1)

    #プロット
    ax4.scatter(data_plot40["x4"],data_plot40["y4"],data_plot40["z4"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

    fig4.show()


#三角プロット範囲指定あり
def clickC():

    plt.rcParams["font.family"] = graph_font

    SUM=data_gattai1[combobox5.get()]/float(textBox30.get())+data_gattai1[combobox6.get()]/float(textBox31.get())+data_gattai1[combobox7.get()]/float(textBox32.get())
    pX=data_gattai1[combobox5.get()]/float(textBox30.get())/SUM*100 
    pY=data_gattai1[combobox6.get()]/float(textBox31.get())/SUM*100
    pZ=data_gattai1[combobox7.get()]/float(textBox32.get())/SUM*100
    data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
    data_concat.columns=['X','Y','Z','SUM']

    data_z_SUM=data_gattai2[combobox5.get()]+data_gattai2[combobox6.get()]+data_gattai2[combobox7.get()]
    data_z_x=data_gattai2[combobox5.get()] #いらない列
    data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
    data_z.columns=['SUM','x']           

    zmax=data_z['SUM'].max()

    print(data_z["SUM"].sort_values())

    amari=zmax%10
    if amari==0:
       baisuu=zmax
    else:
       baisuu=zmax-amari+10

    if textBox13.get()=="":
       tB13="0"
    else:
       tB13=textBox13.get()

    if textBox14.get()=="":
       tB14=baisuu
    else:
       tB14=textBox14.get()

    global triangle_plot
    triangle_plot = 1
    #global data_gattai0
    global data_concat0_tri
    if tB13=="0" and tB14==baisuu:
       data_concat0_tri=data_concat
       data_gattai0=data_gattai1
    else:
       data_concat0_tri=data_concat[(data_z["SUM"]>=int(tB13))&(data_z["SUM"]<=int(tB14))]
       data_gattai0=data_gattai1[(data_z["SUM"]>=int(tB13))&(data_z["SUM"]<=int(tB14))]

    print(data_gattai0)
    print(data_concat0_tri)
    print("index list")
    #print(list(data_concat0_tri.index))

    #重み付けなし普通の平均とデータの標準誤差、標準誤差
    #平均値
    mean_data = data_concat0_tri.mean()
    print("平均")
    print(mean_data)
    #標準偏差
    std_data = np.std(data_concat0_tri, ddof=1) #標本標準偏差
    print("標準偏差")
    print(std_data)
    #標準誤差
    ste_data = std_data/(len(data_concat0_tri)**(1/2))
    print("標準誤差")
    print(ste_data)

    #重み付き平均値
    δ_data = data_gattai0**(1/2)
    data_d_X = data_gattai0[combobox5.get()]/float(textBox30.get())
    data_d_Y = data_gattai0[combobox6.get()]/float(textBox31.get())
    data_d_Z = data_gattai0[combobox7.get()]/float(textBox32.get())
    data_d_sum = data_d_X+data_d_Y+data_d_Z
    δ_data_d_X = δ_data[combobox5.get()]/float(textBox30.get())
    δ_data_d_Y = δ_data[combobox6.get()]/float(textBox31.get())
    δ_data_d_Z = δ_data[combobox7.get()]/float(textBox32.get())
    δ_s = (δ_data_d_X**2+δ_data_d_Y**2+δ_data_d_Z**2)**(1/2)
    δ_X = 100*((δ_data_d_X/data_d_X)**2+(δ_s/data_d_sum)**2)**(1/2)
    δ_Y = 100*((δ_data_d_Y/data_d_Y)**2+(δ_s/data_d_sum)**2)**(1/2)
    δ_Z = 100*((δ_data_d_Z/data_d_Z)**2+(δ_s/data_d_sum)**2)**(1/2)
    σ_S = (δ_X**2+δ_Y**2+δ_Z**2)**(1/2)
    w_S = 1/((σ_S)**2)
    data_w_count_X = data_concat0_tri["X"]*w_S
    data_w_count_Y = data_concat0_tri["Y"]*w_S
    data_w_count_Z = data_concat0_tri["Z"]*w_S
    data_ave_w_X = np.sum(data_w_count_X)/np.sum(w_S)
    data_ave_w_Y = np.sum(data_w_count_Y)/np.sum(w_S)
    data_ave_w_Z = np.sum(data_w_count_Z)/np.sum(w_S)
    print("重みつき平均1")
    print("X")
    print(data_ave_w_X)
    print("Y")
    print(data_ave_w_Y)
    print("Z")
    print(data_ave_w_Z)
    #重み付き標準偏差
    data_zansa_X = data_concat0_tri["X"]-data_ave_w_X
    data_zansa_Y = data_concat0_tri["Y"]-data_ave_w_Y
    data_zansa_Z = data_concat0_tri["Z"]-data_ave_w_Z
    data_w_zansa2_X = w_S*(data_zansa_X**2)
    data_w_zansa2_Y = w_S*(data_zansa_Y**2)
    data_w_zansa2_Z = w_S*(data_zansa_Z**2)
    data_std_w_X = (np.sum(data_w_zansa2_X)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
    data_std_w_Y = (np.sum(data_w_zansa2_Y)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
    data_std_w_Z = (np.sum(data_w_zansa2_Z)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
    print("重みつき標準偏差1")
    print("X")
    print(data_std_w_X)
    print("Y")
    print(data_std_w_Y)
    print("Z")
    print(data_std_w_Z)

    print(tB14)
    print(zmax)
    print(data_concat0_tri)
    h = np.sqrt(3.0)*0.5
    
    global data_plot3
    plotx3=(100-data_concat0_tri['Y'])/100-data_concat0_tri['X']/200
    ploty3=h*data_concat0_tri['X']/100
    data_plot3=pd.concat([plotx3,ploty3],axis=1)
    data_plot3.columns=['x3','y3']

    print(data_plot3)

    global data_click
    data_click=pd.concat([data_concat0_tri,data_plot3],axis=1)
    data_click.columns=["a'","b'","c'","sum","x","y"]
    print("data_click")
    print(data_click)

    ax3.cla()
    fig3.set_facecolor(color_fig)
    ax3.set_facecolor(color_fig)

    for i in range(1,10):
        ax3.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], linestyle='dashed',color='gray', lw=0.5)
        ax3.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], linestyle='dashed',color='gray', lw=0.5)
        ax3.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], linestyle='dashed',color='gray', lw=0.5)

    ax3.plot([0.0, 1.0],[0.0, 0.0], color=color_axes, lw=2)
    ax3.plot([0.0, 0.5],[0.0, h], color=color_axes, lw=2)
    ax3.plot([1.0, 0.5],[0.0, h], color=color_axes, lw=2)
  
    ax3.text(0.455, h+0.0283, combobox5.get(), fontsize=22, color=color_axes)
    ax3.text(-0.1, -0.02, combobox6.get(), fontsize=22, color=color_axes)
    ax3.text(1.02, -0.02, combobox7.get(), fontsize=22, color=color_axes)

    for i in range(1,10):
        ax3.text(0.5+(10-i)/20.0+0.016, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize=17, color=color_axes)
        ax3.text((10-i)/20.0-0.082, h*(10-i)/10.0, '%d0' % i, fontsize=17, color=color_axes)
        ax3.text(i/10.0-0.03, -0.06, '%d0' % i, fontsize=17, color=color_axes)

    #ax3.text(0.84,h/2,'%'+combobox5.get(),fontsize=12, color=color_axes)
    #ax3.text(0.08,h/2,'%'+combobox6.get(),fontsize=12, color=color_axes)
    #ax3.text(0.5,-0.11,'%'+combobox7.get(),fontsize=12, color=color_axes)

    ax3.text(-0.15,1,"Number of particles:"+str(len(data_plot3.dropna())),fontsize=14, color=color_axes)

    ax3.scatter(data_plot3["x3"],data_plot3["y3"],c=color_plot,alpha=alpha_plot,s=size_plot)

    if not sansyou_1_a =="":
        plot_sansyou_1_x = (100-float(sansyou_1_b))/100-float(sansyou_1_a)/200
        plot_sansyou_1_y = h*float(sansyou_1_a)/100
        print(plot_sansyou_1_x)
        print(plot_sansyou_1_y)
        global sansyou_1_sa
        global sansyou_1_sb
        global sansyou_1_sc
        if sansyou_1_sa == "":
            sansyou_1_sa = 0
        if sansyou_1_sb == "":
            sansyou_1_sb = 0
        if sansyou_1_sc == "":
            sansyou_1_sc = 0
        ax3.scatter(plot_sansyou_1_x,plot_sansyou_1_y,c="red",alpha=1,s=20)
        ax3.plot([plot_sansyou_1_x+float(sansyou_1_sa)*h/100/h/2,plot_sansyou_1_x-float(sansyou_1_sa)*h/100/h/2],[plot_sansyou_1_y-float(sansyou_1_sa)*h/100,plot_sansyou_1_y+float(sansyou_1_sa)*h/100],color="red",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_1_x-float(sansyou_1_sb)*h/100/h/2,plot_sansyou_1_x+float(sansyou_1_sb)*h/100/h/2],[plot_sansyou_1_y-float(sansyou_1_sb)*h/100,plot_sansyou_1_y+float(sansyou_1_sb)*h/100],color="red",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_1_x-float(sansyou_1_sc)*h/100/h,plot_sansyou_1_x+float(sansyou_1_sc)*h/100/h],[plot_sansyou_1_y,plot_sansyou_1_y],color="red",alpha=0.8,lw=1.2)

    if not sansyou_2_a =="":
        plot_sansyou_2_x = (100-float(sansyou_2_b))/100-float(sansyou_2_a)/200
        plot_sansyou_2_y = h*float(sansyou_2_a)/100
        print(plot_sansyou_2_x)
        print(plot_sansyou_2_y)
        global sansyou_2_sa
        global sansyou_2_sb
        global sansyou_2_sc
        if sansyou_2_sa == "":
            sansyou_2_sa = 0
        if sansyou_2_sb == "":
            sansyou_2_sb = 0
        if sansyou_2_sc == "":
            sansyou_2_sc = 0
        ax3.scatter(plot_sansyou_2_x,plot_sansyou_2_y,c="blue",alpha=1,s=20)
        ax3.plot([plot_sansyou_2_x+float(sansyou_2_sa)*h/100/h/2,plot_sansyou_2_x-float(sansyou_2_sa)*h/100/h/2],[plot_sansyou_2_y-float(sansyou_2_sa)*h/100,plot_sansyou_2_y+float(sansyou_2_sa)*h/100],color="blue",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_2_x-float(sansyou_2_sb)*h/100/h/2,plot_sansyou_2_x+float(sansyou_2_sb)*h/100/h/2],[plot_sansyou_2_y-float(sansyou_2_sb)*h/100,plot_sansyou_2_y+float(sansyou_2_sb)*h/100],color="blue",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_2_x-float(sansyou_2_sc)*h/100/h,plot_sansyou_2_x+float(sansyou_2_sc)*h/100/h],[plot_sansyou_2_y,plot_sansyou_2_y],color="blue",alpha=0.8,lw=1.2)

    if not sansyou_3_a =="":
        plot_sansyou_3_x = (100-float(sansyou_3_b))/100-float(sansyou_3_a)/200
        plot_sansyou_3_y = h*float(sansyou_3_a)/100
        print(plot_sansyou_3_x)
        print(plot_sansyou_3_y)
        global sansyou_3_sa
        global sansyou_3_sb
        global sansyou_3_sc
        if sansyou_3_sa == "":
            sansyou_3_sa = 0
        if sansyou_3_sb == "":
            sansyou_3_sb = 0
        if sansyou_3_sc == "":
            sansyou_3_sc = 0
        ax3.scatter(plot_sansyou_3_x,plot_sansyou_3_y,c="green",alpha=1,s=20)
        ax3.plot([plot_sansyou_3_x+float(sansyou_3_sa)*h/100/h/2,plot_sansyou_3_x-float(sansyou_3_sa)*h/100/h/2],[plot_sansyou_3_y-float(sansyou_3_sa)*h/100,plot_sansyou_3_y+float(sansyou_3_sa)*h/100],color="green",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_3_x-float(sansyou_3_sb)*h/100/h/2,plot_sansyou_3_x+float(sansyou_3_sb)*h/100/h/2],[plot_sansyou_3_y-float(sansyou_3_sb)*h/100,plot_sansyou_3_y+float(sansyou_3_sb)*h/100],color="green",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_3_x-float(sansyou_3_sc)*h/100/h,plot_sansyou_3_x+float(sansyou_3_sc)*h/100/h],[plot_sansyou_3_y,plot_sansyou_3_y],color="green",alpha=0.8,lw=1.2)

    canvas3.draw()

#組成分布
def clickE():
    SUM=data_gattai1[combobox5.get()]/float(textBox30.get())+data_gattai1[combobox6.get()]/float(textBox31.get())+data_gattai1[combobox7.get()]/float(textBox32.get())
    pX=data_gattai1[combobox5.get()]/float(textBox30.get())/SUM*100 
    pY=data_gattai1[combobox6.get()]/float(textBox31.get())/SUM*100
    pZ=data_gattai1[combobox7.get()]/float(textBox32.get())/SUM*100
    data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
    data_concat.columns=['X','Y','Z','SUM']

    data_z_SUM=data_gattai2[combobox5.get()]+data_gattai2[combobox6.get()]+data_gattai2[combobox7.get()]
    data_z_x=data_gattai2[combobox5.get()] #いらない列
    data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
    data_z.columns=['SUM','x']           

    zmax=data_z['SUM'].max()

    amari=zmax%10
    if amari==0:
       baisuu=zmax
    else:
       baisuu=zmax-amari+10

    if textBox13.get()=="":
       tB13="0"
    else:
       tB13=textBox13.get()

    if textBox14.get()=="":
       tB14=baisuu
    else:
       tB14=textBox14.get()

    if tB13=="0" and tB14==baisuu:
       data_concat0=data_concat
    else:
       data_concat0=data_concat[(data_z["SUM"]>=int(tB13))&(data_z["SUM"]<=int(tB14))]


    if textBox18.get()=="":
        tB18="0"
    else:
        tB18=textBox18.get()

    if textBox19.get()=="":
        tB19="100"
    else:
        tB19=textBox19.get()

    if combobox8.get()==combobox5.get():
        if tB18=="0" and tB19=="100":
            data_concat00=data_concat0
        else:
            data_concat00=data_concat0[(data_concat0['X']>=int(tB18))&(data_concat0['X']<=int(tB19))]

        if combobox9.get()==combobox6.get():
            count=data_concat00['Y']/(data_concat00['Y']+data_concat00['Z'])*100
            perelement=combobox6.get()
        elif combobox9.get()==combobox7.get():
            count=data_concat00['Z']/(data_concat00['Y']+data_concat00['Z'])*100
            perelement=combobox7.get()   
        elif combobox9.get()=="":
            messagebox.showerror('エラー','割合を見る元素を指定してください') 
        else:
            messagebox.showerror('エラー','元素は'+combobox5.get()+"または"+combobox6.get()+"または"+combobox7.get()+'のいずれかを重複せずに入力してください') 
    elif combobox8.get()==combobox6.get():        
        if tB18=="0" and tB19=="100":
            data_concat00=data_concat0
        else:
            data_concat00=data_concat0[(data_concat0['Y']>=int(tB18))&(data_concat0['Y']<=int(tB19))]
      
        if combobox9.get()==combobox7.get():
            count=data_concat00['Z']/(data_concat00['Z']+data_concat00['X'])*100
            perelement=combobox7.get()
        elif combobox9.get()==combobox5.get():
            count=data_concat00['X']/(data_concat00['Z']+data_concat00['X'])*100
            perelement=combobox5.get() 
        elif combobox9.get()=="":
            messagebox.showerror('エラー','割合を見る元素を指定してください')       
        else:
            messagebox.showerror('エラー','元素は'+combobox5.get()+"または"+combobox6.get()+"または"+combobox7.get()+'のいずれかを入力してください') 
    elif combobox8.get()==combobox7.get():
        if tB18=="0" and tB19=="100":
            data_concat00=data_concat0
        else:
            data_concat00=data_concat0[(data_concat0['Z']>=int(tB18))&(data_concat0['Z']<=int(tB19))]
      
        if combobox9.get()==combobox5.get():
            count=data_concat00['X']/(data_concat00['X']+data_concat00['Y'])*100
            perelement=combobox5.get()
        elif combobox9.get()==combobox6.get():
            count=data_concat00['Y']/(data_concat00['X']+data_concat00['Y'])*100 
            perelement=combobox6.get()
        elif combobox9.get()=="":
            messagebox.showerror('error','割合を見る元素を指定してください') 
        else:
            messagebox.showerror('error','元素は'+combobox5.get()+"または"+combobox6.get()+"または"+combobox7.get()+'のいずれかを入力してください') 
    elif combobox8.get()=="":
        messagebox.showerror('error','範囲を固定する元素を指定してください')
    else:
        messagebox.showerror('error','元素は'+combobox5.get()+"または"+combobox6.get()+"または"+combobox7.get()+'のいずれかを入力してください')

    data_z_c=pd.concat([count,data_z_SUM],axis=1)
    data_z_c.columns=['X','SUM']     
    print(data_z_c)
    data_z_0 = data_z_c.dropna(how="any")

    #重み付けなし普通の平均とデータの標準誤差、標準誤差
    #平均値
    mean_data = count.mean()
    print("平均")
    print(mean_data)
    #標準偏差
    std_data = np.std(count, ddof=1) #標本標準偏差でいいよね
    print("標準偏差")
    print(std_data)
    #標準誤差
    ste_data = std_data/(len(count)**(1/2))
    print("標準誤差")
    print(ste_data)

    print(data_z_0)
    #平均値4
    δ_data = data_gattai1**(1/2)
    data_d_X = data_gattai1[combobox5.get()]/float(textBox30.get())
    data_d_Z = data_gattai1[combobox7.get()]/float(textBox32.get())
    data_d_sum = data_d_X+data_d_Z
    δ_data_d_X = δ_data[combobox5.get()]/float(textBox30.get())
    δ_data_d_Z = δ_data[combobox7.get()]/float(textBox32.get())
    δ_s = (δ_data_d_X**2+δ_data_d_Z**2)**(1/2)
    δ_X = 100*((δ_data_d_X/data_d_X)**2+(δ_s/data_d_sum)**2)**(1/2)
    δ_Z = 100*((δ_data_d_Z/data_d_Z)**2+(δ_s/data_d_sum)**2)**(1/2)
    σ_S = (δ_X**2+δ_Z**2)**(1/2)
    w_S = 1/((σ_S)**2)
    data_z_00 = pd.concat([data_z_c,w_S],axis=1)
    data_z_000 = data_z_00.dropna(how="any")
    data_z_000.columns=['X','SUM','w']  
    data_w_count_X = data_z_000["X"]*data_z_000["w"]
    data_ave_w_X = np.sum(data_w_count_X)/np.sum(data_z_000["w"])
    print("重みつき平均4")
    print("X")
    print(data_ave_w_X)
    #標準偏差4
    data_zansa_X = data_z_0["X"]-data_ave_w_X
    data_w_zansa2_X = w_S*(data_zansa_X**2)
    data_std_w_X = (np.sum(data_w_zansa2_X)/((len(data_z_0["X"])-1)*np.sum(w_S)))**(1/2)
    print("重みつき標準偏差1")
    print("X")
    print(data_std_w_X)

    tB33=combobox1.get()

    times=100/int(tB33)

    NumX=[]
    for i in range(0,int(times)):
        NumX.append(np.count_nonzero((count>=i*int(tB33))&(count<=(i+1)*int(tB33))))

        #上でエラーの表示になるときはここでエラー出るからグラフかく操作もif文の中に入れたほうがいいかな？

    ax5.cla()

    plt.rcParams["font.family"] = graph_font

    fig5.set_facecolor(color_fig)
    ax5.set_facecolor(color_fig)

    ax5.spines['top'].set_color(color_axes)
    ax5.spines['bottom'].set_color(color_axes)
    ax5.spines['left'].set_color(color_axes)
    ax5.spines['right'].set_color(color_axes)
    ax5.tick_params(colors=color_axes)

    left=np.linspace(0,100-int(tB33),int(times),dtype=int)
    height=np.array(NumX)
    if bar_style == "枠あり":   
        ax5.bar(left,height,width=int(tB33),color=color_bar,linewidth=1,edgecolor=color_axes,align="edge",zorder=2)
    elif bar_style == "枠なし":
        ax5.bar(left,height,width=int(tB33)* 0.8,color=color_bar,align="edge",zorder=2)
    ax5.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
    ax5.set_xlabel("%"+perelement,fontname=graph_font,color=color_axes,weight=weight_font)
    ax5.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

    canvas5.draw()


#カウント分布
def clickF():

    plt.rcParams["font.family"] = graph_font

    SUM=data_gattai1[combobox5.get()]/float(textBox30.get())+data_gattai1[combobox6.get()]/float(textBox31.get())+data_gattai1[combobox7.get()]/float(textBox32.get())
    pX=data_gattai1[combobox5.get()]/float(textBox30.get())/SUM*100 
    pY=data_gattai1[combobox6.get()]/float(textBox31.get())/SUM*100
    pZ=data_gattai1[combobox7.get()]/float(textBox32.get())/SUM*100
    data_concat=pd.concat([pX,pY,pZ],axis=1)
    data_concat.columns=['X','Y','Z']

    data_z_SUM=data_gattai2[combobox5.get()]+data_gattai2[combobox6.get()]+data_gattai2[combobox7.get()]
    data_z_x=data_gattai2[combobox5.get()] #いらない列
    data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
    data_z.columns=['SUM','x']

    data_concat_z=pd.concat([data_concat,data_z],axis=1)

    if textBox21.get()=="":
        tB21="0"
    else:
        tB21=textBox21.get()

    if textBox22.get()=="":
        tB22="100"
    else:
        tB22=textBox22.get()

    if textBox23.get()=="":
        tB23="0"
    else:
        tB23=textBox23.get()

    if textBox24.get()=="":
        tB24="100"
    else:
        tB24=textBox24.get()
        
    if textBox25.get()=="":
        tB25="0"
    else:
        tB25=textBox25.get()

    if textBox26.get()=="":
        tB26="100"
    else:
        tB26=textBox26.get()

    print(type(data_concat_z["X"][0]))

    data_concat0=data_concat_z[(data_concat_z["X"]>=int(tB21))&(data_concat_z["X"]<=int(tB22))&(data_concat_z["Y"]>=int(tB23))&(data_concat_z["Y"]<=int(tB24))&(data_concat_z["Z"]>=int(tB25))&(data_concat_z["Z"]<=int(tB26))]
    zmax0=data_concat0['SUM'].max()
    print(zmax0)
    amari=zmax0%10
    print(amari)
    if amari==0:
       baisuu=zmax0
    else:
       baisuu=zmax0-amari+10

    if textBox27.get()=="":
        tB27="0"
    else:
        tB27=textBox27.get()

    if textBox28.get()=="":
        tB28=baisuu
    else:
        tB28=textBox28.get()

    if textBox29.get()=="":
        tB29=5
    else:
        tB29=textBox29.get()


    if len(data_concat0)==0:
        if int(tB25)<100-(int(tB22)+int(tB24)) or int(tB26)>100-(int(tB21)+int(tB23)):
            messagebox.showerror('エラー','範囲が間違っています')
        else:
            messagebox.showerror('エラー','範囲内にデータがありません')
    else:
        pltmin=int(tB27)
        amari0=int(tB28)%10
        if amari0==0:
            pltmax=int(tB28)
        else:
            pltmax=int(tB28)-amari0+10

        ax6.cla()

        fig6.set_facecolor(color_fig)
        ax6.set_facecolor(color_fig)

        ax6.spines['top'].set_color(color_axes)
        ax6.spines['bottom'].set_color(color_axes)
        ax6.spines['left'].set_color(color_axes)
        ax6.spines['right'].set_color(color_axes)
        ax6.tick_params(colors=color_axes)
    
        if bar_style == "枠あり":
            ax6.hist(data_concat0["SUM"],bins=np.arange(pltmin,pltmax+int(tB29),int(tB29)),color=color_bar,linewidth=1,edgecolor=color_axes,zorder=2)
        elif bar_style == "枠なし":
            ax6.hist(data_concat0["SUM"],bins=np.arange(pltmin,pltmax+int(tB29),int(tB29)),width = int(tB29) * 0.8,color=color_bar,zorder=2)
        ax6.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
        ax6.set_xlabel("Counts",fontname=graph_font,color=color_axes,weight=weight_font)
        ax6.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

        canvas6.draw()


def onclick(event):
    print("event.button=%d,event.xdata=%f,event.ydata=%f" %(event.button,event.xdata,event.ydata))
    eventx_min = event.xdata-0.02
    eventx_max = event.xdata+0.02
    eventy_min = event.ydata-0.02
    eventy_max = event.ydata+0.02
    data_click_kouho_1=data_click[(data_click["x"]>=eventx_min)&(data_click["x"]<=eventx_max)]
    data_click_kouho_2=data_click_kouho_1[(data_click_kouho_1["y"]>=eventy_min)&(data_click_kouho_1["y"]<=eventy_max)]
    data_y_sa = abs(data_click_kouho_2["y"]-event.ydata)
    data_click_satuki = pd.concat([data_click_kouho_2,data_y_sa],axis=1)
    data_click_satuki.columns = ["a'","b'","c'","sum","x","y","sa"]
    data_click_minjyun = data_click_satuki.sort_values("sa")
    data_click_minjyun_r = data_click_minjyun.reset_index()
    data_click_target_gyou = data_click_minjyun_r[0:1]
    print(data_click_target_gyou["index"])

    ax1_5.cla()

    plt.rcParams["font.family"] = graph_font

    fig1_5.set_facecolor(color_fig)
    ax1_5.set_facecolor(color_fig)

    ax1_5.spines['top'].set_color(color_axes)
    ax1_5.spines['bottom'].set_color(color_axes)
    ax1_5.spines['left'].set_color(color_axes)
    ax1_5.spines['right'].set_color(color_axes)
    ax1_5.tick_params(colors=color_axes)

    NP_number = int(data_click_target_gyou["index"])
    data_skip_column = int(data_large.columns.get_loc("skip"))
    print(data_skip_column)
    element_number = int(data_skip_column)-2
    data_plot = data_large.iloc[:,int(data_skip_column):len(data_large)]
    print(data_plot)
    data_time = data_large["Time"][NP_number]
    print(data_time)
    data_time_list = re.findall(r"\d+\.\d*",data_time)
    print(data_time)
    print(data_time_list)
    data_time_list_float = list(map(float,data_time_list))
    print(data_time_list_float)
    data_large_legend = data_large.columns[1:data_skip_column-1]

    def calc_002(n):
        return n*0.002

    for i in range(0,element_number):
        data_element_i = data_large.iloc[NP_number,data_skip_column+i+1]#[data_skip_column+i+1][NP_number]
        print(data_element_i)
        data_element_list_i = re.findall(r"[+-]?[0-9]+\.[0-9]*[e]?[+-]?[0-9]*",data_element_i)
        print(data_element_list_i)
        data_element_list_float_ini_i = list(map(float,data_element_list_i))
        data_element_list_float_i = list(map(calc_002,data_element_list_float_ini_i))
        print(data_element_list_float_i)
        ax1_5.plot(data_time_list_float,data_element_list_float_i,lw=2)

    ax1_5.set_xlabel("Time(s)",fontname=graph_font,color=color_axes,weight=weight_font)
    ax1_5.set_ylabel("Intensity(Counts)",fontname=graph_font,color=color_axes,weight=weight_font)
    #ax.set_ylim(0,7500)
    ax1_5.legend(data_large_legend,bbox_to_anchor=(1.05,1),loc="upper left",borderaxespad=0)
    canvas1_5.draw()

    a_dash = data_click_target_gyou["a'"]*data_click_target_gyou["sum"]/100
    b_dash = data_click_target_gyou["b'"]*data_click_target_gyou["sum"]/100
    c_dash = data_click_target_gyou["c'"]*data_click_target_gyou["sum"]/100
    a_x = a_dash*float(textBox30.get())
    b_y = b_dash*float(textBox31.get())
    c_z = c_dash*float(textBox32.get())
    a_warux = a_dash/float(textBox30.get())
    b_waruy = b_dash/float(textBox31.get())
    c_waruz = c_dash/float(textBox32.get())
    sa_per = (((1/a_x)+(a_warux+b_waruy+c_waruz)*(1/(a_dash+b_dash+c_dash))**2)**(1/2))*data_click_target_gyou["a'"]
    sb_per = (((1/b_y)+(a_warux+b_waruy+c_waruz)*(1/(a_dash+b_dash+c_dash))**2)**(1/2))*data_click_target_gyou["b'"]
    sc_per = (((1/c_z)+(a_warux+b_waruy+c_waruz)*(1/(a_dash+b_dash+c_dash))**2)**(1/2))*data_click_target_gyou["c'"]
    print("1SD_a")
    print(sa_per)
    print("1SD_b")
    print(sb_per)
    print("1SD_c")
    print(sc_per)

    ax3.cla()

    h=np.sqrt(3.0)*0.5

    for i in range(1,10):
        ax3.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], linestyle='dashed',color='gray', lw=0.5)
        ax3.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], linestyle='dashed',color='gray', lw=0.5)
        ax3.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], linestyle='dashed',color='gray', lw=0.5)

    ax3.plot([0.0, 1.0],[0.0, 0.0], color=color_axes, lw=2)
    ax3.plot([0.0, 0.5],[0.0, h], color=color_axes, lw=2)
    ax3.plot([1.0, 0.5],[0.0, h], color=color_axes, lw=2)
  
    ax3.text(0.455, h+0.0283, combobox5.get(), fontsize=22, color=color_axes)
    ax3.text(-0.1, -0.02, combobox6.get(), fontsize=22, color=color_axes)
    ax3.text(1.02, -0.02, combobox7.get(), fontsize=22, color=color_axes)

    for i in range(1,10):
        ax3.text(0.5+(10-i)/20.0+0.016, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize=17, color=color_axes)
        ax3.text((10-i)/20.0-0.082, h*(10-i)/10.0, '%d0' % i, fontsize=17, color=color_axes)
        ax3.text(i/10.0-0.03, -0.06, '%d0' % i, fontsize=17, color=color_axes)

    #ax3.text(0.90,h/2,'%'+combobox5.get(),fontsize=17, color=color_axes)
    #ax3.text(0.096,h/2,'%'+combobox6.get(),fontsize=17, color=color_axes)
    #ax3.text(0.5,-0.13,'%'+combobox7.get(),fontsize=17, color=color_axes)

    ax3.text(-0.15,1,"Number of particles:"+str(len(data_plot3.dropna())),fontsize=14, color=color_axes)

    ax3.scatter(data_plot3["x3"],data_plot3["y3"],c=color_plot,alpha=alpha_plot,s=size_plot)

    if not sansyou_1_a =="":
        plot_sansyou_1_x = (100-float(sansyou_1_b))/100-float(sansyou_1_a)/200
        plot_sansyou_1_y = h*float(sansyou_1_a)/100
        print(plot_sansyou_1_x)
        print(plot_sansyou_1_y)
        global sansyou_1_sa
        global sansyou_1_sb
        global sansyou_1_sc
        if sansyou_1_sa == "":
            sansyou_1_sa = 0
        if sansyou_1_sb == "":
            sansyou_1_sb = 0
        if sansyou_1_sc == "":
            sansyou_1_sc = 0
        
        ax3.scatter(plot_sansyou_1_x,plot_sansyou_1_y,c="red",alpha=1,s=20)
        ax3.plot([plot_sansyou_1_x+float(sansyou_1_sa)*h/100/h/2,plot_sansyou_1_x-float(sansyou_1_sa)*h/100/h/2],[plot_sansyou_1_y-float(sansyou_1_sa)*h/100,plot_sansyou_1_y+float(sansyou_1_sa)*h/100],color="red",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_1_x-float(sansyou_1_sb)*h/100/h/2,plot_sansyou_1_x+float(sansyou_1_sb)*h/100/h/2],[plot_sansyou_1_y-float(sansyou_1_sb)*h/100,plot_sansyou_1_y+float(sansyou_1_sb)*h/100],color="red",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_1_x-float(sansyou_1_sc)*h/100/h,plot_sansyou_1_x+float(sansyou_1_sc)*h/100/h],[plot_sansyou_1_y,plot_sansyou_1_y],color="red",alpha=0.8,lw=1.2)

    if not sansyou_2_a =="":
        plot_sansyou_2_x = (100-float(sansyou_2_b))/100-float(sansyou_2_a)/200
        plot_sansyou_2_y = h*float(sansyou_2_a)/100
        print(plot_sansyou_2_x)
        print(plot_sansyou_2_y)
        global sansyou_2_sa
        global sansyou_2_sb
        global sansyou_2_sc
        if sansyou_2_sa == "":
            sansyou_2_sa = 0
        if sansyou_2_sb == "":
            sansyou_2_sb = 0
        if sansyou_2_sc == "":
            sansyou_2_sc = 0
        ax3.scatter(plot_sansyou_2_x,plot_sansyou_2_y,c="blue",alpha=1,s=20)
        ax3.plot([plot_sansyou_2_x+float(sansyou_2_sa)*h/100/h/2,plot_sansyou_2_x-float(sansyou_2_sa)*h/100/h/2],[plot_sansyou_2_y-float(sansyou_2_sa)*h/100,plot_sansyou_2_y+float(sansyou_2_sa)*h/100],color="blue",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_2_x-float(sansyou_2_sb)*h/100/h/2,plot_sansyou_2_x+float(sansyou_2_sb)*h/100/h/2],[plot_sansyou_2_y-float(sansyou_2_sb)*h/100,plot_sansyou_2_y+float(sansyou_2_sb)*h/100],color="blue",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_2_x-float(sansyou_2_sc)*h/100/h,plot_sansyou_2_x+float(sansyou_2_sc)*h/100/h],[plot_sansyou_2_y,plot_sansyou_2_y],color="blue",alpha=0.8,lw=1.2)

    if not sansyou_3_a =="":
        plot_sansyou_3_x = (100-float(sansyou_3_b))/100-float(sansyou_3_a)/200
        plot_sansyou_3_y = h*float(sansyou_3_a)/100
        print(plot_sansyou_3_x)
        print(plot_sansyou_3_y)
        global sansyou_3_sa
        global sansyou_3_sb
        global sansyou_3_sc
        if sansyou_3_sa == "":
            sansyou_3_sa = 0
        if sansyou_3_sb == "":
            sansyou_3_sb = 0
        if sansyou_3_sc == "":
            sansyou_3_sc = 0
        ax3.scatter(plot_sansyou_3_x,plot_sansyou_3_y,c="green",alpha=1,s=20)
        ax3.plot([plot_sansyou_3_x+float(sansyou_3_sa)*h/100/h/2,plot_sansyou_3_x-float(sansyou_3_sa)*h/100/h/2],[plot_sansyou_3_y-float(sansyou_3_sa)*h/100,plot_sansyou_3_y+float(sansyou_3_sa)*h/100],color="green",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_3_x-float(sansyou_3_sb)*h/100/h/2,plot_sansyou_3_x+float(sansyou_3_sb)*h/100/h/2],[plot_sansyou_3_y-float(sansyou_3_sb)*h/100,plot_sansyou_3_y+float(sansyou_3_sb)*h/100],color="green",alpha=0.8,lw=1.2)
        ax3.plot([plot_sansyou_3_x-float(sansyou_3_sc)*h/100/h,plot_sansyou_3_x+float(sansyou_3_sc)*h/100/h],[plot_sansyou_3_y,plot_sansyou_3_y],color="green",alpha=0.8,lw=1.2)


    ax3.scatter(data_click_target_gyou["x"],data_click_target_gyou["y"],c="orange",s=size_plot)

    target_x = data_click_target_gyou["x"]
    target_y = data_click_target_gyou["y"]

    target_y_a_1 = target_y-sa_per*h/100
    target_y_a_2 = target_y+sa_per*h/100
    target_x_a_1 = target_x+sa_per*h/100/h/2
    target_x_a_2 = target_x-sa_per*h/100/h/2

    target_x_b_1 = target_x-sb_per*h/100/h/2
    target_x_b_2 = target_x+sb_per*h/100/h/2
    target_y_b_1 = target_y-sb_per*h/100
    target_y_b_2 = target_y+sb_per*h/100

    target_x_c_1 = target_x-sc_per*h/100/h
    target_x_c_2 = target_x+sc_per*h/100/h
    target_y_c_1 = target_y
    target_y_c_2 = target_y
    #"""

    ax3.plot([target_x_a_1,target_x_a_2],[target_y_a_1,target_y_a_2],color="orange",alpha=0.6,lw=1)
    ax3.plot([target_x_b_1,target_x_b_2],[target_y_b_1,target_y_b_2],color="orange",alpha=0.6,lw=1)
    ax3.plot([target_x_c_1,target_x_c_2],[target_y_c_1,target_y_c_2],color="orange",alpha=0.6,lw=1)

    canvas3.draw()

fig3 = plt.figure(figsize=(6.42,6.42))
ax3 = fig3.add_subplot(111)
ax3.set_aspect('equal', 'datalim')
plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
plt.tick_params(bottom=False, left=False, right=False, top=False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
canvas3=FigureCanvasTkAgg(fig3,master=root)
canvas3.get_tk_widget().place(x=341,y=29)
canvas3._tkcanvas.place(x=341,y=29)
fig3.canvas.mpl_connect("button_press_event",onclick)

btn12=tk.Button(root,text="読み込み",command=click_element,font=(label_font_jp,8))
btn12.place(width=50,height=25,x=270,y=98)

btn4=tk.Button(root,text="表示",command=clickC,font=(label_font_jp,9))
btn4.place(width=50,height=25,x=215,y=359)

btn5=tk.Button(root,text="全体表示",command=clickA,font=(label_font_jp,9))
btn5.place(width=90,height=25,x=60,y=440)

btn6=tk.Button(root,text="表示",command=clickD,font=(label_font_jp,9))
btn6.place(width=50,height=25,x=215,y=469)

btn7=tk.Button(root,text="表示",command=clickE,font=(label_font_jp,9))
btn7.place(width=50,height=25,x=215,y=609)

btn8=tk.Button(root,text="表示",command=clickF,font=(label_font_jp,9))
btn8.place(width=50,height=25,x=215,y=809)

btn2=tk.Button(root,text="csv読み込み",command=click2,font=(label_font_jp,9))
btn2.place(width=160,height=25,x=120,y=280)

label1=tk.Label(root,text="ファイル",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
label1.place(width=100,height=20,x=12,y=45)
label3=tk.Label(root,text="元素",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
label3.place(width=100,height=20,x=12,y=100)
label3_2=tk.Label(root,text="質量数",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
label3_2.place(width=100,height=20,x=12,y=145)
label3_3=tk.Label(root,text="最低カウント数",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
label3_3.place(width=100,height=20,x=12,y=190)
label3_4=tk.Label(root,text="補正",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
label3_4.place(width=100,height=20,x=12,y=235)

btn11=tk.Button(root,text="参照",command=click_file,font=(label_font_jp,9))
btn11.place(width=40,height=25,x=275,y=43)
textBox10=tk.Entry(root)
textBox10.place(width=40,height=20,x=120,y=190)
textBox11=tk.Entry(root)
textBox11.place(width=40,height=20,x=170,y=190)
textBox12=tk.Entry(root)
textBox12.place(width=40,height=20,x=220,y=190)
textBox30=tk.Entry(root)
textBox30.place(width=40,height=20,x=120,y=235)
textBox31=tk.Entry(root)
textBox31.place(width=40,height=20,x=170,y=235)
textBox32=tk.Entry(root)
textBox32.place(width=40,height=20,x=220,y=235)

btn1=tk.Button(root,text="読み込み",command=click1,font=(label_font_jp,8))
btn1.place(width=50,height=25,x=270,y=143)


label20=tk.Label(root,text="三角グラフ",anchor=tk.W,bg=color3,font=(label_font_jp,10))#,'underline'))
label20.place(width=67,height=16,x=20,y=330)

textBox13=tk.Entry(root)
textBox13.place(width=40,height=20,x=110,y=360)
textBox14=tk.Entry(root)
textBox14.place(width=40,height=20,x=160,y=360)
label7=tk.Label(root,text="-",bg=color1,font=(label_font,10))
label7.place(width=10,height=20,x=150,y=360)
label24=tk.Label(root,text="カウント",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label24.place(width=50,height=20,x=60,y=360)       

label21=tk.Label(root,text="三角柱グラフ",anchor=tk.W,bg=color4,font=(label_font_jp,10))#,'underline'))
label21.place(width=80,height=16,x=20,y=410)

textBox15=tk.Entry(root)
textBox15.place(width=40,height=20,x=110,y=470)
textBox16=tk.Entry(root)
textBox16.place(width=40,height=20,x=160,y=470)
label8=tk.Label(root,text="-",bg=color1,font=(label_font,10))
label8.place(width=10,height=20,x=150,y=470)
label25=tk.Label(root,text="カウント",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label25.place(width=50,height=20,x=60,y=470)       

label22=tk.Label(root,text="組成分布",anchor=tk.W,bg=color5,font=(label_font_jp,10))#,'underline'))
label22.place(width=57,height=16,x=20,y=520)

textBox18=tk.Entry(root)
textBox18.place(width=40,height=20,x=156,y=550)
textBox19=tk.Entry(root)
textBox19.place(width=40,height=20,x=205,y=550)
combobox1=ttk.Combobox(root,state='readonly',values=[1,2,4,5,10,20,25,50,100])
combobox1.current(4)      
combobox1.place(width=40,height=20,x=110,y=610)
label9=tk.Label(root,text=":",bg=color1,font=(label_font_jp,10))
label9.place(width=3,height=20,x=151,y=550)
label10=tk.Label(root,text="-",bg=color1,font=(label_font_jp,10))
label10.place(width=10,height=20,x=195,y=550)
label29=tk.Label(root,text="%",bg=color1,font=(label_font_jp,9))
label29.place(width=20,height=20,x=248,y=550) 
label26=tk.Label(root,text="固定",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label26.place(width=50,height=20,x=60,y=550) 
label27=tk.Label(root,text="表示",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label27.place(width=50,height=20,x=60,y=580) 
label30=tk.Label(root,text="幅",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label30.place(width=50,height=20,x=60,y=610) 

label22=tk.Label(root,text="カウント分布",anchor=tk.W,bg=color6,font=(label_font_jp,10))#,'underline'))
label22.place(width=80,height=16,x=20,y=660)

textBox21=tk.Entry(root)
textBox21.place(width=40,height=20,x=110,y=690)
textBox22=tk.Entry(root)
textBox22.place(width=40,height=20,x=160,y=690)
textBox23=tk.Entry(root)
textBox23.place(width=40,height=20,x=110,y=720)
textBox24=tk.Entry(root)
textBox24.place(width=40,height=20,x=160,y=720)
textBox25=tk.Entry(root)
textBox25.place(width=40,height=20,x=110,y=750)
textBox26=tk.Entry(root)
textBox26.place(width=40,height=20,x=160,y=750)
label11=tk.Label(root,text=combobox5.get()+":",bg=color1,font=(label_font_jp,10))
label11.place(width=20,height=20,x=80,y=690)
label12=tk.Label(root,text="-",bg=color1,font=(label_font_jp,10))
label12.place(width=10,height=20,x=150,y=690)
label13=tk.Label(root,text="%",bg=color1,font=(label_font_jp,9))
label13.place(width=20,height=20,x=203,y=690)
label14=tk.Label(root,text=combobox6.get()+":",bg=color1,font=(label_font_jp,10))
label14.place(width=20,height=20,x=80,y=720)
label15=tk.Label(root,text="-",bg=color1,font=(label_font_jp,10))
label15.place(width=10,height=20,x=150,y=720)
label16=tk.Label(root,text="%",bg=color1,font=(label_font_jp,9))
label16.place(width=20,height=20,x=203,y=720)
label17=tk.Label(root,text=combobox7.get()+":",bg=color1,font=(label_font_jp,10))
label17.place(width=20,height=20,x=80,y=750)
label18=tk.Label(root,text="-",bg=color1,font=(label_font_jp,10))
label18.place(width=10,height=20,x=150,y=750)
label19=tk.Label(root,text="%",bg=color1,font=(label_font_jp,9))
label19.place(width=20,height=20,x=203,y=750)

textBox27=tk.Entry(root)
textBox27.place(width=40,height=20,x=110,y=780)
textBox28=tk.Entry(root)
textBox28.place(width=40,height=20,x=160,y=780)      
label28=tk.Label(root,text="-",bg=color1,font=(label_font,10))
label28.place(width=10,height=20,x=150,y=780)
label31=tk.Label(root,text="カウント",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label31.place(width=50,height=20,x=60,y=780) 
textBox29=tk.Entry(root)
textBox29.place(width=40,height=20,x=110,y=810) 
label32=tk.Label(root,text="幅",anchor=tk.CENTER,bg=color1,font=(label_font_jp,9))
label32.place(width=50,height=20,x=60,y=810) 


def savelist():
    tBlist = ["",textBox2.get(),"",combobox5.get(),combobox6.get(),combobox7.get(),combobox2.get(),combobox3.get(),combobox4.get(),textBox10.get(),textBox11.get(),textBox12.get(),textBox13.get(),textBox14.get(),textBox15.get(),textBox16.get(),combobox8.get(),textBox18.get(),textBox19.get(),combobox9.get(),textBox21.get(),textBox22.get(),textBox23.get(),textBox24.get(),textBox25.get(),textBox26.get(),textBox28.get(),textBox29.get(),textBox30.get(),textBox31.get(),textBox32.get(),combobox1.get()]
    print(tBlist)
    tBlist_str = "?".join(tBlist)

    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="txt",filetypes = [("TRIファイル(*.tri)","*.tri")])#,title = "名前を付けて保存")

    if len(file_path) != 0:
        f = open(file_path,"w")
        f.write(tBlist_str)
        f.close
    
def openlist():
    file_path = tkinter.filedialog.askopenfilename(filetypes = [("TRIファイル(*.tri)","*.tri")])

    if len(file_path) != 0:
        f = open(file_path)
        tBlist_txt = f.read()
        f.close()

        str = tBlist_txt
        tBlist = str.split("?")

        print(tBlist)

        global textBox2
        textBox2.delete(0, tkinter.END)
        textBox2.insert(tkinter.END,tBlist[1])
        click_element()

        global combobox5
        global combobox6   
        global combobox7

        combo5_list_number=ele_list_min.index(tBlist[3])
        combobox5.current(int(combo5_list_number))

        combo6_list_number=ele_list_min.index(tBlist[4])
        combobox6.current(int(combo6_list_number))

        combo7_list_number=ele_list_min.index(tBlist[5])
        combobox7.current(int(combo7_list_number))

        click1()

        global combobox2
        global combobox3   
        global combobox4

        global combobox8
        global combobox9

        combo2_list_number=mass_list_tB4.index(tBlist[6])
        combobox2.current(int(combo2_list_number))

        combo3_list_number=mass_list_tB5.index(tBlist[7])
        combobox3.current(int(combo3_list_number))

        combo4_list_number=mass_list_tB6.index(tBlist[8])
        combobox4.current(int(combo4_list_number))

        textBox10.delete(0, tkinter.END)
        textBox10.insert(tkinter.END,tBlist[9])
        textBox11.delete(0, tkinter.END)
        textBox11.insert(tkinter.END,tBlist[10])
        textBox12.delete(0, tkinter.END)
        textBox12.insert(tkinter.END,tBlist[11])
        textBox13.delete(0, tkinter.END)
        textBox13.insert(tkinter.END,tBlist[12])
        textBox14.delete(0, tkinter.END)
        textBox14.insert(tkinter.END,tBlist[13])
        textBox15.delete(0, tkinter.END)
        textBox15.insert(tkinter.END,tBlist[14])
        textBox16.delete(0, tkinter.END)
        textBox16.insert(tkinter.END,tBlist[15])
        textBox18.delete(0, tkinter.END)
        textBox18.insert(tkinter.END,tBlist[17])
        textBox19.delete(0, tkinter.END)
        textBox19.insert(tkinter.END,tBlist[18])
        textBox21.delete(0, tkinter.END)
        textBox21.insert(tkinter.END,tBlist[20])
        textBox22.delete(0, tkinter.END)
        textBox22.insert(tkinter.END,tBlist[21])
        textBox23.delete(0, tkinter.END)
        textBox23.insert(tkinter.END,tBlist[22])
        textBox24.delete(0, tkinter.END)
        textBox24.insert(tkinter.END,tBlist[23])
        textBox25.delete(0, tkinter.END)
        textBox25.insert(tkinter.END,tBlist[24])
        textBox26.delete(0, tkinter.END)
        textBox26.insert(tkinter.END,tBlist[25])
        textBox28.delete(0, tkinter.END)
        textBox28.insert(tkinter.END,tBlist[26])
        textBox29.delete(0, tkinter.END)
        textBox29.insert(tkinter.END,tBlist[27])
        textBox30.delete(0, tkinter.END)
        textBox30.insert(tkinter.END,tBlist[28])
        textBox31.delete(0, tkinter.END)
        textBox31.insert(tkinter.END,tBlist[29])
        textBox32.delete(0, tkinter.END)
        textBox32.insert(tkinter.END,tBlist[30])
        combo1_list=[1,2,4,5,10,20,25,50,100]
        combo1_list_number=combo1_list.index(int(tBlist[31]))
        combobox1.current(int(combo1_list_number))

        click2()
        combo8_list_number=ele_list_min.index(tBlist[16])
        combobox8.current(int(combo8_list_number))
        combo9_list_number=ele_list_min.index(tBlist[19])
        combobox9.current(int(combo9_list_number))

        clickC()
        clickE()
        clickF()

def savefig3():
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
    
    print(file_path)

    if len(file_path) != 0:
        fig3.savefig(file_path)


def savefig5():
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
    
    print(file_path)

    if len(file_path) != 0:
        fig5.savefig(file_path)

def savefig6():
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
    
    print(file_path)

    if len(file_path) != 0:
        fig6.savefig(file_path)

def layout():
    newwindow = tk.Toplevel(root)
    newwindow.geometry("500x500")
    newwindow.title(u"レイアウト設定")

    label33=tk.Label(newwindow,text="グラフのフォント",font=(label_font_jp,9),anchor=tk.W)
    label33.place(width=100,height=20,x=20,y=80)
    label34=tk.Label(newwindow,text="プロットの大きさ",font=(label_font_jp,9),anchor=tk.W)
    label34.place(width=100,height=20,x=20,y=110)
    label35=tk.Label(newwindow,text="プロットの透明度",font=(label_font_jp,9),anchor=tk.W)
    label35.place(width=100,height=20,x=20,y=140)
    label36=tk.Label(newwindow,text="プロットの色",font=(label_font_jp,9),anchor=tk.W)
    label36.place(width=100,height=20,x=20,y=170)
    label37=tk.Label(newwindow,text="棒グラフの色",font=(label_font_jp,9),anchor=tk.W)
    label37.place(width=100,height=20,x=20,y=200)
    

    bln1 = tkinter.BooleanVar()
    if color_fig == "black":
        bln1.set(True)
    elif color_fig == "white":
        bln1.set(False)
    else:
        print("checkbox_error")   
    check1 = tk.Checkbutton(newwindow,variable=bln1,text="背景を黒にする",font=(label_font_jp,9))
    check1.place(x=20,y=20)

    graph_font_list=["Arial","Calibri","Cambria","Meiryo"]
    graph_font_list_number=graph_font_list.index(graph_font)
    combobox12=ttk.Combobox(newwindow,state="readonly",values=["Arial","Calibri","Cambria","Meiryo"])
    combobox12.place(width=80,height=20,x=130,y=80)
    combobox12.current(int(graph_font_list_number))    

    color_plot_list_0=["red","blue","green","yellow","gray"]
    if color_plot in color_plot_list_0:
        color_plot_list = ["red","blue","green","yellow","gray"]
    else:
        color_plot_list = ["red","blue","green","yellow","gray",color_plot]
    color_plot_list_number=color_plot_list.index(color_plot)
    global combobox13
    combobox13=ttk.Combobox(newwindow,state="readonly",values=color_plot_list)
    combobox13.place(width=80,height=20,x=130,y=170)
    combobox13.current(int(color_plot_list_number))  

    def color_choose_plot():
        color_now = color_plot
        color = colorchooser.askcolor(color_now,title="その他の色",master=newwindow)
        print(color)
        color_list=list(color)
        colorcode=color_list[1]
        if not color == (None, None):
            global combobox13
            combobox13=ttk.Combobox(newwindow,state="readonly",values=["red","blue","green","yellow","gray",colorcode])
            combobox13.place(width=80,height=20,x=130,y=170)
            combobox13.current(5)  
            print(combobox13.get()) 
        newwindow.attributes("-topmost",True)            

    btn11=tk.Button(newwindow,text="その他の色",command=color_choose_plot)
    btn11.place(width=80,height=25,x=225,y=170)    

    alpha_plot_list=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    alpha_plot_list_number=alpha_plot_list.index(alpha_plot)
    combobox14=ttk.Combobox(newwindow,state="readonly",values=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    combobox14.place(width=80,height=20,x=130,y=140)
    combobox14.current(int(alpha_plot_list_number)) 

    color_bar_list_0=["red","blue","green","yellow","gray"]
    if color_bar in color_bar_list_0:
        color_bar_list = ["red","blue","green","yellow","gray"]
    else:
        color_bar_list = ["red","blue","green","yellow","gray",color_bar]
    color_bar_list_number=color_bar_list.index(color_bar)
    global combobox15
    combobox15=ttk.Combobox(newwindow,state="readonly",values=color_bar_list)
    combobox15.place(width=80,height=20,x=130,y=200)
    combobox15.current(int(color_bar_list_number))  

    def color_choose_bar():
        color_now = color_bar
        color = colorchooser.askcolor(color_now,title="その他の色",master=newwindow)
        print(color)
        color_list=list(color)
        colorcode=color_list[1]
        if not colorcode == "None":
            global combobox15
            combobox15=ttk.Combobox(newwindow,state="readonly",values=["red","blue","green","yellow","gray",colorcode])
            combobox15.place(width=80,height=20,x=130,y=200)
            combobox15.current(5)  
            print(combobox15.get())   
        newwindow.attributes("-topmost",True)

    btn13=tk.Button(newwindow,text="その他の色",command=color_choose_bar)
    btn13.place(width=80,height=25,x=225,y=200)          

    bln2 = tkinter.BooleanVar()
    if bar_style == "枠あり":
        bln2.set(True)
    elif bar_style == "枠なし":
        bln2.set(False)
    else:
        print("checkbox_error")   
    check2 = tk.Checkbutton(newwindow,variable=bln2,text="棒グラフに枠線を表示する",font=(label_font_jp,9))
    check2.place(x=20,y=50)

    textBox34=ttk.Entry(newwindow)
    textBox34.place(width=60,height=20,x=130,y=110)
    textBox34.insert(tkinter.END,size_plot)

    def OK():
        global color_fig
        global color_axes
        global graph_font
        global color_plot
        global alpha_plot
        global color_bar
        global bar_style
        global size_plot
        if bln1.get():
            color_fig="black"
            color_axes="white"
        else:
            color_fig="white"
            color_axes="black"            
        print("color_fig:"+color_fig)
        print("color_axes:"+color_axes)
        graph_font=combobox12.get()
        print("graph_font:"+graph_font)
        color_plot=combobox13.get()
        print("color_plot:"+color_plot)
        alpha_plot=float(combobox14.get())
        print("alpha_plot:"+str(alpha_plot))
        color_bar=combobox15.get()
        print("color_bar:"+color_bar)    
        if bln2.get():
            bar_style="枠あり"
        else:
            bar_style="枠なし"
        print("bar_style:"+bar_style)  
        size_plot=int(float(textBox34.get()))
        print("size_plot:"+str(size_plot))                   
        newwindow.destroy()

    def Cancel():
        global color_fig
        global color_axes
        global graph_font
        global color_plot
        global alpha_plot
        global color_bar
        global bar_style
        global size_plot
        color_fig=color_fig
        print("color_fig:"+color_fig)
        color_axes=color_axes
        print("color_axes:"+color_axes)
        graph_font=graph_font
        print("graph_font:"+graph_font)
        color_plot=color_plot
        print("color_plot:"+color_plot)
        alpha_plot=float(alpha_plot)
        print("alpha_plot:"+str(alpha_plot))
        color_bar=color_bar
        print("color_bar:"+color_bar)
        bar_style=bar_style
        print("bar_style:"+bar_style)
        size_plot=float(size_plot)
        print("size_plot:"+str(size_plot))
        newwindow.destroy()

    btn9=tk.Button(newwindow,text="決定",command=OK)
    btn9.place(width=80,height=25,x=20,y=240)
    btn10=tk.Button(newwindow,text="キャンセル",command=Cancel)
    btn10.place(width=80,height=25,x=110,y=240)

def end():
    ret = messagebox.askyesno("確認","ウィンドウを閉じますか？")
    if ret == True:
        root.quit()
        sys.exit()#ちゃんと閉じれない　右上の×押すのと一緒

def sansyou():
    newwindow2 = tk.Toplevel(root)
    newwindow2.geometry("500x500")
    newwindow2.title(u"参照値")

    label38=tk.Label(newwindow2,text="参照値１",font=(label_font_jp,9),anchor=tk.W)
    label38.place(width=60,height=20,x=20,y=20)
    if combobox5.get() == "":
        label39=tk.Label(newwindow2,text="元素A",font=(label_font_jp,9),anchor=tk.W)
    else:
        label39=tk.Label(newwindow2,text=combobox5.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label39.place(width=60,height=20,x=80,y=20)
    if combobox6.get() =="":
        label40=tk.Label(newwindow2,text="元素B",font=(label_font_jp,9),anchor=tk.W)
    else:
        label40=tk.Label(newwindow2,text=combobox6.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label40.place(width=60,height=20,x=80,y=50)
    if combobox7.get() =="":
        label41=tk.Label(newwindow2,text="元素C",font=(label_font_jp,9),anchor=tk.W)
    else:
        label41=tk.Label(newwindow2,text=combobox7.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label41.place(width=60,height=20,x=80,y=80)

    label42=tk.Label(newwindow2,text="参照値２",font=(label_font_jp,9),anchor=tk.W)
    label42.place(width=60,height=20,x=20,y=140)
    if combobox5.get() == "":
        label43=tk.Label(newwindow2,text="元素A",font=(label_font_jp,9),anchor=tk.W)
    else:
        label43=tk.Label(newwindow2,text=combobox5.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label43.place(width=60,height=20,x=80,y=140)
    if combobox6.get() =="":
        label44=tk.Label(newwindow2,text="元素B",font=(label_font_jp,9),anchor=tk.W)
    else:
        label44=tk.Label(newwindow2,text=combobox6.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label44.place(width=60,height=20,x=80,y=170)
    if combobox7.get() =="":
        label45=tk.Label(newwindow2,text="元素C",font=(label_font_jp,9),anchor=tk.W)
    else:
        label45=tk.Label(newwindow2,text=combobox7.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label45.place(width=60,height=20,x=80,y=200)

    label46=tk.Label(newwindow2,text="参照値３",font=(label_font_jp,9),anchor=tk.W)
    label46.place(width=60,height=20,x=20,y=260)
    if combobox5.get() == "":
        label47=tk.Label(newwindow2,text="元素A",font=(label_font_jp,9),anchor=tk.W)
    else:
        label47=tk.Label(newwindow2,text=combobox5.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label47.place(width=60,height=20,x=80,y=260)
    if combobox6.get() =="":
        label48=tk.Label(newwindow2,text="元素B",font=(label_font_jp,9),anchor=tk.W)
    else:
        label48=tk.Label(newwindow2,text=combobox6.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label48.place(width=60,height=20,x=80,y=290)
    if combobox7.get() =="":
        label49=tk.Label(newwindow2,text="元素C",font=(label_font_jp,9),anchor=tk.W)
    else:
        label49=tk.Label(newwindow2,text=combobox7.get(),font=(label_font_jp,9),anchor=tk.CENTER)
    label49.place(width=60,height=20,x=80,y=320)

    textBox35=ttk.Entry(newwindow2)
    textBox35.place(width=50,height=20,x=140,y=20)
    textBox35.insert(tkinter.END,sansyou_1_a)
    label50=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label50.place(width=20,height=20,x=190,y=20)
    textBox36=ttk.Entry(newwindow2)
    textBox36.place(width=50,height=20,x=210,y=20)
    textBox36.insert(tkinter.END,sansyou_1_sa)
    textBox37=ttk.Entry(newwindow2)
    textBox37.place(width=50,height=20,x=140,y=50)
    textBox37.insert(tkinter.END,sansyou_1_b)
    label51=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label51.place(width=20,height=20,x=190,y=50)
    textBox38=ttk.Entry(newwindow2)
    textBox38.place(width=50,height=20,x=210,y=50)
    textBox38.insert(tkinter.END,sansyou_1_sb)
    textBox39=ttk.Entry(newwindow2)
    textBox39.place(width=50,height=20,x=140,y=80)
    textBox39.insert(tkinter.END,sansyou_1_c)
    label52=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label52.place(width=20,height=20,x=190,y=80)
    textBox40=ttk.Entry(newwindow2)
    textBox40.place(width=50,height=20,x=210,y=80)
    textBox40.insert(tkinter.END,sansyou_1_sc)

    textBox41=ttk.Entry(newwindow2)
    textBox41.place(width=50,height=20,x=140,y=140)
    textBox41.insert(tkinter.END,sansyou_2_a)
    label53=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label53.place(width=20,height=20,x=190,y=140)
    textBox42=ttk.Entry(newwindow2)
    textBox42.place(width=50,height=20,x=210,y=140)
    textBox42.insert(tkinter.END,sansyou_2_sa)
    textBox43=ttk.Entry(newwindow2)
    textBox43.place(width=50,height=20,x=140,y=170)
    textBox43.insert(tkinter.END,sansyou_2_b)
    label54=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label54.place(width=20,height=20,x=190,y=170)
    textBox44=ttk.Entry(newwindow2)
    textBox44.place(width=50,height=20,x=210,y=170)
    textBox44.insert(tkinter.END,sansyou_2_sb)
    textBox45=ttk.Entry(newwindow2)
    textBox45.place(width=50,height=20,x=140,y=200)
    textBox45.insert(tkinter.END,sansyou_2_c)
    label55=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label55.place(width=20,height=20,x=190,y=200)
    textBox46=ttk.Entry(newwindow2)
    textBox46.place(width=50,height=20,x=210,y=200)
    textBox46.insert(tkinter.END,sansyou_2_sc)

    textBox47=ttk.Entry(newwindow2)
    textBox47.place(width=50,height=20,x=140,y=260)
    textBox47.insert(tkinter.END,sansyou_3_a)
    label56=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label56.place(width=20,height=20,x=190,y=260)
    textBox48=ttk.Entry(newwindow2)
    textBox48.place(width=50,height=20,x=210,y=260)
    textBox48.insert(tkinter.END,sansyou_3_sa)
    textBox49=ttk.Entry(newwindow2)
    textBox49.place(width=50,height=20,x=140,y=290)
    textBox49.insert(tkinter.END,sansyou_3_b)
    label57=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label57.place(width=20,height=20,x=190,y=290)
    textBox50=ttk.Entry(newwindow2)
    textBox50.place(width=50,height=20,x=210,y=290)
    textBox50.insert(tkinter.END,sansyou_3_sb)
    textBox51=ttk.Entry(newwindow2)
    textBox51.place(width=50,height=20,x=140,y=320)
    textBox51.insert(tkinter.END,sansyou_3_c)
    label58=tk.Label(newwindow2,text="±",font=(label_font_jp,9),anchor=tk.CENTER)
    label58.place(width=20,height=20,x=190,y=320)
    textBox52=ttk.Entry(newwindow2)
    textBox52.place(width=50,height=20,x=210,y=320)
    textBox52.insert(tkinter.END,sansyou_3_sc)

    def OK2():
        global sansyou_1_a
        global sansyou_1_b
        global sansyou_1_c
        global sansyou_1_sa
        global sansyou_1_sb
        global sansyou_1_sc
        global sansyou_2_a
        global sansyou_2_b
        global sansyou_2_c
        global sansyou_2_sa
        global sansyou_2_sb
        global sansyou_2_sc
        global sansyou_3_a
        global sansyou_3_b
        global sansyou_3_c
        global sansyou_3_sa
        global sansyou_3_sb
        global sansyou_3_sc

        sansyou_1_a = textBox35.get()
        sansyou_1_sa = textBox36.get()
        sansyou_1_b = textBox37.get()
        sansyou_1_sb = textBox38.get()
        sansyou_1_c = textBox39.get()
        sansyou_1_sc = textBox40.get()

        sansyou_2_a = textBox41.get()
        sansyou_2_sa = textBox42.get()
        sansyou_2_b = textBox43.get()
        sansyou_2_sb = textBox44.get()
        sansyou_2_c = textBox45.get()
        sansyou_2_sc = textBox46.get()

        sansyou_3_a = textBox47.get()
        sansyou_3_sa = textBox48.get()
        sansyou_3_b = textBox49.get()
        sansyou_3_sb = textBox50.get()
        sansyou_3_c = textBox51.get()
        sansyou_3_sc = textBox52.get()

        newwindow2.destroy()

    def Cancel2():
        global sansyou_1_a
        global sansyou_1_b
        global sansyou_1_c
        global sansyou_1_sa
        global sansyou_1_sb
        global sansyou_1_sc
        global sansyou_2_a
        global sansyou_2_b
        global sansyou_2_c
        global sansyou_2_sa
        global sansyou_2_sb
        global sansyou_2_sc
        global sansyou_3_a
        global sansyou_3_b
        global sansyou_3_c
        global sansyou_3_sa
        global sansyou_3_sb
        global sansyou_3_sc

        sansyou_1_a = sansyou_1_a
        sansyou_1_b = sansyou_1_b
        sansyou_1_c = sansyou_1_c
        sansyou_1_sa = sansyou_1_sa
        sansyou_1_sb = sansyou_1_sb
        sansyou_1_sc = sansyou_1_sc

        sansyou_2_a = sansyou_2_a
        sansyou_2_b = sansyou_2_b
        sansyou_2_c = sansyou_2_c
        sansyou_2_sa = sansyou_2_sa
        sansyou_2_sb = sansyou_2_sb
        sansyou_2_sc = sansyou_2_sc

        sansyou_3_a = sansyou_3_a
        sansyou_3_b = sansyou_3_b
        sansyou_3_c = sansyou_3_c
        sansyou_3_sa = sansyou_3_sa
        sansyou_3_sb = sansyou_3_sb
        sansyou_3_sc = sansyou_3_sc

        newwindow2.destroy()
    
    btn13=tk.Button(newwindow2,text="決定",command=OK2)
    btn13.place(width=80,height=25,x=20,y=370)
    btn14=tk.Button(newwindow2,text="キャンセル",command=Cancel2)
    btn14.place(width=80,height=25,x=110,y=370)

def hannisitei():
    if triangle_plot == "":
        messagebox.showerror("エラー","三角グラフの表示を行ってください")
    else:
        newwindow3 = tk.Toplevel(root)
        newwindow3.geometry("500x500")
        newwindow3.title(u"範囲指定")

        if combobox5.get() == "":
            label59=tk.Label(newwindow3,text="元素A",font=(label_font_jp,9),anchor=tk.W)
        else:
            label59=tk.Label(newwindow3,text=combobox5.get(),font=(label_font_jp,9),anchor=tk.CENTER)
        label59.place(width=60,height=20,x=20,y=20)
        if combobox6.get() =="":
            label60=tk.Label(newwindow3,text="元素B",font=(label_font_jp,9),anchor=tk.W)
        else:
            label60=tk.Label(newwindow3,text=combobox6.get(),font=(label_font_jp,9),anchor=tk.CENTER)
        label60.place(width=60,height=20,x=20,y=50)
        if combobox7.get() =="":
            label61=tk.Label(newwindow3,text="元素C",font=(label_font_jp,9),anchor=tk.W)
        else:
            label61=tk.Label(newwindow3,text=combobox7.get(),font=(label_font_jp,9),anchor=tk.CENTER)
        label61.place(width=60,height=20,x=20,y=80)    

        textBox53=ttk.Entry(newwindow3)
        textBox53.place(width=50,height=20,x=80,y=20)
        textBox53.insert(tkinter.END,sansyou_1_a)
        label62=tk.Label(newwindow3,text="-",font=(label_font_jp,9),anchor=tk.CENTER)
        label62.place(width=20,height=20,x=130,y=20)
        textBox54=ttk.Entry(newwindow3)
        textBox54.place(width=50,height=20,x=150,y=20)
        textBox54.insert(tkinter.END,sansyou_1_sa)
        textBox55=ttk.Entry(newwindow3)
        textBox55.place(width=50,height=20,x=80,y=50)
        textBox55.insert(tkinter.END,sansyou_1_b)
        label63=tk.Label(newwindow3,text="-",font=(label_font_jp,9),anchor=tk.CENTER)
        label63.place(width=20,height=20,x=130,y=50)
        textBox56=ttk.Entry(newwindow3)
        textBox56.place(width=50,height=20,x=150,y=50)
        textBox56.insert(tkinter.END,sansyou_1_sb)
        textBox57=ttk.Entry(newwindow3)
        textBox57.place(width=50,height=20,x=80,y=80)
        textBox57.insert(tkinter.END,sansyou_1_c)
        label64=tk.Label(newwindow3,text="-",font=(label_font_jp,9),anchor=tk.CENTER)
        label64.place(width=20,height=20,x=130,y=80)
        textBox58=ttk.Entry(newwindow3)
        textBox58.place(width=50,height=20,x=150,y=80)
        textBox58.insert(tkinter.END,sansyou_1_sc)
        label65=tk.Label(newwindow3,text="%",font=(label_font_jp,9),anchor=tk.CENTER)
        label65.place(width=20,height=20,x=200,y=20)
        label66=tk.Label(newwindow3,text="%",font=(label_font_jp,9),anchor=tk.CENTER)
        label66.place(width=20,height=20,x=200,y=50)
        label67=tk.Label(newwindow3,text="%",font=(label_font_jp,9),anchor=tk.CENTER)
        label67.place(width=20,height=20,x=200,y=80)
    def OK3():
        global hanni_a_1
        global hanni_a_2
        global hanni_b_1
        global hanni_b_2
        global hanni_c_1
        global hanni_c_2

        if textBox53.get()=="":
            hanni_a_1 = "0"
        else:
            hanni_a_1 = textBox53.get()
        
        if textBox54.get()=="":
            hanni_a_2 = "100"
        else:
            hanni_a_2 = textBox54.get()
        
        if textBox55.get()=="":
            hanni_b_1 = "0"
        else:
            hanni_b_1 = textBox55.get()
        
        if textBox56.get()=="":
            hanni_b_2 = "100"
        else:
            hanni_b_2 = textBox56.get()
        
        if textBox57.get()=="":
            hanni_c_1 = "0"
        else:
            hanni_c_1 = textBox57.get()
        
        if textBox58.get()=="":
            hanni_c_2 = "100"
        else:
            hanni_c_2 = textBox58.get()

        newwindow3.destroy()

        newwindow4 = tk.Toplevel(root)
        newwindow4.geometry("1850x980")
        newwindow4.title(u"範囲指定")
        newwindow4.configure(bg=color7)

        print(data_concat0_tri)#%表示のconcat0を参照すればいいはず… XがA%、YがB%、ZがC%に対応
        data_gattai0_hanni = data_concat0_tri[(data_concat0_tri["X"]>=int(hanni_a_1))&(data_concat0_tri["X"]<=int(hanni_a_2))&(data_concat0_tri["Y"]>=int(hanni_b_1))&(data_concat0_tri["Y"]<=int(hanni_b_2))&(data_concat0_tri["Z"]>=int(hanni_c_1))&(data_concat0_tri["Z"]<=int(hanni_c_2))]
        print(data_gattai0_hanni)
        if len(data_gattai0_hanni)==0:
            messagebox.showerror("エラー","範囲が間違っている あるいは範囲内にデータがありません")#後でそれぞれ別のエラーにする(カウント数分布の範囲指定参照)
        else:
            print(data)
            index_list_hanni = list(data_gattai0_hanni.index)
            columns_list_hanni = data.columns.values
            data_hanni = []
            for i in range(0,len(index_list_hanni)):
                index_i = int(index_list_hanni[i])
                print(index_i)
                hanni_list_i = list(data.iloc[index_i])
                print(hanni_list_i)
                #print(list(hanni_list_i[1:2]))
                data_hanni.append(list(hanni_list_i))
            print(data_hanni)#これをデータフレームにすればよい
            
            global dataframe_hanni
            dataframe_hanni = pd.DataFrame(data_hanni,columns=columns_list_hanni,index=index_list_hanni)
            print(dataframe_hanni)#dataと同じ形にできた！

            frame4_3=tk.Canvas(newwindow4,width=315,height=285,bg=color2)
            frame4_3.place(x=8,y=28)

            combobox4_1=ttk.Combobox(newwindow4,state='readonly',values=[1,2,4,5,10,20,25,50,100])
            combobox4_1.current(4)      
            combobox4_1.place(width=40,height=20,x=110,y=610)

            combobox4_2=ttk.Combobox(newwindow4,state="readonly",values=[])
            combobox4_2.place(width=40,height=20,x=120,y=145)
            combobox4_3=ttk.Combobox(newwindow4,state="readonly",values=[])
            combobox4_3.place(width=40,height=20,x=170,y=145)
            combobox4_4=ttk.Combobox(newwindow4,state="readonly",values=[])
            combobox4_4.place(width=40,height=20,x=220,y=145)

            combobox4_5=ttk.Combobox(newwindow4,state='readonly',values=[])
            combobox4_5.place(width=40,height=20,x=120,y=100)
            combobox4_6=ttk.Combobox(newwindow4,state='readonly',values=[])
            combobox4_6.place(width=40,height=20,x=170,y=100)
            combobox4_7=ttk.Combobox(newwindow4,state='readonly',values=[])
            combobox4_7.place(width=40,height=20,x=220,y=100)

            combobox4_8=ttk.Combobox(newwindow4,state='readonly',values=[])
            combobox4_8.place(width=40,height=20,x=110,y=550)
            combobox4_9=ttk.Combobox(newwindow4,state='readonly',values=[])
            combobox4_9.place(width=40,height=20,x=110,y=580)

            frame4_1=tk.Canvas(newwindow4,width=652,height=652,bg=color3)
            frame4_1.place(x=334,y=22)
            frame4_4=tk.Canvas(newwindow4,width=610,height=321,bg=color5)
            frame4_4.place(x=996,y=22)
            frame4_5=tk.Canvas(newwindow4,width=610,height=321,bg=color6)
            frame4_5.place(x=996,y=353)

            frame4_6=tk.Canvas(newwindow4,width=71,height=20,bg=color3)
            frame4_6.place(x=16,y=326)
            frame4_7=tk.Canvas(newwindow4,width=84,height=20,bg=color4)
            frame4_7.place(x=16,y=406)
            frame4_8=tk.Canvas(newwindow4,width=61,height=20,bg=color5)
            frame4_8.place(x=16,y=516)
            frame4_9=tk.Canvas(newwindow4,width=84,height=20,bg=color6)
            frame4_9.place(x=16,y=656)

            fig4_5=plt.figure(figsize=(6,3.11))
            fig4_5.subplots_adjust(bottom=0.2)
            ax4_5=fig4_5.add_subplot(111)
            ax4_5.spines['top'].set_color("w")
            ax4_5.spines['bottom'].set_color("w")
            ax4_5.spines['left'].set_color("w")
            ax4_5.spines['right'].set_color("w")
            ax4_5.tick_params(colors="w")
            canvas4_5=FigureCanvasTkAgg(fig4_5,master=newwindow4)
            canvas4_5.get_tk_widget().place(x=1003,y=29)
            canvas4_5._tkcanvas.place(x=1003,y=29)

            fig4_6=plt.figure(figsize=(6,3.11))
            fig4_6.subplots_adjust(bottom=0.2)
            ax4_6=fig4_6.add_subplot(111)
            ax4_6.spines['top'].set_color("w")
            ax4_6.spines['bottom'].set_color("w")
            ax4_6.spines['left'].set_color("w")
            ax4_6.spines['right'].set_color("w")
            ax4_6.tick_params(colors="w")
            canvas4_6=FigureCanvasTkAgg(fig4_6,master=newwindow4)
            canvas4_6.get_tk_widget().place(x=1003,y=360)
            canvas4_6._tkcanvas.place(x=1003,y=360)

            def click_element_4():
                global combobox4_5
                global combobox4_6   
                global combobox4_7
                global ele_list_min_4
                global ele_list_4
                global mass_list_4

                if not textBox2.get()=="":
                    try:
                        data_csv = pd.read_csv(textBox2.get())
                        """
                        data_NaN=data_csv.loc[:,data_csv.iloc[1].isnull()]
                        header=data_NaN.columns
                        header_number=header[0].replace("Unnamed: ","")
                        isotope_number=int(header_number)-1
                        """
                        #isotope_df=data_csv.iloc[1,1:isotope_number+1]
                        isotope_df_0=data_csv.columns
                        isotope_df = isotope_df_0[1:len(isotope_df_0)-1]
                        isotope_list=isotope_df.values.tolist()
                        print(isotope_list)
                        ele_list_4=[]
                        for i in range(0,len(isotope_list)):
                            alpha_i="".join([s for s in isotope_list[i] if s.isalpha()])
                            ele_list_4.append(alpha_i)
                        print(ele_list_4)
                        mass_list_4=[]
                        for i in range(0,len(isotope_list)):
                            digit_i="".join([s for s in isotope_list[i] if s.isdigit()])
                            mass_list_4.append(digit_i)
                        print(mass_list_4)
                        ele_list_min_4=list(set(ele_list_4))
                        ele_list_min_4.sort()
                        print(ele_list_min_4)
                        combobox4_5=ttk.Combobox(newwindow4,state='readonly',values=ele_list_min_4)
                        combobox4_5.current(0)
                        combobox4_5.place(width=40,height=20,x=120,y=100)
                        combobox4_6=ttk.Combobox(newwindow4,state='readonly',values=ele_list_min_4)
                        combobox4_6.current(0)
                        combobox4_6.place(width=40,height=20,x=170,y=100)
                        combobox4_7=ttk.Combobox(newwindow4,state='readonly',values=ele_list_min_4)
                        combobox4_7.current(0)
                        combobox4_7.place(width=40,height=20,x=220,y=100)
                    except:
                        messagebox.showerror('エラー','正しい形式のファイルを選択してください')    
                else:
                    messagebox.showerror('エラー','ファイルを選択してください')

            def click4_1():
               global combobox4_2
               global combobox4_3   
               global combobox4_4
               global combobox4_5
               global combobox4_6
               global combobox4_7
               global mass_list_tB4_4
               global mass_list_tB4_5
               global mass_list_tB4_6

               if combobox4_5.get()=="" or combobox4_6.get()=="" or combobox4_7.get()=="":
                   messagebox.showerror('エラー','元素を３か所すべてに入力してください') #多分絶対このエラー出ない
               elif combobox4_5.get()==combobox4_6.get() or combobox4_6.get()==combobox4_7.get() or combobox4_5.get()==combobox4_7.get():
                   messagebox.showerror('エラー','元素を重複なく選択してください')
               elif not combobox4_5.get() in Atomic_Symbol_list or not combobox4_6.get() in Atomic_Symbol_list or not combobox4_7.get() in Atomic_Symbol_list: #読み取れるようになればいらない
                   messagebox.showerror('エラー','元素を正しく入力してください') #多分絶対このエラー出ない
               else:
                   iso_list_tB4_4 = [k for k, x in enumerate(ele_list_4) if x == combobox4_5.get()]
                   mass_list_tB4_4=[]
                   for i in range(0,len(iso_list_tB4_4)):
                       iso_index_i = iso_list_tB4_4[i]
                       mass_i = mass_list_4[int(iso_index_i)]
                       mass_list_tB4_4.append(mass_i)
                   print(mass_list_tB4_4) 
                   iso_list_tB4_5 = [k for k, x in enumerate(ele_list_4) if x == combobox4_6.get()]
                   mass_list_tB4_5=[]
                   for i in range(0,len(iso_list_tB4_5)):
                       iso_index_i = iso_list_tB4_5[i]
                       mass_i = mass_list_4[int(iso_index_i)]
                       mass_list_tB4_5.append(mass_i)
                   print(mass_list_tB4_5) 
                   iso_list_tB4_6 = [k for k, x in enumerate(ele_list_4) if x == combobox4_7.get()]
                   mass_list_tB4_6=[]
                   for i in range(0,len(iso_list_tB4_6)):
                       iso_index_i = iso_list_tB4_6[i]
                       mass_i = mass_list_4[int(iso_index_i)]
                       mass_list_tB4_6.append(mass_i)
                   print(mass_list_tB4_6) 
                   combobox4_2=ttk.Combobox(newwindow4,state='readonly',values=mass_list_tB4_4)
                   combobox4_2.current(0)
                   combobox4_2.place(width=40,height=20,x=120,y=145)
                   combobox4_3=ttk.Combobox(newwindow4,state='readonly',values=mass_list_tB4_5)
                   combobox4_3.current(0)
                   combobox4_3.place(width=40,height=20,x=170,y=145)
                   combobox4_4=ttk.Combobox(newwindow4,state='readonly',values=mass_list_tB4_6)
                   combobox4_4.current(0)
                   combobox4_4.place(width=40,height=20,x=220,y=145)

            def click4_2():
                global dataframe_hanni
                global data_gattai4_1
                global data_gattai4_2
                global combobox4_2
                global combobox4_3
                global combobox4_4
                global combobox4_5
                global combobox4_6
                global combobox4_7
                global combobox4_8
                global combobox4_9
                global ele_list_min_4

                tB4_4_data_1 = dataframe_hanni["'[{}{}]+'".format(combobox4_2.get(),combobox4_5.get())]
                tB4_5_data_1 = dataframe_hanni["'[{}{}]+'".format(combobox4_3.get(),combobox4_6.get())]
                tB4_6_data_1 = dataframe_hanni["'[{}{}]+'".format(combobox4_4.get(),combobox4_7.get())]
                data_gattai4_1=pd.concat([tB4_4_data_1,tB4_5_data_1,tB4_6_data_1],axis=1)
                data_gattai4_1.columns=["{}".format(combobox4_5.get()),"{}".format(combobox4_6.get()),"{}".format(combobox4_7.get())]
                print(data_gattai4_1)

                iso_list_tB4_4 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox4_5.get()]
                mass_list_tB4_4=[]
                for i in range(0,len(iso_list_tB4_4)):
                    iso_index_i = iso_list_tB4_4[i]
                    massnumber = element_list["Mass Number"]
                    mass_i = massnumber[int(iso_index_i)]
                    mass_list_tB4_4.append(mass_i)
                print(mass_list_tB4_4) 
                iso_list_tB4_5 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox4_6.get()]
                mass_list_tB4_5=[]
                for i in range(0,len(iso_list_tB4_5)):
                    iso_index_i = iso_list_tB4_5[i]
                    massnumber = element_list["Mass Number"]
                    mass_i = massnumber[int(iso_index_i)]
                    mass_list_tB4_5.append(mass_i)
                print(mass_list_tB4_5) 
                iso_list_tB4_6 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == combobox4_7.get()]
                mass_list_tB4_6=[]
                for i in range(0,len(iso_list_tB4_6)):
                    iso_index_i = iso_list_tB4_6[i]
                    massnumber = element_list["Mass Number"]
                    mass_i = massnumber[int(iso_index_i)]
                    mass_list_tB4_6.append(mass_i)
                print(mass_list_tB4_6) 

                Iso_Compo_list = element_list["Isotopic Composition"]
                list_number_tB4_4 = mass_list_tB4_4.index(int(combobox4_2.get()))
                index_tB4_4 = iso_list_tB4_4[int(list_number_tB4_4)]
                iso_compo_tB4_4 = Iso_Compo_list[int(index_tB4_4)]
                print(iso_compo_tB4_4)
                list_number_tB4_5 = mass_list_tB4_5.index(int(combobox4_3.get()))
                index_tB4_5 = iso_list_tB4_5[int(list_number_tB4_5)]
                iso_compo_tB4_5 = Iso_Compo_list[int(index_tB4_5)]
                print(iso_compo_tB4_5)
                list_number_tB4_6 = mass_list_tB4_6.index(int(combobox4_4.get()))
                index_tB4_6 = iso_list_tB4_6[int(list_number_tB4_6)]
                iso_compo_tB4_6 = Iso_Compo_list[int(index_tB4_6)]
                print(iso_compo_tB4_6)

                print(textBox4_30.get())
                if textBox4_30.get()=="" and textBox4_31.get()=="" and textBox4_32.get()=="":
                    textBox4_30.insert(tkinter.END,iso_compo_tB4_4)
                    textBox4_31.insert(tkinter.END,iso_compo_tB4_5)
                    textBox4_32.insert(tkinter.END,iso_compo_tB4_6)
                    tB4_30=iso_compo_tB4_4
                    tB4_31=iso_compo_tB4_5
                    tB4_32=iso_compo_tB4_6
                else:
                    tB4_30=textBox4_30.get()
                    tB4_31=textBox4_31.get()
                    tB4_32=textBox4_32.get()

                tB4_4_data_2 = dataframe_hanni["'[{}{}]+'".format(combobox4_2.get(),combobox4_5.get())]/float(iso_compo_tB4_4)*float(textBox4_30.get())/float(tB4_30)
                tB4_5_data_2 = dataframe_hanni["'[{}{}]+'".format(combobox4_3.get(),combobox4_6.get())]/float(iso_compo_tB4_4)*float(textBox4_30.get())/float(tB4_31)
                tB4_6_data_2 = dataframe_hanni["'[{}{}]+'".format(combobox4_4.get(),combobox4_7.get())]/float(iso_compo_tB4_4)*float(textBox4_30.get())/float(tB4_32)
                data_gattai4_2=pd.concat([tB4_4_data_2,tB4_5_data_2,tB4_6_data_2],axis=1)
                data_gattai4_2.columns=["{}".format(combobox4_5.get()),"{}".format(combobox4_6.get()),"{}".format(combobox4_7.get())]
                print(data_gattai4_2)    

                combobox4_8=ttk.Combobox(newwindow4,state='readonly',values=ele_list_min_4)#後で変える
                combobox4_8.current(0)      
                combobox4_8.place(width=40,height=20,x=110,y=550)
                combobox4_9=ttk.Combobox(newwindow4,state='readonly',values=ele_list_min_4)
                combobox4_9.current(1)      
                combobox4_9.place(width=40,height=20,x=110,y=580)

                label4_11_2=tk.Label(newwindow4,text=combobox4_5.get()+":",bg=color7,font=(label_font,12))
                label4_11_2.place(width=20,height=20,x=80,y=690)
                label4_14_2=tk.Label(newwindow4,text=combobox4_6.get()+":",bg=color7,font=(label_font,12))
                label4_14_2.place(width=20,height=20,x=80,y=720)
                label4_17_2=tk.Label(newwindow4,text=combobox4_7.get()+":",bg=color7,font=(label_font,12))
                label4_17_2.place(width=20,height=20,x=80,y=750)

                ax4_3.cla()
                ax4_5.cla()
                ax4_6.cla()
                ax4_3.spines['top'].set_color(color_axes_pre)
                ax4_3.spines['bottom'].set_color(color_axes_pre)
                ax4_3.spines['left'].set_color(color_axes_pre)
                ax4_3.spines['right'].set_color(color_axes_pre)
                ax4_3.tick_params(colors=color_axes_pre)
                ax4_5.spines['top'].set_color(color_axes_pre)
                ax4_5.spines['bottom'].set_color(color_axes_pre)
                ax4_5.spines['left'].set_color(color_axes_pre)
                ax4_5.spines['right'].set_color(color_axes_pre)
                ax4_5.tick_params(colors=color_axes_pre)
                ax4_6.spines['top'].set_color(color_axes_pre)
                ax4_6.spines['bottom'].set_color(color_axes_pre)
                ax4_6.spines['left'].set_color(color_axes_pre)
                ax4_6.spines['right'].set_color(color_axes_pre)
                ax4_6.tick_params(colors=color_axes_pre)
                canvas4_3.draw()
                canvas4_5.draw()
                canvas4_6.draw()

            #三角プロット範囲指定あり
            def click4_C():
                global combobox4_5
                global combobox4_6
                global combobox4_7

                plt.rcParams["font.family"] = graph_font

                SUM=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())+data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())+data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                pX=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())/SUM*100 
                pY=data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())/SUM*100
                pZ=data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())/SUM*100
                data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat.columns=['X','Y','Z','SUM']

                data_z_SUM=data_gattai4_2[combobox4_5.get()]+data_gattai4_2[combobox4_6.get()]+data_gattai4_2[combobox4_7.get()]
                data_z_x=data_gattai4_2[combobox4_5.get()] #いらない列
                data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
                data_z.columns=['SUM','x']           

                zmax=data_z['SUM'].max()

                print(data_z["SUM"].sort_values())

                amari=zmax%10
                if amari==0:
                   baisuu=zmax
                else:
                   baisuu=zmax-amari+10

                if textBox4_13.get()=="":
                   tB4_13="0"
                else:
                   tB4_13=textBox4_13.get()

                if textBox4_14.get()=="":
                   tB4_14=baisuu
                else:
                   tB4_14=textBox4_14.get()

                #global data_gattai0
                if tB4_13=="0" and tB4_14==baisuu:
                   data_concat4_0_tri=data_concat
                   data_gattai4_0=data_gattai4_1
                else:
                   data_concat4_0_tri=data_concat[(data_z["SUM"]>=int(tB4_13))&(data_z["SUM"]<=int(tB4_14))]
                   data_gattai4_0=data_gattai4_1[(data_z["SUM"]>=int(tB4_13))&(data_z["SUM"]<=int(tB4_14))]

                print(data_gattai4_1)
                print(data_gattai4_0)
                print(data_concat4_0_tri)
                print("index list")
                print(list(data_concat4_0_tri.index))

                #重み付けなし普通の平均とデータの標準誤差、標準誤差
                #平均値
                mean_data = data_concat4_0_tri.mean()
                print("平均")
                print(mean_data)
                #標準偏差
                std_data = np.std(data_concat4_0_tri, ddof=1) #標本標準偏差
                print("標準偏差")
                print(std_data)
                #標準誤差
                ste_data = std_data/(len(data_concat4_0_tri)**(1/2))
                print("標準誤差")
                print(ste_data)

                #重み付き平均値
                δ_data = data_gattai4_0**(1/2)
                data_d_X = data_gattai4_0[combobox4_5.get()]/float(textBox4_30.get())
                data_d_Y = data_gattai4_0[combobox4_6.get()]/float(textBox4_31.get())
                data_d_Z = data_gattai4_0[combobox4_7.get()]/float(textBox4_32.get())
                data_d_sum = data_d_X+data_d_Y+data_d_Z
                δ_data_d_X = δ_data[combobox4_5.get()]/float(textBox4_30.get())
                δ_data_d_Y = δ_data[combobox4_6.get()]/float(textBox4_31.get())
                δ_data_d_Z = δ_data[combobox4_7.get()]/float(textBox4_32.get())
                δ_s = (δ_data_d_X**2+δ_data_d_Y**2+δ_data_d_Z**2)**(1/2)
                δ_X = 100*((δ_data_d_X/data_d_X)**2+(δ_s/data_d_sum)**2)**(1/2)
                δ_Y = 100*((δ_data_d_Y/data_d_Y)**2+(δ_s/data_d_sum)**2)**(1/2)
                δ_Z = 100*((δ_data_d_Z/data_d_Z)**2+(δ_s/data_d_sum)**2)**(1/2)
                σ_S = (δ_X**2+δ_Y**2+δ_Z**2)**(1/2)
                w_S = 1/((σ_S)**2)
                data_w_count_X = data_concat4_0_tri["X"]*w_S
                data_w_count_Y = data_concat4_0_tri["Y"]*w_S
                data_w_count_Z = data_concat4_0_tri["Z"]*w_S
                data_ave_w_X = np.sum(data_w_count_X)/np.sum(w_S)
                data_ave_w_Y = np.sum(data_w_count_Y)/np.sum(w_S)
                data_ave_w_Z = np.sum(data_w_count_Z)/np.sum(w_S)
                print("重みつき平均1")
                print("X")
                print(data_ave_w_X)
                print("Y")
                print(data_ave_w_Y)
                print("Z")
                print(data_ave_w_Z)
                #重み付き標準偏差
                data_zansa_X = data_concat4_0_tri["X"]-data_ave_w_X
                data_zansa_Y = data_concat4_0_tri["Y"]-data_ave_w_Y
                data_zansa_Z = data_concat4_0_tri["Z"]-data_ave_w_Z
                data_w_zansa2_X = w_S*(data_zansa_X**2)
                data_w_zansa2_Y = w_S*(data_zansa_Y**2)
                data_w_zansa2_Z = w_S*(data_zansa_Z**2)
                data_std_w_X = (np.sum(data_w_zansa2_X)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
                data_std_w_Y = (np.sum(data_w_zansa2_Y)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
                data_std_w_Z = (np.sum(data_w_zansa2_Z)/((len(data_concat)-1)*np.sum(w_S)))**(1/2)
                print("重みつき標準偏差1")
                print("X")
                print(data_std_w_X)
                print("Y")
                print(data_std_w_Y)
                print("Z")
                print(data_std_w_Z)

                print(tB4_14)
                print(zmax)
                print(data_concat4_0_tri)
                
                h = np.sqrt(3.0)*0.5

                global data_plot4_3
                plotx3=(100-data_concat4_0_tri['Y'])/100-data_concat4_0_tri['X']/200
                ploty3=h*data_concat4_0_tri['X']/100
                data_plot4_3=pd.concat([plotx3,ploty3],axis=1)
                data_plot4_3.columns=['x3','y3']

                print(data_plot4_3)

                global data_click_4
                data_click_4=pd.concat([data_concat4_0_tri,data_plot4_3],axis=1)
                data_click_4.columns=["a'","b'","c'","sum","x","y"]
                print("data_click")
                print(data_click_4)

                ax4_3.cla()
                fig4_3.set_facecolor(color_fig)
                ax4_3.set_facecolor(color_fig)

                for i in range(1,10):
                    ax4_3.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], linestyle='dashed',color='gray', lw=0.5)
                    ax4_3.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], linestyle='dashed',color='gray', lw=0.5)
                    ax4_3.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], linestyle='dashed',color='gray', lw=0.5)

                ax4_3.plot([0.0, 1.0],[0.0, 0.0], color=color_axes, lw=2)
                ax4_3.plot([0.0, 0.5],[0.0, h], color=color_axes, lw=2)
                ax4_3.plot([1.0, 0.5],[0.0, h], color=color_axes, lw=2)
  
                ax4_3.text(0.455, h+0.0283, combobox4_5.get(), fontsize=22, color=color_axes)
                ax4_3.text(-0.1, -0.02, combobox4_6.get(), fontsize=22, color=color_axes)
                ax4_3.text(1.02, -0.02, combobox4_7.get(), fontsize=22, color=color_axes)

                for i in range(1,10):
                    ax4_3.text(0.5+(10-i)/20.0+0.016, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize=17, color=color_axes)
                    ax4_3.text((10-i)/20.0-0.082, h*(10-i)/10.0, '%d0' % i, fontsize=17, color=color_axes)
                    ax4_3.text(i/10.0-0.03, -0.06, '%d0' % i, fontsize=17, color=color_axes)

                #ax4_3.text(0.84,h/2,'%'+combobox4_5.get(),fontsize=12, color=color_axes)
                #ax4_3.text(0.08,h/2,'%'+combobox4_6.get(),fontsize=12, color=color_axes)
                #ax4_3.text(0.5,-0.11,'%'+combobox4_7.get(),fontsize=12, color=color_axes)

                ax4_3.text(-0.15,1,"Number of particles:"+str(len(data_plot4_3.dropna())),fontsize=14, color=color_axes)

                ax4_3.scatter(data_plot4_3["x3"],data_plot4_3["y3"],c=color_plot,alpha=alpha_plot,s=size_plot)
                
                if not sansyou_4_1_a =="": #これを使う関数入れないといけない(def sansyou()のnewwindow4バージョン)
                    plot_sansyou_4_1_x = (100-float(sansyou_4_1_b))/100-float(sansyou_4_1_a)/200
                    plot_sansyou_4_1_y = h*float(sansyou_4_1_a)/100
                    print(plot_sansyou_4_1_x)
                    print(plot_sansyou_4_1_y)
                    global sansyou_4_1_sa
                    global sansyou_4_1_sb
                    global sansyou_4_1_sc
                    if sansyou_4_1_sa == "":
                        sansyou_4_1_sa = 0
                    if sansyou_4_1_sb == "":
                        sansyou_4_1_sb = 0
                    if sansyou_4_1_sc == "":
                        sansyou_4_1_sc = 0
                    ax4_3.scatter(plot_sansyou_4_1_x,plot_sansyou_4_1_y,c="red",alpha=1,s=20)
                    ax4_3.plot([plot_sansyou_4_1_x,plot_sansyou_4_1_x],[plot_sansyou_4_1_y-float(sansyou_4_1_sa)*h/100,plot_sansyou_4_1_y+float(sansyou_4_1_sa)*h/100],color="red",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_1_x-float(sansyou_4_1_sb)*h*h/100,plot_sansyou_4_1_x+float(sansyou_4_1_sb)*h*h/100],[plot_sansyou_4_1_y-float(sansyou_4_1_sb)*h/200,plot_sansyou_4_1_y+float(sansyou_4_1_sb)*h/200],color="red",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_1_x-float(sansyou_4_1_sc)*h*h/100,plot_sansyou_4_1_x+float(sansyou_4_1_sc)*h*h/100],[plot_sansyou_4_1_y+float(sansyou_4_1_sc)*h/200,plot_sansyou_4_1_y-float(sansyou_4_1_sc)*h/200],color="red",alpha=0.8,lw=1.2)

                if not sansyou_4_2_a =="":
                    plot_sansyou_4_2_x = (100-float(sansyou_4_2_b))/100-float(sansyou_4_2_a)/200
                    plot_sansyou_4_2_y = h*float(sansyou_4_2_a)/100
                    print(plot_sansyou_4_2_x)
                    print(plot_sansyou_4_2_y)
                    global sansyou_4_2_sa
                    global sansyou_4_2_sb
                    global sansyou_4_2_sc
                    if sansyou_4_2_sa == "":
                        sansyou_4_2_sa = 0
                    if sansyou_4_2_sb == "":
                        sansyou_4_2_sb = 0
                    if sansyou_4_2_sc == "":
                        sansyou_4_2_sc = 0
                    ax4_3.scatter(plot_sansyou_4_2_x,plot_sansyou_4_2_y,c="blue",alpha=1,s=20)
                    ax4_3.plot([plot_sansyou_4_2_x,plot_sansyou_4_2_x],[plot_sansyou_4_2_y-float(sansyou_4_2_sa)*h/100,plot_sansyou_4_2_y+float(sansyou_4_2_sa)*h/100],color="blue",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_2_x-float(sansyou_4_2_sb)*h*h/100,plot_sansyou_4_2_x+float(sansyou_4_2_sb)*h*h/100],[plot_sansyou_4_2_y-float(sansyou_4_2_sb)*h/200,plot_sansyou_4_2_y+float(sansyou_4_2_sb)*h/200],color="blue",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_2_x-float(sansyou_4_2_sc)*h*h/100,plot_sansyou_4_2_x+float(sansyou_4_2_sc)*h*h/100],[plot_sansyou_4_2_y+float(sansyou_4_2_sc)*h/200,plot_sansyou_4_2_y-float(sansyou_4_2_sc)*h/200],color="blue",alpha=0.8,lw=1.2)

                if not sansyou_4_3_a =="":
                    plot_sansyou_4_3_x = (100-float(sansyou_4_3_b))/100-float(sansyou_4_3_a)/200
                    plot_sansyou_4_3_y = h*float(sansyou_4_3_a)/100
                    print(plot_sansyou_4_3_x)
                    print(plot_sansyou_4_3_y)
                    global sansyou_4_3_sa
                    global sansyou_4_3_sb
                    global sansyou_4_3_sc
                    if sansyou_4_3_sa == "":
                        sansyou_4_3_sa = 0
                    if sansyou_4_3_sb == "":
                        sansyou_4_3_sb = 0
                    if sansyou_4_3_sc == "":
                        sansyou_4_3_sc = 0
                    ax4_3.scatter(plot_sansyou_4_3_x,plot_sansyou_4_3_y,c="green",alpha=1,s=20)
                    ax4_3.plot([plot_sansyou_4_3_x,plot_sansyou_4_3_x],[plot_sansyou_4_3_y-float(sansyou_4_3_sa)*h/100,plot_sansyou_4_3_y+float(sansyou_4_3_sa)*h/100],color="green",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_3_x-float(sansyou_4_3_sb)*h*h/100,plot_sansyou_4_3_x+float(sansyou_4_3_sb)*h*h/100],[plot_sansyou_4_3_y-float(sansyou_4_3_sb)*h/200,plot_sansyou_4_3_y+float(sansyou_4_3_sb)*h/200],color="green",alpha=0.8,lw=1.2)
                    ax4_3.plot([plot_sansyou_4_3_x-float(sansyou_4_3_sc)*h*h/100,plot_sansyou_4_3_x+float(sansyou_4_3_sc)*h*h/100],[plot_sansyou_4_3_y+float(sansyou_4_3_sc)*h/200,plot_sansyou_4_3_y-float(sansyou_4_3_sc)*h/200],color="green",alpha=0.8,lw=1.2)
                
                canvas4_3.draw()

            #三角柱プロット範囲指定なし
            def click4_A(): 
                global combobox4_5
                global combobox4_6
                global combobox4_7

                plt.rcParams["font.family"] = graph_font

                #データ決め 
                SUM=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())+data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())+data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                pX=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())/SUM*100 
                pY=data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())/SUM*100
                pZ=data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())/SUM*100
                data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat.columns=['X','Y','Z','SUM']

                data_z_SUM=data_gattai4_2[combobox4_5.get()]+data_gattai4_2[combobox4_6.get()]+data_gattai4_2[combobox4_7.get()]
                data_z_x=data_gattai4_2[combobox4_5.get()] #いらない列
                data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
                data_z.columns=['SUM','x']

                h = np.sqrt(3.0)*0.5
   
                #座標・軸決め
                zmax=data_z['SUM'].max()

                amari=zmax%10

                if amari==0:
                    baisuu=zmax
                else:
                    baisuu=zmax-amari+10

                NP1=np.linspace(0,baisuu,6,dtype=int)

                plotx4_1=(100-data_concat['Y'])/100-data_concat['X']/200
                ploty4_1=h*data_concat['X']/100
                plotz4_1=data_z['SUM']/baisuu 
                data_plot4_1=pd.concat([plotx4_1,ploty4_1,plotz4_1],axis=1)
                data_plot4_1.columns=['x1','y1','z1']

                #プロット場所決め
                fig4_1=plt.figure(figsize=(7.5,7.5))
                ax4_1=fig4_1.add_subplot(111,projection='3d')
                ax4_1.set_xticks([])
                ax4_1.set_yticks([])
                ax4_1.set_zticks([])
                plt.axis('off')
                ax4_1.view_init(elev=12,azim=-69)

                #三角グラフ描き
                fig4_1.set_facecolor(color_fig)
                ax4_1.set_facecolor(color_fig)

                for i in range(1,5):
                    ax4_1.plot([i*2/20.0, 1.0-i*2/20.0],[h*2*i/10.0, h*i*2/10.0],[0,0],color='gray', lw=0.5)
                    ax4_1.plot([i*2/20.0, i*2/10.0],[h*i*2/10.0, 0.0],[0,0], color='gray', lw=0.5)
                    ax4_1.plot([0.5+i*2/20.0, i*2/10.0],[h*(1.0-i*2/10.0), 0.0],[0,0],color='gray', lw=0.5)

                ax4_1.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
                ax4_1.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax4_1.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax4_1.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
                ax4_1.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
                ax4_1.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
                ax4_1.text(0.5, h+0.15,-0.1, combobox4_5.get(), fontsize=20,ha="center", color=color_axes)
                ax4_1.text(-0.15*h, -0.15/2,-0.1, combobox4_6.get(), fontsize=20,ha="center", color=color_axes)
                ax4_1.text(1+0.15*h, -0.15/2,-0.1, combobox4_7.get(), fontsize=20,ha="center", color=color_axes)

                for i in range(1,5):
                    ax4_1.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
                    ax4_1.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
                    ax4_1.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)

                ax4_1.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
                ax4_1.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
                ax4_1.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

                ax4_1.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

                for i in range(0,6):
                   ax4_1.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

                for i in range(0,6):
                   ax4_1.text(-0.078,-0.078,i/5-0.01,NP1[i],fontsize=20,ha="right", color=color_axes)

                ax4_1.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？
    
                ax4_1.set_xlim(0,1)
                ax4_1.set_ylim(0,1)
                ax4_1.set_zlim(0,1)

                #プロット
                ax4_1.scatter(data_plot4_1["x1"],data_plot4_1["y1"],data_plot4_1["z1"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

                #範囲指定のところに値が入っていた場合に全体表示のどの範囲にあたるかを示す
                if not textBox4_15.get() == "" or not textBox4_16.get() == "" :
                    if textBox4_15.get()=="":
                       tB4_15="0"
                    else:
                       tB4_15=textBox4_15.get()

                    if textBox4_16.get()=="":
                       tB4_16=baisuu
                    else:
                       tB4_16=textBox4_16.get()

                    tB4_15_range = int(tB4_15)/baisuu
                    tB4_16_range = int(tB4_16)/baisuu   

                    ax4_1.plot([0.0, 1.0],[0.0, 0.0],[tB4_15_range,tB4_15_range], color="red", lw=1.5)
                    ax4_1.plot([0.0, 0.5],[0.0, h],[tB4_15_range,tB4_15_range], color="red", lw=1.5)
                    ax4_1.plot([1.0, 0.5],[0.0, h],[tB4_15_range,tB4_15_range], color="red", lw=1.5)
                    ax4_1.plot([0.0, 0.0],[0.0, 0.0],[tB4_15_range,tB4_16_range], color="red", lw=1.5)
                    ax4_1.plot([1, 1],[0,0],[tB4_15_range,tB4_16_range], color="red", lw=1.5)
                    ax4_1.plot([0.5, 0.5],[h, h],[tB4_15_range,tB4_16_range], color="red", lw=1.5)
                    ax4_1.plot([0.0, 1.0],[0.0, 0.0],[tB4_16_range,tB4_16_range], color="red", lw=1.5)
                    ax4_1.plot([0.0, 0.5],[0.0, h],[tB4_16_range,tB4_16_range], color="red", lw=1.5)
                    ax4_1.plot([1.0, 0.5],[0.0, h],[tB4_16_range,tB4_16_range], color="red", lw=1.5)        

                fig4_1.show()

            #三角柱プロット範囲指定あり
            def click4_D(): 
                global combobox4_5
                global combobox4_6
                global combobox4_7

                plt.rcParams["font.family"] = graph_font

                SUM=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())+data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())+data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                pX=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())/SUM*100 
                pY=data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())/SUM*100
                pZ=data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())/SUM*100
                data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat.columns=['X','Y','Z','SUM']

                data_z_SUM=data_gattai4_2[combobox4_5.get()]+data_gattai4_2[combobox4_6.get()]+data_gattai4_2[combobox4_7.get()]
                data_z_x=data_gattai4_2[combobox4_5.get()] #いらない列
                data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
                data_z.columns=['SUM','x']

                h = np.sqrt(3.0)*0.5
     
                #座標決め
                zmax=data_z['SUM'].max()

                amari=zmax%10
                if amari==0:
                   baisuu=zmax
                else:
                   baisuu=zmax-amari+10

                plotx4_4=(100-data_concat['Y'])/100-data_concat['X']/200
                ploty4_4=h*data_concat['X']/100

                if textBox4_15.get()=="":
                   tB4_15="0"
                else:
                   tB4_15=textBox4_15.get()

                if textBox4_16.get()=="":
                   tB4_16=baisuu
                else:
                   tB4_16=textBox4_16.get()

                if tB4_15=="0" and tB4_16==baisuu:
                   zvalue=baisuu
                   plotz4_4=data_z['SUM']/zvalue
                   NP4_4=np.linspace(0,baisuu,6,dtype=int)
                else:
                   zvalue=int(tB4_16)-int(tB4_15)
                   plotz4_4=(data_z['SUM']-int(tB4_15))/zvalue
                   NP4_4=np.linspace(int(tB4_15),int(tB4_16),6,dtype=int) #少数になっちゃう可能性ありそうだけどだいじょうぶかな

                data_plot4_4=pd.concat([plotx4_4,ploty4_4,plotz4_4],axis=1)
                data_plot4_4.columns=['x4','y4','z4']
                data_plot4_40=data_plot4_4[(data_plot4_4["z4"]>=0)&(data_plot4_4["z4"]<=1)]

                #プロット場所決め
                fig4_4=plt.figure(figsize=(7.5,7.5))
                ax4_4=fig4_4.add_subplot(111,projection='3d')
                ax4_4.set_xticks([])
                ax4_4.set_yticks([])
                ax4_4.set_zticks([])
                plt.axis('off')
                ax4_4.view_init(elev=12,azim=-69)

                #三角グラフ描き
                fig4_4.set_facecolor(color_fig)
                ax4_4.set_facecolor(color_fig)

                for i in range(1,5):
                    ax4_4.plot([2*i/20.0, 1.0-2*i/20.0],[h*2*i/10.0, h*2*i/10.0],[0,0],color='gray', lw=0.5)
                    ax4_4.plot([2*i/20.0, 2*i/10.0],[h*2*i/10.0, 0.0],[0,0], color='gray', lw=0.5)
                    ax4_4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[0,0], color='gray', lw=0.5)

                ax4_4.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
                ax4_4.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax4_4.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax4_4.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
                ax4_4.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
                ax4_4.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
                ax4_4.text(0.5, h+0.15,-0.1, combobox4_5.get(), fontsize=20,ha="center", color=color_axes)
                ax4_4.text(-0.15*h, -0.15/2,-0.1, combobox4_6.get(), fontsize=20,ha="center", color=color_axes)
                ax4_4.text(1+0.15*h, -0.15/2,-0.1, combobox4_7.get(), fontsize=20,ha="center", color=color_axes)

                for i in range(1,5):
                    ax4_4.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
                    ax4_4.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
                    ax4_4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)

                ax4_4.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
                ax4_4.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
                ax4_4.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

                ax4_4.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

                for i in range(0,6):
                   ax4_4.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

                for i in range(0,6):
                   ax4_4.text(-0.078,-0.078,i/5-0.01,NP4_4[i],fontsize=20,ha="right", color=color_axes)

                ax4_4.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？

                ax4_4.set_xlim(0,1)
                ax4_4.set_ylim(0,1)
                ax4_4.set_zlim(0,1)

                #プロット
                ax4_4.scatter(data_plot4_40["x4"],data_plot4_40["y4"],data_plot4_40["z4"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

                fig4_4.show()

            def click4_E():
                global combobox4_5
                global combobox4_6
                global combobox4_7
                global combobox4_8
                global combobox4_9

                SUM=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())+data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())+data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                pX=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())/SUM*100 
                pY=data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())/SUM*100
                pZ=data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())/SUM*100
                data_concat=pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat.columns=['X','Y','Z','SUM']

                data_z_SUM=data_gattai4_2[combobox4_5.get()]+data_gattai4_2[combobox4_6.get()]+data_gattai4_2[combobox4_7.get()]
                data_z_x=data_gattai4_2[combobox4_5.get()] #いらない列
                data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
                data_z.columns=['SUM','x']           

                zmax=data_z['SUM'].max()

                amari=zmax%10
                if amari==0:
                   baisuu=zmax
                else:
                   baisuu=zmax-amari+10

                if textBox4_13.get()=="":
                   tB4_13="0"
                else:
                   tB4_13=textBox4_13.get()

                if textBox4_14.get()=="":
                   tB4_14=baisuu
                else:
                   tB4_14=textBox4_14.get()

                if tB4_13=="0" and tB4_14==baisuu:
                   data_concat0=data_concat
                else:
                   data_concat0=data_concat[(data_z["SUM"]>=int(tB4_13))&(data_z["SUM"]<=int(tB4_14))]


                if textBox4_18.get()=="":
                    tB4_18="0"
                else:
                    tB4_18=textBox4_18.get()

                if textBox4_19.get()=="":
                    tB4_19="100"
                else:
                    tB4_19=textBox4_19.get()

                if combobox4_8.get()==combobox4_5.get():
                    if tB4_18=="0" and tB4_19=="100":
                        data_concat00=data_concat0
                    else:
                        data_concat00=data_concat0[(data_concat0['X']>=int(tB4_18))&(data_concat0['X']<=int(tB4_19))]

                    if combobox4_9.get()==combobox4_6.get():
                        count=data_concat00['Y']/(data_concat00['Y']+data_concat00['Z'])*100
                        perelement=combobox4_6.get()
                    elif combobox4_9.get()==combobox4_7.get():
                        count=data_concat00['Z']/(data_concat00['Y']+data_concat00['Z'])*100
                        perelement=combobox4_7.get()   
                    elif combobox4_9.get()=="":
                        messagebox.showerror('エラー','割合を見る元素を指定してください') 
                    else:
                        messagebox.showerror('エラー','元素は'+combobox4_5.get()+"または"+combobox4_6.get()+"または"+combobox4_7.get()+'のいずれかを重複せずに入力してください') 
                elif combobox4_8.get()==combobox4_6.get():        
                    if tB4_18=="0" and tB4_19=="100":
                        data_concat00=data_concat0
                    else:
                        data_concat00=data_concat0[(data_concat0['Y']>=int(tB4_18))&(data_concat0['Y']<=int(tB4_19))]
      
                    if combobox4_9.get()==combobox4_7.get():
                        count=data_concat00['Z']/(data_concat00['Z']+data_concat00['X'])*100
                        perelement=combobox4_7.get()
                    elif combobox4_9.get()==combobox4_5.get():
                        count=data_concat00['X']/(data_concat00['Z']+data_concat00['X'])*100
                        perelement=combobox4_5.get() 
                    elif combobox4_9.get()=="":
                        messagebox.showerror('エラー','割合を見る元素を指定してください')       
                    else:
                        messagebox.showerror('エラー','元素は'+combobox4_5.get()+"または"+combobox4_6.get()+"または"+combobox4_7.get()+'のいずれかを入力してください') 
                elif combobox4_8.get()==combobox4_7.get():
                    if tB4_18=="0" and tB4_19=="100":
                        data_concat00=data_concat0
                    else:
                        data_concat00=data_concat0[(data_concat0['Z']>=int(tB4_18))&(data_concat0['Z']<=int(tB4_19))]
      
                    if combobox4_9.get()==combobox4_5.get():
                        count=data_concat00['X']/(data_concat00['X']+data_concat00['Y'])*100
                        perelement=combobox4_5.get()
                    elif combobox4_9.get()==combobox4_6.get():
                        count=data_concat00['Y']/(data_concat00['X']+data_concat00['Y'])*100 
                        perelement=combobox4_6.get()
                    elif combobox4_9.get()=="":
                        messagebox.showerror('error','割合を見る元素を指定してください') 
                    else:
                        messagebox.showerror('error','元素は'+combobox4_5.get()+"または"+combobox4_6.get()+"または"+combobox4_7.get()+'のいずれかを入力してください') 
                elif combobox4_8.get()=="":
                    messagebox.showerror('error','範囲を固定する元素を指定してください')
                else:
                    messagebox.showerror('error','元素は'+combobox4_5.get()+"または"+combobox4_6.get()+"または"+combobox4_7.get()+'のいずれかを入力してください')

                data_z_c=pd.concat([count,data_z_SUM],axis=1)
                data_z_c.columns=['X','SUM']     
                print(data_z_c)
                data_z_0 = data_z_c.dropna(how="any")

                #重み付けなし普通の平均とデータの標準誤差、標準誤差
                #平均値
                mean_data = count.mean()
                print("平均")
                print(mean_data)
                #標準偏差
                std_data = np.std(count, ddof=1) #標本標準偏差でいいよね
                print("標準偏差")
                print(std_data)
                #標準誤差
                ste_data = std_data/(len(count)**(1/2))
                print("標準誤差")
                print(ste_data)

                print(data_z_0)
                #平均値4
                δ_data = data_gattai4_1**(1/2)
                data_d_X = data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())
                data_d_Z = data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                data_d_sum = data_d_X+data_d_Z
                δ_data_d_X = δ_data[combobox4_5.get()]/float(textBox4_30.get())
                δ_data_d_Z = δ_data[combobox4_7.get()]/float(textBox4_32.get())
                δ_s = (δ_data_d_X**2+δ_data_d_Z**2)**(1/2)
                δ_X = 100*((δ_data_d_X/data_d_X)**2+(δ_s/data_d_sum)**2)**(1/2)
                δ_Z = 100*((δ_data_d_Z/data_d_Z)**2+(δ_s/data_d_sum)**2)**(1/2)
                σ_S = (δ_X**2+δ_Z**2)**(1/2)
                w_S = 1/((σ_S)**2)
                data_z_00 = pd.concat([data_z_c,w_S],axis=1)
                data_z_000 = data_z_00.dropna(how="any")
                data_z_000.columns=['X','SUM','w']  
                data_w_count_X = data_z_000["X"]*data_z_000["w"]
                data_ave_w_X = np.sum(data_w_count_X)/np.sum(data_z_000["w"])
                print("重みつき平均4")
                print("X")
                print(data_ave_w_X)
                #標準偏差4
                data_zansa_X = data_z_0["X"]-data_ave_w_X
                data_w_zansa2_X = w_S*(data_zansa_X**2)
                data_std_w_X = (np.sum(data_w_zansa2_X)/((len(data_z_0["X"])-1)*np.sum(w_S)))**(1/2)
                print("重みつき標準偏差1")
                print("X")
                print(data_std_w_X)

                tB4_33=combobox4_1.get()

                times=100/int(tB4_33)

                Num4_X=[]
                for i in range(0,int(times)):
                    Num4_X.append(np.count_nonzero((count>=i*int(tB4_33))&(count<=(i+1)*int(tB4_33))))

                    #上でエラーの表示になるときはここでエラー出るからグラフかく操作もif文の中に入れたほうがいいかな？

                ax4_5.cla()

                plt.rcParams["font.family"] = graph_font

                fig4_5.set_facecolor(color_fig)
                ax4_5.set_facecolor(color_fig)

                ax4_5.spines['top'].set_color(color_axes)
                ax4_5.spines['bottom'].set_color(color_axes)
                ax4_5.spines['left'].set_color(color_axes)
                ax4_5.spines['right'].set_color(color_axes)
                ax4_5.tick_params(colors=color_axes)

                left=np.linspace(0,100-int(tB4_33),int(times),dtype=int)
                height=np.array(Num4_X)
                if bar_style == "枠あり":   
                    ax4_5.bar(left,height,width=int(tB4_33),color=color_bar,linewidth=1,edgecolor=color_axes,align="edge",zorder=2)
                elif bar_style == "枠なし":
                    ax4_5.bar(left,height,width=int(tB4_33)* 0.8,color=color_bar,align="edge",zorder=2)
                ax4_5.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
                ax4_5.set_xlabel("%"+perelement,fontname=graph_font,color=color_axes,weight=weight_font)
                ax4_5.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

                canvas4_5.draw()


            #カウント分布
            def click4_F():
                global combobox4_5
                global combobox4_6
                global combobox4_7

                plt.rcParams["font.family"] = graph_font
            
                SUM=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())+data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())+data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())
                pX=data_gattai4_1[combobox4_5.get()]/float(textBox4_30.get())/SUM*100 
                pY=data_gattai4_1[combobox4_6.get()]/float(textBox4_31.get())/SUM*100
                pZ=data_gattai4_1[combobox4_7.get()]/float(textBox4_32.get())/SUM*100
                data_concat=pd.concat([pX,pY,pZ],axis=1)
                data_concat.columns=['X','Y','Z']

                data_z_SUM=data_gattai4_2[combobox4_5.get()]+data_gattai4_2[combobox4_6.get()]+data_gattai4_2[combobox4_7.get()]
                data_z_x=data_gattai4_2[combobox4_5.get()] #いらない列
                data_z=pd.concat([data_z_SUM,data_z_x],axis=1)
                data_z.columns=['SUM','x']

                data_concat_z=pd.concat([data_concat,data_z],axis=1)

                if textBox4_21.get()=="":
                    tB4_21="0"
                else:
                    tB4_21=textBox4_21.get()

                if textBox4_22.get()=="":
                    tB4_22="100"
                else:
                    tB4_22=textBox4_22.get()
            
                if textBox4_23.get()=="":
                    tB4_23="0"
                else:
                    tB4_23=textBox4_23.get()

                if textBox4_24.get()=="":
                    tB4_24="100"
                else:
                    tB4_24=textBox4_24.get()
        
                if textBox4_25.get()=="":
                    tB4_25="0"
                else:
                    tB4_25=textBox4_25.get()

                if textBox4_26.get()=="":
                    tB4_26="100"
                else:
                    tB4_26=textBox4_26.get()

                data_concat0=data_concat_z[(data_concat_z["X"]>=int(tB4_21))&(data_concat_z["X"]<=int(tB4_22))&(data_concat_z["Y"]>=int(tB4_23))&(data_concat_z["Y"]<=int(tB4_24))&(data_concat_z["Z"]>=int(tB4_25))&(data_concat_z["Z"]<=int(tB4_26))]
                zmax0=data_concat0['SUM'].max()

                amari=zmax0%10
                if amari==0:
                   baisuu=zmax0
                else:
                   baisuu=zmax0-amari+10

                if textBox4_27.get()=="":
                    tB4_27="0"
                else:
                    tB4_27=textBox4_27.get()

                if textBox4_28.get()=="":
                    tB4_28=baisuu
                else:
                    tB4_28=textBox4_28.get()
            
                if textBox4_29.get()=="":
                    tB4_29=5
                else:
                    tB4_29=textBox4_29.get()


                if len(data_concat0)==0:
                    if int(tB4_25)<100-(int(tB4_22)+int(tB4_24)) or int(tB4_26)>100-(int(tB4_21)+int(tB4_23)):
                        messagebox.showerror('エラー','範囲が間違っています')
                    else:
                        messagebox.showerror('エラー','範囲内にデータがありません')
                else:
                    pltmin=int(tB4_27)
                    amari0=int(tB4_28)%10
                    if amari0==0:
                        pltmax=int(tB4_28)
                    else:
                        pltmax=int(tB4_28)-amari0+10

                    ax4_6.cla()

                    fig4_6.set_facecolor(color_fig)
                    ax4_6.set_facecolor(color_fig)

                    ax4_6.spines['top'].set_color(color_axes)
                    ax4_6.spines['bottom'].set_color(color_axes)
                    ax4_6.spines['left'].set_color(color_axes)
                    ax4_6.spines['right'].set_color(color_axes)
                    ax4_6.tick_params(colors=color_axes)
    
                    if bar_style == "枠あり":
                        ax4_6.hist(data_concat0["SUM"],bins=np.arange(pltmin,pltmax+int(tB4_29),int(tB4_29)),color=color_bar,linewidth=1,edgecolor=color_axes,zorder=2)
                    elif bar_style == "枠なし":
                        ax4_6.hist(data_concat0["SUM"],bins=np.arange(pltmin,pltmax+int(tB4_29),int(tB4_29)),width = int(tB4_29) * 0.8,color=color_bar,zorder=2)
                    ax4_6.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
                    ax4_6.set_xlabel("Counts",fontname=graph_font,color=color_axes,weight=weight_font)
                    ax4_6.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

                    canvas4_6.draw()

            fig4_3 = plt.figure(figsize=(6.42,6.42))
            ax4_3 = fig4_3.add_subplot(111)
            ax4_3.set_aspect('equal', 'datalim')
            plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
            plt.tick_params(bottom=False, left=False, right=False, top=False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            canvas4_3=FigureCanvasTkAgg(fig4_3,master=newwindow4)
            canvas4_3.get_tk_widget().place(x=341,y=29)
            canvas4_3._tkcanvas.place(x=341,y=29)
            #fig4_3.canvas.mpl_connect("button_press_event",onclick_4)#とりあえず保留
            btn4_12=tk.Button(newwindow4,text="読み込み",command=click_element_4,font=(label_font_jp,8))
            btn4_12.place(width=50,height=25,x=270,y=98)
            btn4_1=tk.Button(newwindow4,text="読み込み",command=click4_1,font=(label_font_jp,8))
            btn4_1.place(width=50,height=25,x=270,y=143)
            btn4_2=tk.Button(newwindow4,text="決定",command=click4_2,font=(label_font_jp,9))
            btn4_2.place(width=160,height=25,x=120,y=280)
            btn4_4=tk.Button(newwindow4,text="表示",command=click4_C,font=(label_font_jp,9))
            btn4_4.place(width=50,height=25,x=215,y=359)
            btn4_5=tk.Button(newwindow4,text="全体表示",command=click4_A,font=(label_font_jp,9))
            btn4_5.place(width=90,height=25,x=60,y=440)
            btn4_6=tk.Button(newwindow4,text="表示",command=click4_D,font=(label_font_jp,9))
            btn4_6.place(width=50,height=25,x=215,y=469)
            btn4_7=tk.Button(newwindow4,text="表示",command=click4_E,font=(label_font_jp,9))
            btn4_7.place(width=50,height=25,x=215,y=609)
            btn4_8=tk.Button(newwindow4,text="表示",command=click4_F,font=(label_font_jp,9))
            btn4_8.place(width=50,height=25,x=215,y=809)

            label4_3=tk.Label(newwindow4,text="元素",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
            label4_3.place(width=100,height=20,x=12,y=100)
            label4_3_2=tk.Label(newwindow4,text="質量数",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
            label4_3_2.place(width=100,height=20,x=12,y=145)
            label4_3_4=tk.Label(newwindow4,text="補正",anchor=tk.CENTER,bg=color2,font=(label_font_jp,9))
            label4_3_4.place(width=100,height=20,x=12,y=235)
            textBox4_30=tk.Entry(newwindow4)
            textBox4_30.place(width=40,height=20,x=120,y=235)
            textBox4_31=tk.Entry(newwindow4)
            textBox4_31.place(width=40,height=20,x=170,y=235)
            textBox4_32=tk.Entry(newwindow4)
            textBox4_32.place(width=40,height=20,x=220,y=235)

            label4_20=tk.Label(newwindow4,text="三角グラフ",anchor=tk.W,bg=color3,font=(label_font_jp,10))#,'underline'))
            label4_20.place(width=67,height=16,x=20,y=330)

            textBox4_13=tk.Entry(newwindow4)
            textBox4_13.place(width=40,height=20,x=110,y=360)
            textBox4_14=tk.Entry(newwindow4)
            textBox4_14.place(width=40,height=20,x=160,y=360)
            label4_7=tk.Label(newwindow4,text="-",bg=color7,font=(label_font,10))
            label4_7.place(width=10,height=20,x=150,y=360)
            label4_24=tk.Label(newwindow4,text="カウント",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_24.place(width=50,height=20,x=60,y=360)       

            label4_21=tk.Label(newwindow4,text="三角柱グラフ",anchor=tk.W,bg=color4,font=(label_font_jp,10))#,'underline'))
            label4_21.place(width=80,height=16,x=20,y=410)

            textBox4_15=tk.Entry(newwindow4)
            textBox4_15.place(width=40,height=20,x=110,y=470)
            textBox4_16=tk.Entry(newwindow4)
            textBox4_16.place(width=40,height=20,x=160,y=470)
            label4_8=tk.Label(newwindow4,text="-",bg=color7,font=(label_font,10))
            label4_8.place(width=10,height=20,x=150,y=470)
            label4_25=tk.Label(newwindow4,text="カウント",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_25.place(width=50,height=20,x=60,y=470)       

            label4_22=tk.Label(newwindow4,text="組成分布",anchor=tk.W,bg=color5,font=(label_font_jp,10))#,'underline'))
            label4_22.place(width=57,height=16,x=20,y=520)

            textBox4_18=tk.Entry(newwindow4)
            textBox4_18.place(width=40,height=20,x=156,y=550)
            textBox4_19=tk.Entry(newwindow4)
            textBox4_19.place(width=40,height=20,x=205,y=550)
            label4_9=tk.Label(newwindow4,text=":",bg=color7,font=(label_font_jp,10))
            label4_9.place(width=3,height=20,x=151,y=550)
            label4_10=tk.Label(newwindow4,text="-",bg=color7,font=(label_font_jp,10))
            label4_10.place(width=10,height=20,x=195,y=550)
            label4_29=tk.Label(newwindow4,text="%",bg=color7,font=(label_font_jp,9))
            label4_29.place(width=20,height=20,x=248,y=550) 
            label4_26=tk.Label(newwindow4,text="固定",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_26.place(width=50,height=20,x=60,y=550) 
            label4_27=tk.Label(newwindow4,text="表示",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_27.place(width=50,height=20,x=60,y=580) 
            label4_30=tk.Label(newwindow4,text="幅",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_30.place(width=50,height=20,x=60,y=610) 

            label4_22=tk.Label(newwindow4,text="カウント分布",anchor=tk.W,bg=color6,font=(label_font_jp,10))#,'underline'))
            label4_22.place(width=80,height=16,x=20,y=660)

            textBox4_21=tk.Entry(newwindow4)
            textBox4_21.place(width=40,height=20,x=110,y=690)
            textBox4_22=tk.Entry(newwindow4)
            textBox4_22.place(width=40,height=20,x=160,y=690)
            textBox4_23=tk.Entry(newwindow4)
            textBox4_23.place(width=40,height=20,x=110,y=720)
            textBox4_24=tk.Entry(newwindow4)
            textBox4_24.place(width=40,height=20,x=160,y=720)
            textBox4_25=tk.Entry(newwindow4)
            textBox4_25.place(width=40,height=20,x=110,y=750)
            textBox4_26=tk.Entry(newwindow4)
            textBox4_26.place(width=40,height=20,x=160,y=750)
            label4_11=tk.Label(newwindow4,text=combobox4_5.get()+":",bg=color7,font=(label_font_jp,10))
            label4_11.place(width=20,height=20,x=80,y=690)
            label4_12=tk.Label(newwindow4,text="-",bg=color7,font=(label_font_jp,10))
            label4_12.place(width=10,height=20,x=150,y=690)
            label4_13=tk.Label(newwindow4,text="%",bg=color7,font=(label_font_jp,9))
            label4_13.place(width=20,height=20,x=203,y=690)
            label4_14=tk.Label(newwindow4,text=combobox4_6.get()+":",bg=color7,font=(label_font_jp,10))
            label4_14.place(width=20,height=20,x=80,y=720)
            label4_15=tk.Label(newwindow4,text="-",bg=color7,font=(label_font_jp,10))
            label4_15.place(width=10,height=20,x=150,y=720)
            label4_16=tk.Label(newwindow4,text="%",bg=color7,font=(label_font_jp,9))
            label4_16.place(width=20,height=20,x=203,y=720)
            label4_17=tk.Label(newwindow4,text=combobox4_7.get()+":",bg=color7,font=(label_font_jp,10))
            label4_17.place(width=20,height=20,x=80,y=750)
            label4_18=tk.Label(newwindow4,text="-",bg=color7,font=(label_font_jp,10))
            label4_18.place(width=10,height=20,x=150,y=750)
            label4_19=tk.Label(newwindow4,text="%",bg=color7,font=(label_font_jp,9))
            label4_19.place(width=20,height=20,x=203,y=750)

            textBox4_27=tk.Entry(newwindow4)
            textBox4_27.place(width=40,height=20,x=110,y=780)
            textBox4_28=tk.Entry(newwindow4)
            textBox4_28.place(width=40,height=20,x=160,y=780)      
            label4_28=tk.Label(newwindow4,text="-",bg=color7,font=(label_font,10))
            label4_28.place(width=10,height=20,x=150,y=780)
            label4_31=tk.Label(newwindow4,text="カウント",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_31.place(width=50,height=20,x=60,y=780) 
            textBox4_29=tk.Entry(newwindow4)
            textBox4_29.place(width=40,height=20,x=110,y=810) 
            label4_32=tk.Label(newwindow4,text="幅",anchor=tk.CENTER,bg=color7,font=(label_font_jp,9))
            label4_32.place(width=50,height=20,x=60,y=810) 
            
            def savefig4_3():
                file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
                print(file_path)

                if len(file_path) != 0:
                    fig4_3.savefig(file_path)
                
            def savefig4_5():
                file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
                print(file_path)
                
                if len(file_path) != 0:
                    fig4_5.savefig(file_path)

            def savefig4_6():
                file_path = tkinter.filedialog.asksaveasfilename(defaultextension="png",filetypes=[("PNG(*.png)","*.png")])
                print(file_path)
                
                if len(file_path) != 0:
                    fig4_6.savefig(file_path)

            menubar_4 = tk.Menu(newwindow4)
            newwindow4.config(menu = menubar_4)

            savefig_menu_4 = tk.Menu(menubar_4,tearoff = 0)
            menubar_4.add_cascade(label = "グラフ保存",menu = savefig_menu_4)

            savefig_menu_4.add_command(label = "三角グラフ",command = savefig4_3)
            savefig_menu_4.add_command(label = "組成分布",command = savefig4_5)
            savefig_menu_4.add_command(label = "カウント分布",command = savefig4_6)



    def Cancel3():
        newwindow3.destroy()

    btn15=tk.Button(newwindow3,text="決定",command=OK3)
    btn15.place(width=80,height=25,x=20,y=130)
    btn16=tk.Button(newwindow3,text="キャンセル",command=Cancel3)
    btn16.place(width=80,height=25,x=110,y=130)

def choutenplus():
    if textBox2.get() == "":
        messagebox.showerror("エラー","ファイルを選択してください")
    else:
        data_csv_p = pd.read_csv(textBox2.get())
        isotope_df_0_p = data_csv_p.columns
        isotope_df_p = isotope_df_0_p[1:len(isotope_df_0_p)-1]
        isotope_list_p = isotope_df_p.values.tolist()
        print(isotope_list_p)
        ele_list_p = []
        for i in range(0,len(isotope_list_p)):
            alpha_p_i = "".join([s for s in isotope_list_p[i] if s.isalpha()])
            ele_list_p.append(alpha_p_i)
        print(ele_list_p)
        mass_list_p = []
        for i in range(0,len(isotope_list_p)):
            digit_p_i = "".join([s for s in isotope_list_p[i] if s.isdigit()])
            mass_list_p.append(digit_p_i)
        print(mass_list_p)
        ele_list_min_p = list(set(ele_list_p))
        ele_list_min_p.sort()
        ele_list_min_ini_p = list(set(ele_list_p))
        ele_list_min_ini_p.sort()
        ele_list_min_bar_p = list(set(ele_list_p))
        ele_list_min_bar_p.sort()
        ele_list_min_bar_p.insert(0,"-")
        ele_list_min_zero_p = list(set(ele_list_p))
        ele_list_min_zero_p.sort()
        ele_list_min_zero_p.append("-")
        print(ele_list_min_p)
        print(ele_list_min_zero_p)

        if len(ele_list_min_p) > 10:
            messagebox.showerror("エラー","元素数が多すぎます")
        else:
            while len(ele_list_min_p) < 10:
                ele_list_min_p.append('-')
        
        print(ele_list_min_p)

        if ele_list_min_p[0] == "-":
            messagebox.showerror('エラー',"最低３元素は測定してください")
        else:
            iso_list_p1 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[0]]
            mass_list_p1 = []
            for i in range(0,len(iso_list_p1)):
                iso_index_p_i = iso_list_p1[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p1.append(mass_p_i)
            print(mass_list_p1)
        if ele_list_min_p[1] == "-":
            messagebox.showerror('エラー',"最低３元素は測定してください")
        else:
            iso_list_p2 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[1]]
            mass_list_p2 = []
            for i in range(0,len(iso_list_p2)):
                iso_index_p_i = iso_list_p2[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p2.append(mass_p_i)
            print(mass_list_p2)
        if ele_list_min_p[2] == "-":
            messagebox.showerror('エラー',"最低３元素は測定してください")
        else:
            iso_list_p3 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[2]]
            mass_list_p3 = []
            for i in range(0,len(iso_list_p3)):
                iso_index_p_i = iso_list_p3[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p3.append(mass_p_i)
            print(mass_list_p3)
        if ele_list_min_p[3] == "-":
            mass_list_p4 = ["-"]
        else:
            iso_list_p4 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[3]]
            mass_list_p4 = []
            for i in range(0,len(iso_list_p4)):
                iso_index_p_i = iso_list_p4[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p4.append(mass_p_i)
            print(mass_list_p4)
        if ele_list_min_p[4] == "-":
            mass_list_p5 = ["-"]
        else:
            iso_list_p5 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[4]]
            mass_list_p5 = []
            for i in range(0,len(iso_list_p5)):
                iso_index_p_i = iso_list_p5[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p5.append(mass_p_i)
            print(mass_list_p5)
        if ele_list_min_p[5] == "-":
            mass_list_p6 = ["-"]
        else:
            iso_list_p6 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[5]]
            mass_list_p6 = []
            for i in range(0,len(iso_list_p6)):
                iso_index_p_i = iso_list_p6[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p6.append(mass_p_i)
            print(mass_list_p6)
        if ele_list_min_p[6] == "-":
            mass_list_p7 = ["-"]
        else:
            iso_list_p7 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[6]]
            mass_list_p7 = []
            for i in range(0,len(iso_list_p7)):
                iso_index_p_i = iso_list_p7[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p7.append(mass_p_i)
            print(mass_list_p7)
        if ele_list_min_p[7] == "-":
            mass_list_p8 = ["-"]
        else:
            iso_list_p8 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[7]]
            mass_list_p8 = []
            for i in range(0,len(iso_list_p8)):
                iso_index_p_i = iso_list_p8[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p8.append(mass_p_i)
            print(mass_list_p8)
        if ele_list_min_p[8] == "-":
            mass_list_p9 = ["-"]
        else:
            iso_list_p9 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[8]]
            mass_list_p9 = []
            for i in range(0,len(iso_list_p9)):
                iso_index_p_i = iso_list_p9[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p9.append(mass_p_i)
            print(mass_list_p9)
        if ele_list_min_p[9] == "-":
            mass_list_p10 = ["-"]
        else:
            iso_list_p10 = [k for k, x in enumerate(ele_list_p) if x == ele_list_min_p[9]]
            mass_list_p10 = []
            for i in range(0,len(iso_list_p10)):
                iso_index_p_i = iso_list_p10[i]
                mass_p_i = mass_list_p[int(iso_index_p_i)]
                mass_list_p10.append(mass_p_i)
            print(mass_list_p10)


        iso_list_abd_p1 = [k for k, x in enumerate(element_list["Atomic Symbol"]) if x == ele_list_min_p[0]]
        mass_list_abd_p1 = []
        for i in range(0,len(iso_list_abd_p1)):
            iso_index_abd_p_i = iso_list_abd_p1[i]
            massnumber = element_list["Mass Number"]
            mass_abd_p_i = massnumber[int(iso_index_abd_p_i)]
            mass_list_abd_p1.append(mass_abd_p_i)
        print(mass_list_abd_p1)
        #残り９個についても後でやらないといけない(同位体存在度で補正できるようにするとき)

        newwindow_p = tk.Toplevel(root)
        newwindow_p.attributes("-topmost",True)
        newwindow_p.geometry("890x200")
        newwindow_p.title(u"元素読み込み")

        label_p01 = tk.Label(newwindow_p,text="元素",font=(label_font_jp,10),anchor=tk.CENTER)
        label_p01.place(width=50,height=20,x=20,y=20)
        label_p02 = tk.Label(newwindow_p,text="質量数",font=(label_font_jp,10),anchor=tk.CENTER)
        label_p02.place(width=50,height=20,x=20,y=60)
        label_p03 = tk.Label(newwindow_p,text="補正",font=(label_font_jp,10),anchor=tk.CENTER)
        label_p03.place(width=50,height=20,x=20,y=100)

        label_p1 = tk.Label(newwindow_p,text=ele_list_min_p[0],font=(label_font_jp,10))
        label_p1.place(width=50,height=20,x=90,y=20)
        label_p2 = tk.Label(newwindow_p,text=ele_list_min_p[1],font=(label_font_jp,10))
        label_p2.place(width=50,height=20,x=170,y=20)
        label_p3 = tk.Label(newwindow_p,text=ele_list_min_p[2],font=(label_font_jp,10))
        label_p3.place(width=50,height=20,x=250,y=20)
        label_p4 = tk.Label(newwindow_p,text=ele_list_min_p[3],font=(label_font_jp,10))
        label_p4.place(width=50,height=20,x=330,y=20)
        label_p5 = tk.Label(newwindow_p,text=ele_list_min_p[4],font=(label_font_jp,10))
        label_p5.place(width=50,height=20,x=410,y=20)
        label_p6 = tk.Label(newwindow_p,text=ele_list_min_p[5],font=(label_font_jp,10))
        label_p6.place(width=50,height=20,x=490,y=20)
        label_p7 = tk.Label(newwindow_p,text=ele_list_min_p[6],font=(label_font_jp,10))
        label_p7.place(width=50,height=20,x=570,y=20)
        label_p8 = tk.Label(newwindow_p,text=ele_list_min_p[7],font=(label_font_jp,10))
        label_p8.place(width=50,height=20,x=650,y=20)
        label_p9 = tk.Label(newwindow_p,text=ele_list_min_p[8],font=(label_font_jp,10))
        label_p9.place(width=50,height=20,x=730,y=20)
        label_p10 = tk.Label(newwindow_p,text=ele_list_min_p[9],font=(label_font_jp,10))
        label_p10.place(width=50,height=20,x=810,y=20)

        combobox_p1 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p1)
        combobox_p1.place(width=50,height=20,x=90,y=60)
        combobox_p1.current(0)
        combobox_p2 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p2)
        combobox_p2.place(width=50,height=20,x=170,y=60)
        combobox_p2.current(0)
        combobox_p3 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p3)
        combobox_p3.place(width=50,height=20,x=250,y=60)
        combobox_p3.current(0)
        combobox_p4 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p4)
        combobox_p4.place(width=50,height=20,x=330,y=60)
        combobox_p4.current(0)
        combobox_p5 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p5)
        combobox_p5.place(width=50,height=20,x=410,y=60)
        combobox_p5.current(0)
        combobox_p6 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p6)
        combobox_p6.place(width=50,height=20,x=490,y=60)
        combobox_p6.current(0)
        combobox_p7 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p7)
        combobox_p7.place(width=50,height=20,x=570,y=60)
        combobox_p7.current(0)
        combobox_p8 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p8)
        combobox_p8.place(width=50,height=20,x=650,y=60)
        combobox_p8.current(0)
        combobox_p9 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p9)
        combobox_p9.place(width=50,height=20,x=730,y=60)
        combobox_p9.current(0)
        combobox_p10 = ttk.Combobox(newwindow_p,state='readonly',values=mass_list_p10)
        combobox_p10.place(width=50,height=20,x=810,y=60)
        combobox_p10.current(0)

        textBox_p1 = ttk.Entry(newwindow_p)
        textBox_p1.place(width=50,height=20,x=90,y=100)
        textBox_p2 = ttk.Entry(newwindow_p)
        textBox_p2.place(width=50,height=20,x=170,y=100)
        textBox_p3 = ttk.Entry(newwindow_p)
        textBox_p3.place(width=50,height=20,x=250,y=100)
        textBox_p4 = ttk.Entry(newwindow_p)
        textBox_p4.place(width=50,height=20,x=330,y=100)
        textBox_p5 = ttk.Entry(newwindow_p)
        textBox_p5.place(width=50,height=20,x=410,y=100)
        textBox_p6 = ttk.Entry(newwindow_p)
        textBox_p6.place(width=50,height=20,x=490,y=100)
        textBox_p7 = ttk.Entry(newwindow_p)
        textBox_p7.place(width=50,height=20,x=570,y=100)
        textBox_p8 = ttk.Entry(newwindow_p)
        textBox_p8.place(width=50,height=20,x=650,y=100)
        textBox_p9 = ttk.Entry(newwindow_p)
        textBox_p9.place(width=50,height=20,x=730,y=100)
        textBox_p10 = ttk.Entry(newwindow_p)
        textBox_p10.place(width=50,height=20,x=810,y=100)

    def OKp():
        global ele_p1
        global ele_p2
        global ele_p3
        global ele_p4
        global ele_p5
        global ele_p6
        global ele_p7
        global ele_p8
        global ele_p9
        global ele_p10
        global mass_p1
        global mass_p2
        global mass_p3
        global mass_p4
        global mass_p5
        global mass_p6
        global mass_p7
        global mass_p8
        global mass_p9
        global mass_p10
        global cor_p1
        global cor_p2
        global cor_p3
        global cor_p4
        global cor_p5
        global cor_p6
        global cor_p7
        global cor_p8
        global cor_p9
        global cor_p10

        ele_p1 = ele_list_min_p[0]
        ele_p2 = ele_list_min_p[1]
        ele_p3 = ele_list_min_p[2]
        ele_p4 = ele_list_min_p[3]
        ele_p5 = ele_list_min_p[4]
        ele_p6 = ele_list_min_p[5]
        ele_p7 = ele_list_min_p[6]
        ele_p8 = ele_list_min_p[7]
        ele_p9 = ele_list_min_p[8]
        ele_p10 = ele_list_min_p[9]
        ele_p_list = []
        ele_p_list.append(ele_p1)
        ele_p_list.append(ele_p2)
        ele_p_list.append(ele_p3)
        ele_p_list.append(ele_p4)
        ele_p_list.append(ele_p5)
        ele_p_list.append(ele_p6)
        ele_p_list.append(ele_p7)
        ele_p_list.append(ele_p8)
        ele_p_list.append(ele_p9)
        ele_p_list.append(ele_p10)
        print(ele_p_list)

        mass_p1 = combobox_p1.get()
        mass_p2 = combobox_p2.get()
        mass_p3 = combobox_p3.get()
        mass_p4 = combobox_p4.get()
        mass_p5 = combobox_p5.get()
        mass_p6 = combobox_p6.get()
        mass_p7 = combobox_p7.get()
        mass_p8 = combobox_p8.get()
        mass_p9 = combobox_p9.get()
        mass_p10 = combobox_p10.get()
        mass_p_list =[]
        mass_p_list.append(mass_p1)
        mass_p_list.append(mass_p2)
        mass_p_list.append(mass_p3)
        mass_p_list.append(mass_p4)
        mass_p_list.append(mass_p5)
        mass_p_list.append(mass_p6)
        mass_p_list.append(mass_p7)
        mass_p_list.append(mass_p8)
        mass_p_list.append(mass_p9)
        mass_p_list.append(mass_p10)
        print(mass_p_list)

        cor_p1 = textBox_p1.get()
        cor_p2 = textBox_p2.get()
        cor_p3 = textBox_p3.get()
        cor_p4 = textBox_p4.get()
        cor_p5 = textBox_p5.get()
        cor_p6 = textBox_p6.get()
        cor_p7 = textBox_p7.get()
        cor_p8 = textBox_p8.get()
        cor_p9 = textBox_p9.get()
        cor_p10 = textBox_p10.get()
        cor_p_list=[]
        cor_p_list.append(cor_p1)
        cor_p_list.append(cor_p2)
        cor_p_list.append(cor_p3)
        cor_p_list.append(cor_p4)
        cor_p_list.append(cor_p5)
        cor_p_list.append(cor_p6)
        cor_p_list.append(cor_p7)
        cor_p_list.append(cor_p8)
        cor_p_list.append(cor_p9)
        cor_p_list.append(cor_p10)
        print(cor_p_list)

        if ele_p1 != "-" and cor_p1 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p2 != "-" and cor_p2 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p3 != "-" and cor_p3 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p4 != "-" and cor_p4 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p5 != "-" and cor_p5 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p6 != "-" and cor_p6 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p7 != "-" and cor_p7 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p8 != "-" and cor_p8 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p9 != "-" and cor_p9 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        elif ele_p10 != "-" and cor_p10 == "":
            messagebox.showerror('エラー',"補正項を入力してください")
        else:
            newwindow_p.destroy()

            newwindow_p2 = tk.Toplevel(root)
            newwindow_p2.geometry("1850x980")
            newwindow_p2.title(u"頂点設定")
            newwindow_p2.configure(bg=color8)

            ele_list_p.insert(0,"-")

            frame_p3 = tk.Canvas(newwindow_p2,width=315,height=215,bg=color2)
            frame_p3.place(x=8,y=28)

            frame_p6=tk.Canvas(newwindow_p2,width=71,height=20,bg=color3)
            frame_p6.place(x=16,y=326)
            frame_p7=tk.Canvas(newwindow_p2,width=84,height=20,bg=color4)
            frame_p7.place(x=16,y=406)
            frame_p8=tk.Canvas(newwindow_p2,width=61,height=20,bg=color5)
            frame_p8.place(x=16,y=516)
            frame_p9=tk.Canvas(newwindow_p2,width=84,height=20,bg=color6)
            frame_p9.place(x=16,y=656)

            label_p11 = tk.Label(newwindow_p2,text="A",anchor=tk.CENTER,bg=color2,font=(label_font_jp,10))
            label_p11.place(width=50,height=25,x=12,y=45)
            label_p12 = tk.Label(newwindow_p2,text="B",anchor=tk.CENTER,bg=color2,font=(label_font_jp,10))
            label_p12.place(width=50,height=25,x=12,y=100)
            label_p13 = tk.Label(newwindow_p2,text="C",anchor=tk.CENTER,bg=color2,font=(label_font_jp,10))
            label_p13.place(width=50,height=25,x=12,y=155)

            combobox_p11 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p11.place(width=50,height=25,x=100,y=45)
            combobox_p11.current(0)
            label_p14 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p14.place(width=20,height=25,x=152,y=45)
            combobox_p12 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p12.place(width=50,height=25,x=174,y=45)
            combobox_p12.current(0)
            label_p15 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p15.place(width=20,height=25,x=226,y=45)
            combobox_p13 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p13.place(width=50,height=25,x=248,y=45)
            combobox_p13.current(0)

            combobox_p14 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p14.place(width=50,height=25,x=100,y=100)
            combobox_p14.current(0)
            label_p16 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p16.place(width=20,height=25,x=152,y=100)
            combobox_p15 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p15.place(width=50,height=25,x=174,y=100)
            combobox_p15.current(0)
            label_p17 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p17.place(width=20,height=25,x=226,y=100)
            combobox_p16 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p16.place(width=50,height=25,x=248,y=100)
            combobox_p16.current(0)

            combobox_p17 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p17.place(width=50,height=25,x=100,y=155)
            combobox_p17.current(0)
            label_p18 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p18.place(width=20,height=25,x=152,y=155)
            combobox_p18 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p18.place(width=50,height=25,x=174,y=155)
            combobox_p18.current(0)
            label_p19 = tk.Label(newwindow_p2,text="+",anchor=tk.CENTER,bg=color2,font=(label_font_jp,12))
            label_p19.place(width=20,height=25,x=226,y=155)
            combobox_p19 = ttk.Combobox(newwindow_p2,state='readonly',values=ele_list_min_bar_p)
            combobox_p19.place(width=50,height=25,x=248,y=155)
            combobox_p19.current(0)

            frame_p1=tk.Canvas(newwindow_p2,width=652,height=652,bg=color3)
            frame_p1.place(x=334,y=22)
            frame_p2=tk.Canvas(newwindow_p2,width=610,height=321,bg=color5)
            frame_p2.place(x=996,y=22)
            frame_p4=tk.Canvas(newwindow_p2,width=610,height=321,bg=color6)
            frame_p4.place(x=996,y=353)

            fig_p3 = plt.figure(figsize=(6.42,6.42))
            ax_p3 = fig_p3.add_subplot(111)
            ax_p3.set_aspect('equal', 'datalim')
            plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
            plt.tick_params(bottom=False, left=False, right=False, top=False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            canvas_p3=FigureCanvasTkAgg(fig_p3,master=newwindow_p2)
            canvas_p3.get_tk_widget().place(x=341,y=29)
            canvas_p3._tkcanvas.place(x=341,y=29)

            fig_p5=plt.figure(figsize=(6,3.11))
            fig_p5.subplots_adjust(bottom=0.2)
            ax_p5=fig_p5.add_subplot(111)
            ax_p5.spines['top'].set_color("w")
            ax_p5.spines['bottom'].set_color("w")
            ax_p5.spines['left'].set_color("w")
            ax_p5.spines['right'].set_color("w")
            ax_p5.tick_params(colors="w")
            canvas_p5=FigureCanvasTkAgg(fig_p5,master=newwindow_p2)
            canvas_p5.get_tk_widget().place(x=1003,y=29)
            canvas_p5._tkcanvas.place(x=1003,y=29)

            fig_p6=plt.figure(figsize=(6,3.11))
            fig_p6.subplots_adjust(bottom=0.2)
            ax_p6=fig_p6.add_subplot(111)
            ax_p6.spines['top'].set_color("w")
            ax_p6.spines['bottom'].set_color("w")
            ax_p6.spines['left'].set_color("w")
            ax_p6.spines['right'].set_color("w")
            ax_p6.tick_params(colors="w")
            canvas_p6=FigureCanvasTkAgg(fig_p6,master=newwindow_p2)
            canvas_p6.get_tk_widget().place(x=1003,y=360)
            canvas_p6._tkcanvas.place(x=1003,y=360)

            combobox_p21=ttk.Combobox(newwindow_p2,state='readonly',values=["A","B","C"])
            combobox_p21.place(width=40,height=20,x=110,y=550)
            combobox_p21.current(0)
            combobox_p22=ttk.Combobox(newwindow_p2,state='readonly',values=["A","B","C"])
            combobox_p22.place(width=40,height=20,x=110,y=580)
            combobox_p22.current(0)

            label_p020=tk.Label(newwindow_p2,text="三角グラフ",anchor=tk.W,bg=color3,font=(label_font_jp,10))#,'underline'))
            label_p020.place(width=67,height=16,x=20,y=330)

            label_p021=tk.Label(newwindow_p2,text="三角柱グラフ",anchor=tk.W,bg=color4,font=(label_font_jp,10))#,'underline'))
            label_p021.place(width=80,height=16,x=20,y=410)

            label_p022=tk.Label(newwindow_p2,text="組成分布",anchor=tk.W,bg=color5,font=(label_font_jp,10))#,'underline'))
            label_p022.place(width=57,height=16,x=20,y=520)

            label_p023=tk.Label(newwindow_p2,text="カウント分布",anchor=tk.W,bg=color6,font=(label_font_jp,10))#,'underline'))
            label_p023.place(width=80,height=16,x=20,y=660)


            def click_p2():
                sample_label_long_p = textBox2.get()
                print(sample_label_long_p)
                sample_label_p = sample_label_long_p[:-22]
                print(sample_label_p)

                all_file_p = glob.glob(sample_label_p+"_*_NP_events_large.csv")
                print(all_file_p)
                data_num_p = len(all_file_p)

                sample_p = ["{}_{}_NP_events_large".format(sample_label_p,str(i)) for i in range(1,data_num_p+1)]
                print("sample")
                print(sample_p)
                print(len(sample_p))

                global data_p
                global data_use_p
                global data_use_cor_p
                global data_use_size_p
                global data_chouten_zenbu_p
                global data_choutensize_zenbu_p

                data_p = pd.DataFrame()
                print(data_p)
                for run in range (0,len(sample_p)):
                    datasheet_p = "{}.csv".format(sample_p[run])
                    print("\n{}".format(datasheet_p))
                    try:
                        df_p = pd.read_csv(datasheet_p,low_memory=True)
                        data_p = data_p.append(df_p,ignore_index=True)
                        print(data_p)
                    except FileNotFoundError:
                        messagebox.showerror('エラー','選択されたファイルが正しくありません')
                print("data")
                print(data_p)

                data_zero_p = pd.DataFrame(np.zeros_like(data_p["t_elapsed_Buf"]))

                data_use_p = data_p["'[{}{}]+'".format(mass_p1,ele_p1)]                
                for i in range(1,len(ele_list_min_ini_p)):
                    data_i_p = data_p["'[{}{}]+'".format(mass_p_list[i],ele_p_list[i])]
                    data_use_p = pd.concat([data_use_p,data_i_p],axis=1)
                data_use_p = pd.concat([data_use_p,data_zero_p],axis=1)
                print(data_use_p)


                data_use_cor_p = data_p["'[{}{}]+'".format(mass_p1,ele_p1)]/float(cor_p1)
                for i in range(1,len(ele_list_min_ini_p)):
                    data_i_cor_p = data_p["'[{}{}]+'".format(mass_p_list[i],ele_p_list[i])]/float(cor_p_list[i])
                    data_use_cor_p = pd.concat([data_use_cor_p,data_i_cor_p],axis=1)
                data_use_cor_p = pd.concat([data_use_cor_p,data_zero_p],axis=1)
                print(data_use_cor_p)

                Iso_Compo_list = element_list["Isotopic Composition"]
                list_number_p1 = mass_list_abd_p1.index(mass_abd_p_i)
                index_p1 = iso_list_abd_p1[int(list_number_p1)]
                iso_compo_p1 = Iso_Compo_list[int(index_p1)]
                print("iso_compo_p1")
                print(iso_compo_p1)
                
                data_use_size_p = data_p["'[{}{}]+'".format(mass_p1,ele_p1)]/float(iso_compo_p1)*float(cor_p1)/float(cor_p1)           
                for i in range(1,len(ele_list_min_ini_p)):
                    data_i_size_p = data_p["'[{}{}]+'".format(mass_p_list[i],ele_p_list[i])]/float(iso_compo_p1)*float(cor_p1)/float(cor_p_list[i])
                    data_use_size_p = pd.concat([data_use_size_p,data_i_size_p],axis=1)
                data_use_size_p = pd.concat([data_use_size_p,data_zero_p],axis=1)
                print(data_use_size_p)

                data_use_p.columns = ele_list_min_zero_p
                print(data_use_p)
                data_use_cor_p.columns = ele_list_min_zero_p
                print(data_use_cor_p)
                data_use_size_p.columns = ele_list_min_zero_p
                print(data_use_size_p)

                data_chouten1_p = data_use_cor_p[combobox_p11.get()]+data_use_cor_p[combobox_p12.get()]+data_use_cor_p[combobox_p13.get()]
                #print(data_chouten1_p)
                data_chouten2_p = data_use_cor_p[combobox_p14.get()]+data_use_cor_p[combobox_p15.get()]+data_use_cor_p[combobox_p16.get()]
                #print(data_chouten2_p)
                data_chouten3_p = data_use_cor_p[combobox_p17.get()]+data_use_cor_p[combobox_p18.get()]+data_use_cor_p[combobox_p19.get()]
                #print(data_chouten3_p)
                data_chouten_zenbu_p = pd.concat([data_chouten1_p,data_chouten2_p,data_chouten3_p],axis=1)
                data_chouten_zenbu_p.columns = ["CT1","CT2","CT3"]
                #print(data_chouten_zenbu_p)

                data_choutensize1_p = data_use_size_p[combobox_p11.get()]+data_use_size_p[combobox_p12.get()]+data_use_size_p[combobox_p13.get()]
                #print(data_choutensize1_p)
                data_choutensize2_p = data_use_size_p[combobox_p14.get()]+data_use_size_p[combobox_p15.get()]+data_use_size_p[combobox_p16.get()]
                #print(data_choutensize2_p)
                data_choutensize3_p = data_use_size_p[combobox_p17.get()]+data_use_size_p[combobox_p18.get()]+data_use_size_p[combobox_p19.get()]
                #print(data_choutensize3_p)
                data_choutensize_zenbu_p = pd.concat([data_choutensize1_p,data_choutensize2_p,data_choutensize3_p],axis=1)
                data_choutensize_zenbu_p.columns = ["CT1","CT2","CT3"]
                print(data_choutensize_zenbu_p)

            def click_pC():

                plt.rcParams["font.family"] = graph_font

                SUM = data_chouten_zenbu_p["CT1"]+data_chouten_zenbu_p["CT2"]+data_chouten_zenbu_p["CT3"]
                pX = data_chouten_zenbu_p["CT1"]/SUM*100
                pY = data_chouten_zenbu_p["CT2"]/SUM*100
                pZ = data_chouten_zenbu_p["CT3"]/SUM*100
                data_concat_p = pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat_p.columns = ['X','Y','Z','SUM']

                data_z_SUM_p = data_choutensize_zenbu_p["CT1"]+data_choutensize_zenbu_p["CT2"]+data_choutensize_zenbu_p["CT3"]
                data_z_x_p = data_choutensize_zenbu_p["CT1"] #いらない列
                data_z_p = pd.concat([data_z_SUM_p,data_z_x_p],axis=1)
                data_z_p.columns = ['SUM','X']

                zmax_p = data_z_p['SUM'].max()

                print(data_z_p['SUM'].sort_values())

                amari_p = zmax_p%10

                if amari_p == 0:
                    baisuu_p = zmax_p
                else:
                    baisuu_p = zmax_p-amari_p+10

                if textBox_p11.get() == "":
                    tB_p11 = "0"
                else:
                    tB_p11 = textBox_p11.get()

                if textBox_p12.get() == "":
                    tB_p12 = baisuu_p
                else:
                    tB_p12 = textBox_p12.get()

                if tB_p11 == "0" and tB_p12 == baisuu_p:
                    data_concat_0_tri_p = data_concat_p
                    data_gattai_0_p = data_chouten_zenbu_p
                else:
                    data_concat_0_tri_p = data_concat_p[(data_z_p["SUM"]>=int(tB_p11))&(data_z_p["SUM"]<=int(tB_p12))]
                    data_gattai_0_p = data_chouten_zenbu_p[(data_z_p["SUM"]>=int(tB_p11))&(data_z_p["SUM"]<=int(tB_p12))]

                print(data_chouten_zenbu_p)
                print(data_gattai_0_p)
                print(data_concat_0_tri_p)
                print("index list")
                #print(list(data_concat_0_tri_p.index))
                
                h = np.sqrt(3.0)*0.5

                global data_plot_p3
                plotx_p3 = (100-data_concat_0_tri_p['Y'])/100-data_concat_0_tri_p['X']/200
                ploty_p3 = h*data_concat_0_tri_p['X']/100
                data_plot_p3 = pd.concat([plotx_p3,ploty_p3],axis=1)
                data_plot_p3.columns = ['x3','y3']

                print(data_plot_p3)

                ax_p3.cla()
                fig_p3.set_facecolor(color_fig)
                ax_p3.set_facecolor(color_fig)

                for i in range(1,10):
                    ax_p3.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], linestyle='dashed',color='gray', lw=0.5)
                    ax_p3.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], linestyle='dashed',color='gray', lw=0.5)
                    ax_p3.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], linestyle='dashed',color='gray', lw=0.5)
                
                ax_p3.plot([0.0, 1.0],[0.0, 0.0], color=color_axes, lw=2)
                ax_p3.plot([0.0, 0.5],[0.0, h], color=color_axes, lw=2)
                ax_p3.plot([1.0, 0.5],[0.0, h], color=color_axes, lw=2)   

                #chouten1_text = "{}+{}+{}".format(combobox_p11.get(),combobox_p12.get(),combobox_p13.get())
                #chouten2_text = "{}+{}+{}".format(combobox_p14.get(),combobox_p15.get(),combobox_p16.get())
                #chouten3_text = "{}+{}+{}".format(combobox_p17.get(),combobox_p18.get(),combobox_p19.get())
                chouten1_text = "A"
                chouten2_text = "B"
                chouten3_text = "C"

                ax_p3.text(0.455, h+0.0283, chouten1_text, fontsize=22, color=color_axes, va="center")
                ax_p3.text(-0.1, -0.02, chouten2_text, fontsize=22, color=color_axes, va="center")
                ax_p3.text(1.02, -0.02, chouten3_text, fontsize=22, color=color_axes, va="center")

                for i in range(1,10):
                    ax_p3.text(0.5+(10-i)/20.0+0.016, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize=17, color=color_axes)
                    ax_p3.text((10-i)/20.0-0.082, h*(10-i)/10.0, '%d0' % i, fontsize=17, color=color_axes)
                    ax_p3.text(i/10.0-0.03, -0.06, '%d0' % i, fontsize=17, color=color_axes)

                ax_p3.text(-0.15,1,"Number of particles:"+str(len(data_plot_p3.dropna())),fontsize=14, color=color_axes)

                ax_p3.scatter(data_plot_p3["x3"],data_plot_p3["y3"],c=color_plot,alpha=alpha_plot,s=size_plot)

                canvas_p3.draw()                     

            def click_pA():

                plt.rcParams["font.family"] = graph_font

                SUM = data_chouten_zenbu_p["CT1"]+data_chouten_zenbu_p["CT2"]+data_chouten_zenbu_p["CT3"]
                pX = data_chouten_zenbu_p["CT1"]/SUM*100
                pY = data_chouten_zenbu_p["CT2"]/SUM*100
                pZ = data_chouten_zenbu_p["CT3"]/SUM*100
                data_concat_p = pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat_p.columns = ['X','Y','Z','SUM']

                data_z_SUM_p = data_choutensize_zenbu_p["CT1"]+data_choutensize_zenbu_p["CT2"]+data_choutensize_zenbu_p["CT3"]
                data_z_x_p = data_choutensize_zenbu_p["CT1"] #いらない列
                data_z_p = pd.concat([data_z_SUM_p,data_z_x_p],axis=1)
                data_z_p.columns = ['SUM','X']

                h = np.sqrt(3.0)*0.5

                zmax_p = data_z_p['SUM'].max()

                amari_p = zmax_p%10
                
                if amari_p == 0:
                    baisuu_p = zmax_p
                else:
                    baisuu_p = zmax_p-amari_p+10

                NP1_p = np.linspace(0,baisuu_p,6,dtype=int)

                plotx_p1 = (100-data_concat_p['Y'])/100-data_concat_p['X']/200
                ploty_p1 = h*data_concat_p['X']/100
                plotz_p1 = data_z_p['SUM']/baisuu_p
                data_plot_p1 = pd.concat([plotx_p1,ploty_p1,plotz_p1],axis=1)
                data_plot_p1.columns = ['x1','y1','z1']

                fig_p1 = plt.figure(figsize=(7.5,7.5))
                ax_p1 = fig_p1.add_subplot(111,projection='3d')
                ax_p1.set_xticks([])
                ax_p1.set_yticks([])
                ax_p1.set_zticks([])
                plt.axis('off')
                ax_p1.view_init(elev=12,azim=-69)

                fig_p1.set_facecolor(color_fig)
                ax_p1.set_facecolor(color_fig)

                for i in range(1,5):
                    ax_p1.plot([i*2/20.0, 1.0-i*2/20.0],[h*2*i/10.0, h*i*2/10.0],[0,0],color='gray', lw=0.5)
                    ax_p1.plot([i*2/20.0, i*2/10.0],[h*i*2/10.0, 0.0],[0,0], color='gray', lw=0.5)
                    ax_p1.plot([0.5+i*2/20.0, i*2/10.0],[h*(1.0-i*2/10.0), 0.0],[0,0],color='gray', lw=0.5)

                ax_p1.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
                ax_p1.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax_p1.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax_p1.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
                ax_p1.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
                ax_p1.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
                ax_p1.text(0.5, h+0.15,-0.1, "A", fontsize=20,ha="center", color=color_axes)
                ax_p1.text(-0.15*h, -0.15/2,-0.1, "B", fontsize=20,ha="center", color=color_axes)
                ax_p1.text(1+0.15*h, -0.15/2,-0.1, "C", fontsize=20,ha="center", color=color_axes)

                for i in range(1,5):
                    ax_p1.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
                    ax_p1.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
                    ax_p1.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)
    
                ax_p1.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
                ax_p1.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
                ax_p1.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

                ax_p1.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

                for i in range(0,6):
                   ax_p1.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

                for i in range(0,6):
                   ax_p1.text(-0.078,-0.078,i/5-0.01,NP1_p[i],fontsize=20,ha="right", color=color_axes)

                ax_p1.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？
    
                ax_p1.set_xlim(0,1)
                ax_p1.set_ylim(0,1)
                ax_p1.set_zlim(0,1)

                #プロット
                ax_p1.scatter(data_plot_p1["x1"],data_plot_p1["y1"],data_plot_p1["z1"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

                #範囲指定のところに値が入っていた場合に全体表示のどの範囲にあたるかを示す
                if not textBox_p13.get() == "" or not textBox_p14.get() == "" :
                    if textBox_p13.get()=="":
                       tB_p13="0"
                    else:
                       tB_p13=textBox_p13.get()

                    if textBox_p14.get()=="":
                       tB_p14=baisuu_p
                    else:
                       tB_p14=textBox_p14.get()

                    tB_p13_range = int(tB_p13)/baisuu_p
                    tB_p14_range = int(tB_p14)/baisuu_p   

                    ax_p1.plot([0.0, 1.0],[0.0, 0.0],[tB_p13_range,tB_p13_range], color="red", lw=1.5)
                    ax_p1.plot([0.0, 0.5],[0.0, h],[tB_p13_range,tB_p13_range], color="red", lw=1.5)
                    ax_p1.plot([1.0, 0.5],[0.0, h],[tB_p13_range,tB_p13_range], color="red", lw=1.5)
                    ax_p1.plot([0.0, 0.0],[0.0, 0.0],[tB_p13_range,tB_p14_range], color="red", lw=1.5)
                    ax_p1.plot([1, 1],[0,0],[tB_p13_range,tB_p14_range], color="red", lw=1.5)
                    ax_p1.plot([0.5, 0.5],[h, h],[tB_p13_range,tB_p14_range], color="red", lw=1.5)
                    ax_p1.plot([0.0, 1.0],[0.0, 0.0],[tB_p14_range,tB_p14_range], color="red", lw=1.5)
                    ax_p1.plot([0.0, 0.5],[0.0, h],[tB_p14_range,tB_p14_range], color="red", lw=1.5)
                    ax_p1.plot([1.0, 0.5],[0.0, h],[tB_p14_range,tB_p14_range], color="red", lw=1.5)        

                fig_p1.show()

            def click_pD(): 

                plt.rcParams["font.family"] = graph_font

                SUM = data_chouten_zenbu_p["CT1"]+data_chouten_zenbu_p["CT2"]+data_chouten_zenbu_p["CT3"]
                pX = data_chouten_zenbu_p["CT1"]/SUM*100
                pY = data_chouten_zenbu_p["CT2"]/SUM*100
                pZ = data_chouten_zenbu_p["CT3"]/SUM*100
                data_concat_p = pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat_p.columns = ['X','Y','Z','SUM']

                data_z_SUM_p = data_choutensize_zenbu_p["CT1"]+data_choutensize_zenbu_p["CT2"]+data_choutensize_zenbu_p["CT3"]
                data_z_x_p = data_choutensize_zenbu_p["CT1"] #いらない列
                data_z_p = pd.concat([data_z_SUM_p,data_z_x_p],axis=1)
                data_z_p.columns = ['SUM','X']

                h = np.sqrt(3.0)*0.5
     
                #座標決め
                zmax_p = data_z_p['SUM'].max()

                amari_p = zmax_p%10
                
                if amari_p == 0:
                    baisuu_p = zmax_p
                else:
                    baisuu_p = zmax_p-amari_p+10

                plotx_p4=(100-data_concat_p['Y'])/100-data_concat_p['X']/200
                ploty_p4=h*data_concat_p['X']/100

                if textBox_p13.get()=="":
                   tB_p13="0"
                else:
                   tB_p13=textBox_p13.get()

                if textBox_p14.get()=="":
                   tB_p14=baisuu_p
                else:
                   tB_p14=textBox_p14.get()

                if tB_p13=="0" and tB_p14==baisuu_p:
                   zvalue_p=baisuu_p
                   plotz_p4=data_z_p['SUM']/zvalue_p
                   NP4_p=np.linspace(0,baisuu_p,6,dtype=int)
                else:
                   zvalue_p=int(tB_p14)-int(tB_p13)
                   plotz_p4=(data_z_p['SUM']-int(tB_p13))/zvalue_p
                   NP4_p=np.linspace(int(tB_p13),int(tB_p14),6,dtype=int) #少数になっちゃう可能性ありそうだけどだいじょうぶかな

                data_plot_p4=pd.concat([plotx_p4,ploty_p4,plotz_p4],axis=1)
                data_plot_p4.columns=['x4','y4','z4']
                data_plot_p40=data_plot_p4[(data_plot_p4["z4"]>=0)&(data_plot_p4["z4"]<=1)]

                #プロット場所決め
                fig_p4=plt.figure(figsize=(7.5,7.5))
                ax_p4=fig_p4.add_subplot(111,projection='3d')
                ax_p4.set_xticks([])
                ax_p4.set_yticks([])
                ax_p4.set_zticks([])
                plt.axis('off')
                ax_p4.view_init(elev=12,azim=-69)

                #三角グラフ描き
                fig_p4.set_facecolor(color_fig)
                ax_p4.set_facecolor(color_fig)

                for i in range(1,5):
                    ax_p4.plot([2*i/20.0, 1.0-2*i/20.0],[h*2*i/10.0, h*2*i/10.0],[0,0],color='gray', lw=0.5)
                    ax_p4.plot([2*i/20.0, 2*i/10.0],[h*2*i/10.0, 0.0],[0,0], color='gray', lw=0.5)
                    ax_p4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[0,0], color='gray', lw=0.5)

                ax_p4.plot([0.0, 1.0],[0.0, 0.0],[0,0], color=color_axes, lw=2)
                ax_p4.plot([0.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax_p4.plot([1.0, 0.5],[0.0, h],[0,0], color=color_axes, lw=2)
                ax_p4.plot([0.0, 0.0],[0.0, 0.0],[0,1], color=color_axes, lw=2)
                ax_p4.plot([1, 1],[0,0],[0,1], color=color_axes, lw=2)
                ax_p4.plot([0.5, 0.5],[h, h],[0,1], color=color_axes, lw=2)
                ax_p4.text(0.5, h+0.15,-0.1, "A", fontsize=20,ha="center", color=color_axes)
                ax_p4.text(-0.15*h, -0.15/2,-0.1, "B", fontsize=20,ha="center", color=color_axes)
                ax_p4.text(1+0.15*h, -0.15/2,-0.1, "C", fontsize=20,ha="center", color=color_axes)

                for i in range(1,5):
                    ax_p4.plot([2*i/20.0, 1.0-2*i/20.0],[2*h*i/10.0, 2*h*i/10.0],[1,1],color='gray', lw=0.5)
                    ax_p4.plot([2*i/20.0, 2*i/10.0],[2*h*i/10.0, 0.0],[1,1], color='gray', lw=0.5)
                    ax_p4.plot([0.5+2*i/20.0, 2*i/10.0],[h*(1.0-2*i/10.0), 0.0],[1,1], color='gray', lw=0.5)

                ax_p4.plot([0.0, 1.0],[0.0, 0.0],[1,1], color=color_axes, lw=2)
                ax_p4.plot([0.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)
                ax_p4.plot([1.0, 0.5],[0.0, h],[1,1], color=color_axes, lw=2)

                ax_p4.plot([0,0],[0,0],[0,1], color=color_axes, lw=2)

                for i in range(0,6):
                   ax_p4.plot([0,-0.02],[0,-0.02],[i/5,i/5], color=color_axes, lw=2)

                for i in range(0,6):
                   ax_p4.text(-0.078,-0.078,i/5-0.01,NP4_p[i],fontsize=20,ha="right", color=color_axes)

                ax_p4.text(-0.08,-0.08,1.2,"Counts",ha="right",fontsize=20,color=color_axes) #縦にならなくても入れたほうがいいですか？

                ax_p4.set_xlim(0,1)
                ax_p4.set_ylim(0,1)
                ax_p4.set_zlim(0,1)

                #プロット
                ax_p4.scatter(data_plot_p40["x4"],data_plot_p40["y4"],data_plot_p40["z4"],c=color_plot,alpha=alpha_plot,depthshade=False,s=size_plot)

                fig_p4.show()

            def click_pE():

                plt.rcParams["font.family"] = graph_font

                SUM = data_chouten_zenbu_p["CT1"]+data_chouten_zenbu_p["CT2"]+data_chouten_zenbu_p["CT3"]
                pX = data_chouten_zenbu_p["CT1"]/SUM*100
                pY = data_chouten_zenbu_p["CT2"]/SUM*100
                pZ = data_chouten_zenbu_p["CT3"]/SUM*100
                data_concat_p = pd.concat([pX,pY,pZ,SUM],axis=1)
                data_concat_p.columns = ['X','Y','Z','SUM']

                data_z_SUM_p = data_choutensize_zenbu_p["CT1"]+data_choutensize_zenbu_p["CT2"]+data_choutensize_zenbu_p["CT3"]
                data_z_x_p = data_choutensize_zenbu_p["CT1"] #いらない列
                data_z_p = pd.concat([data_z_SUM_p,data_z_x_p],axis=1)
                data_z_p.columns = ['SUM','X']

                zmax_p = data_z_p['SUM'].max()

                amari_p = zmax_p%10

                if amari_p == 0:
                    baisuu_p = zmax_p
                else:
                    baisuu_p = zmax_p-amari_p+10

                if textBox_p11.get() == "":
                    tB_p11 = "0"
                else:
                    tB_p11 = textBox_p11.get()

                if textBox_p12.get() == "":
                    tB_p12 = baisuu_p
                else:
                    tB_p12 = textBox_p12.get()

                if tB_p11 == "0" and tB_p12 == baisuu_p:
                    data_concat0_p = data_concat_p
                else:
                    data_concat0_p = data_concat_p[(data_z_p["SUM"]>=int(tB_p11))&(data_z_p["SUM"]<=int(tB_p12))]


                if textBox_p15.get()=="":
                    tB_p15="0"
                else:
                    tB_p15=textBox_p15.get()

                if textBox_p16.get()=="":
                    tB_p16="100"
                else:
                    tB_p16=textBox_p16.get()

                if combobox_p21.get()=="A":
                    if tB_p15=="0" and tB_p16=="100":
                        data_concat00_p=data_concat0_p
                    else:
                        data_concat00_p=data_concat0_p[(data_concat0_p['X']>=int(tB_p15))&(data_concat0_p['X']<=int(tB_p16))]

                    if combobox_p22.get()=="B":
                        count_p=data_concat00_p['Y']/(data_concat00_p['Y']+data_concat00_p['Z'])*100
                        perelement_p="B"
                    elif combobox_p22.get()=="C":
                        count_p=data_concat00_p['Z']/(data_concat00_p['Y']+data_concat00_p['Z'])*100
                        perelement_p="C"   
                    elif combobox_p22.get()=="":
                        messagebox.showerror('エラー','割合を見る元素を指定してください') 
                    else:
                        messagebox.showerror('エラー','重複せずに選択してください') 
                elif combobox_p21.get()=="B":        
                    if tB_p15=="0" and tB_p16=="100":
                        data_concat00_p=data_concat0_p
                    else:
                        data_concat00_p=data_concat0_p[(data_concat0_p['Y']>=int(tB_p15))&(data_concat0_p['Y']<=int(tB_p16))]
      
                    if combobox_p22.get()=="C":
                        count_p=data_concat00_p['Z']/(data_concat00_p['Z']+data_concat00_p['X'])*100
                        perelement_p="C"
                    elif combobox_p22.get()=="A":
                        count_p=data_concat00_p['X']/(data_concat00_p['Z']+data_concat00_p['X'])*100
                        perelement_p="A"
                    elif combobox_p22.get()=="":
                        messagebox.showerror('エラー','割合を見る元素を指定してください')       
                    else:
                        messagebox.showerror('エラー','重複せずに選択してください') 
                elif combobox_p21.get()=="C":
                    if tB_p15=="0" and tB_p16=="100":
                        data_concat00_p=data_concat0_p
                    else:
                        data_concat00_p=data_concat0_p[(data_concat0_p['Z']>=int(tB_p15))&(data_concat0_p['Z']<=int(tB_p16))]
      
                    if combobox_p22.get()=="A":
                        count_p=data_concat00_p['X']/(data_concat00_p['X']+data_concat00_p['Y'])*100
                        perelement_p="A"
                    elif combobox_p22.get()=="B":
                        count_p=data_concat00_p['Y']/(data_concat00_p['X']+data_concat00_p['Y'])*100 
                        perelement_p="A"
                    elif combobox_p22.get()=="":
                        messagebox.showerror('error','割合を見る元素を指定してください') 
                    else:
                        messagebox.showerror('error','重複せずに選択してください') 
                elif combobox_p21.get()=="":
                    messagebox.showerror('error','範囲を固定する元素を指定してください')
                #else:
                #   messagebox.showerror('error','元素は'+combobox4_5.get()+"または"+combobox4_6.get()+"または"+combobox4_7.get()+'のいずれかを入力してください')

                data_z_c_p=pd.concat([count_p,data_z_SUM_p],axis=1)
                data_z_c_p.columns=['X','SUM']     
                print(data_z_c_p)
                data_z_0_p = data_z_c_p.dropna(how="any")
                print(data_z_0_p)

                tB_p333=combobox_p20.get()

                times_p=100/int(tB_p333)

                Num4_X_p=[]
                for i in range(0,int(times_p)):
                    Num4_X_p.append(np.count_nonzero((count_p>=i*int(tB_p333))&(count_p<=(i+1)*int(tB_p333))))

                    #上でエラーの表示になるときはここでエラー出るからグラフかく操作もif文の中に入れたほうがいいかな？

                ax_p5.cla()

                plt.rcParams["font.family"] = graph_font

                fig_p5.set_facecolor(color_fig)
                ax_p5.set_facecolor(color_fig)

                ax_p5.spines['top'].set_color(color_axes)
                ax_p5.spines['bottom'].set_color(color_axes)
                ax_p5.spines['left'].set_color(color_axes)
                ax_p5.spines['right'].set_color(color_axes)
                ax_p5.tick_params(colors=color_axes)

                left=np.linspace(0,100-int(tB_p333),int(times_p),dtype=int)
                height=np.array(Num4_X_p)
                if bar_style == "枠あり":   
                    ax_p5.bar(left,height,width=int(tB_p333),color=color_bar,linewidth=1,edgecolor=color_axes,align="edge",zorder=2)
                elif bar_style == "枠なし":
                    ax_p5.bar(left,height,width=int(tB_p333)* 0.8,color=color_bar,align="edge",zorder=2)
                ax_p5.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
                ax_p5.set_xlabel("%"+perelement_p,fontname=graph_font,color=color_axes,weight=weight_font)
                ax_p5.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

                canvas_p5.draw()

            def click_pF():
                plt.rcParams["font.family"] = graph_font
            
                SUM = data_chouten_zenbu_p["CT1"]+data_chouten_zenbu_p["CT2"]+data_chouten_zenbu_p["CT3"]
                pX = data_chouten_zenbu_p["CT1"]/SUM*100
                pY = data_chouten_zenbu_p["CT2"]/SUM*100
                pZ = data_chouten_zenbu_p["CT3"]/SUM*100
                data_concat_p = pd.concat([pX,pY,pZ],axis=1)
                data_concat_p.columns = ['X','Y','Z']

                data_z_SUM_p = data_choutensize_zenbu_p["CT1"]+data_choutensize_zenbu_p["CT2"]+data_choutensize_zenbu_p["CT3"]
                data_z_x_p = data_choutensize_zenbu_p["CT1"] #いらない列
                data_z_p = pd.concat([data_z_SUM_p,data_z_x_p],axis=1)
                data_z_p.columns = ['SUM','x']

                data_concat_z_p=pd.concat([data_concat_p,data_z_p],axis=1)

                if textBox_p17.get()=="":
                    tB_p17="0"
                else:
                    tB_p17=textBox_p17.get()
            
                if textBox_p18.get()=="":
                    tB_p18="100"
                else:
                    tB_p18=textBox_p18.get()

                if textBox_p19.get()=="":
                    tB_p19="0"
                else:
                    tB_p19=textBox_p19.get()
        
                if textBox_p20.get()=="":
                    tB_p20="100"
                else:
                    tB_p20=textBox_p20.get()

                if textBox_p21.get()=="":
                    tB_p21="0"
                else:
                    tB_p21=textBox_p21.get()

                if textBox_p22.get()=="":
                    tB_p22="100"
                else:
                    tB_p22=textBox_p22.get()

                #ここでなぜかエラー　strとintの間に不等号が入っちゃってるらしい　左が違うのか？？？  NaNがあるっぽい！！どこかでdropnaする必要あり　他の関数で起きていないのはなぜ？？
                print(data_concat_z_p)
                data_concat_z_p_drop = data_concat_z_p.dropna(how="any")
                print(type(data_concat_z_p["X"][0]))
                #data_concat0_p=data_concat_z_p[(data_concat_z_p["X"]>=int(tB_p17))&(data_concat_z_p["X"]<=int(tB_p18))&(data_concat_z_p["Y"]>=int(tB_p19))&(data_concat_z_p["Y"]<=int(tB_p20))&(data_concat_z_p["Z"]>=int(tB_p21))&(data_concat_z_p["Z"]<=int(tB_p22))]
                data_concat0_p=data_concat_z_p_drop[(data_concat_z_p_drop["X"]>=int(tB_p17))&(data_concat_z_p_drop["X"]<=int(tB_p18))&(data_concat_z_p_drop["Y"]>=int(tB_p19))&(data_concat_z_p_drop["Y"]<=int(tB_p20))&(data_concat_z_p_drop["Z"]>=int(tB_p21))&(data_concat_z_p_drop["Z"]<=int(tB_p22))]
                print(data_concat0_p)
                zmax0_p = data_concat0_p['SUM'].max()
                print(zmax0_p)
                amari_p=zmax0_p%10
                print(amari_p)
                if amari_p==0:
                   baisuu_p=zmax0_p
                else:
                   baisuu_p=zmax0_p-amari_p+10

                if textBox_p23.get()=="":
                    tB_p23="0"
                else:
                    tB_p23=textBox_p23.get()

                if textBox_p24.get()=="":
                    tB_p24=baisuu_p
                else:
                    tB_p24=textBox_p24.get()
            
                if textBox_p25.get()=="":
                    tB_p25=5
                else:
                    tB_p25=textBox_p25.get()


                if len(data_concat0_p)==0:
                    if int(tB_p21)<100-(int(tB_p18)+int(tB_p20)) or int(tB_p22)>100-(int(tB_p17)+int(tB_p19)):
                        messagebox.showerror('エラー','範囲が間違っています')
                    else:
                        messagebox.showerror('エラー','範囲内にデータがありません')
                else:
                    pltmin_p=int(tB_p23)
                    amari0_p=int(tB_p24)%10
                    if amari0_p==0:
                        pltmax_p=int(tB_p24)
                    else:
                        pltmax_p=int(tB_p24)-amari0_p+10

                    ax_p6.cla()

                    fig_p6.set_facecolor(color_fig)
                    ax_p6.set_facecolor(color_fig)

                    ax_p6.spines['top'].set_color(color_axes)
                    ax_p6.spines['bottom'].set_color(color_axes)
                    ax_p6.spines['left'].set_color(color_axes)
                    ax_p6.spines['right'].set_color(color_axes)
                    ax_p6.tick_params(colors=color_axes)
    
                    if bar_style == "枠あり":
                        ax_p6.hist(data_concat0_p["SUM"],bins=np.arange(pltmin_p,pltmax_p+int(tB_p25),int(tB_p25)),color=color_bar,linewidth=1,edgecolor=color_axes,zorder=2)
                    elif bar_style == "枠なし":
                        ax_p6.hist(data_concat0_p["SUM"],bins=np.arange(pltmin_p,pltmax_p+int(tB_p25),int(tB_p25)),width = int(tB_p25) * 0.8,color=color_bar,zorder=2)
                    ax_p6.grid(b=True,which='major',axis='y',color=color_axes,linewidth=0.5,zorder=1)
                    ax_p6.set_xlabel("Counts",fontname=graph_font,color=color_axes,weight=weight_font)
                    ax_p6.set_ylabel("Number of particles",fontname=graph_font,color=color_axes,weight=weight_font)

                    canvas_p6.draw()

            btn_p3 = tk.Button(newwindow_p2,text="読み込み",command=click_p2,font=(label_font_jp,8))
            btn_p3.place(width=160,height=25,x=100,y=200)
            btn_p4 = tk.Button(newwindow_p2,text="表示",command=click_pC,font=(label_font_jp,8))
            btn_p4.place(width=50,height=25,x=215,y=359)
            btn_p5 = tk.Button(newwindow_p2,text="全体表示",command=click_pA,font=(label_font_jp,9))
            btn_p5.place(width=90,height=25,x=60,y=440)
            btn_p6=tk.Button(newwindow_p2,text="表示",command=click_pD,font=(label_font_jp,9))
            btn_p6.place(width=50,height=25,x=215,y=469)
            btn_p7=tk.Button(newwindow_p2,text="表示",command=click_pE,font=(label_font_jp,9))
            btn_p7.place(width=50,height=25,x=215,y=609)
            btn_p8=tk.Button(newwindow_p2,text="表示",command=click_pF,font=(label_font_jp,9))
            btn_p8.place(width=50,height=25,x=215,y=809)

            textBox_p11 = tk.Entry(newwindow_p2)
            textBox_p11.place(width=40,height=20,x=110,y=360)
            textBox_p12 = tk.Entry(newwindow_p2)
            textBox_p12.place(width=40,height=20,x=160,y=360)
            label_p23=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font,10))
            label_p23.place(width=10,height=20,x=150,y=360)
            label_p24=tk.Label(newwindow_p2,text="カウント",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p24.place(width=50,height=20,x=60,y=360)       

            textBox_p13=tk.Entry(newwindow_p2)
            textBox_p13.place(width=40,height=20,x=110,y=470)
            textBox_p14=tk.Entry(newwindow_p2)
            textBox_p14.place(width=40,height=20,x=160,y=470)
            label_p25=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font,10))
            label_p25.place(width=10,height=20,x=150,y=470)
            label_p26=tk.Label(newwindow_p2,text="カウント",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p26.place(width=50,height=20,x=60,y=470)      

            textBox_p15=tk.Entry(newwindow_p2)
            textBox_p15.place(width=40,height=20,x=156,y=550)
            textBox_p16=tk.Entry(newwindow_p2)
            textBox_p16.place(width=40,height=20,x=205,y=550)
            combobox_p20=ttk.Combobox(newwindow_p2,state='readonly',values=[1,2,4,5,10,20,25,50,100])
            combobox_p20.current(4)      
            combobox_p20.place(width=40,height=20,x=110,y=610)
            label_p27=tk.Label(newwindow_p2,text=":",bg=color8,font=(label_font_jp,10))
            label_p27.place(width=3,height=20,x=151,y=550)
            label_p28=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font_jp,10))
            label_p28.place(width=10,height=20,x=195,y=550)
            label_p29=tk.Label(newwindow_p2,text="%",bg=color8,font=(label_font_jp,9))
            label_p29.place(width=20,height=20,x=248,y=550) 
            label_p30=tk.Label(newwindow_p2,text="固定",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p30.place(width=50,height=20,x=60,y=550) 
            label_p31=tk.Label(newwindow_p2,text="表示",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p31.place(width=50,height=20,x=60,y=580) 
            label_p32=tk.Label(newwindow_p2,text="幅",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p32.place(width=50,height=20,x=60,y=610) 

            textBox_p17=tk.Entry(newwindow_p2)
            textBox_p17.place(width=40,height=20,x=110,y=690)
            textBox_p18=tk.Entry(newwindow_p2)
            textBox_p18.place(width=40,height=20,x=160,y=690)
            textBox_p19=tk.Entry(newwindow_p2)
            textBox_p19.place(width=40,height=20,x=110,y=720)
            textBox_p20=tk.Entry(newwindow_p2)
            textBox_p20.place(width=40,height=20,x=160,y=720)
            textBox_p21=tk.Entry(newwindow_p2)
            textBox_p21.place(width=40,height=20,x=110,y=750)
            textBox_p22=tk.Entry(newwindow_p2)
            textBox_p22.place(width=40,height=20,x=160,y=750)
            label_p33=tk.Label(newwindow_p2,text="A"+":",bg=color8,font=(label_font_jp,10))
            label_p33.place(width=20,height=20,x=80,y=690)
            label_p34=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font_jp,10))
            label_p34.place(width=10,height=20,x=150,y=690)
            label_p35=tk.Label(newwindow_p2,text="%",bg=color8,font=(label_font_jp,9))
            label_p35.place(width=20,height=20,x=203,y=690)
            label_p36=tk.Label(newwindow_p2,text="B"+":",bg=color8,font=(label_font_jp,10))
            label_p36.place(width=20,height=20,x=80,y=720)
            label_p37=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font_jp,10))
            label_p37.place(width=10,height=20,x=150,y=720)
            label_p38=tk.Label(newwindow_p2,text="%",bg=color8,font=(label_font_jp,9))
            label_p38.place(width=20,height=20,x=203,y=720)
            label_p39=tk.Label(newwindow_p2,text="C"+":",bg=color8,font=(label_font_jp,10))
            label_p39.place(width=20,height=20,x=80,y=750)
            label_p40=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font_jp,10))
            label_p40.place(width=10,height=20,x=150,y=750)
            label_p41=tk.Label(newwindow_p2,text="%",bg=color8,font=(label_font_jp,9))
            label_p41.place(width=20,height=20,x=203,y=750)
            textBox_p23=tk.Entry(newwindow_p2)
            textBox_p23.place(width=40,height=20,x=110,y=780)
            textBox_p24=tk.Entry(newwindow_p2)
            textBox_p24.place(width=40,height=20,x=160,y=780)      
            label_p42=tk.Label(newwindow_p2,text="-",bg=color8,font=(label_font,10))
            label_p42.place(width=10,height=20,x=150,y=780)
            label_p43=tk.Label(newwindow_p2,text="カウント",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p43.place(width=50,height=20,x=60,y=780) 
            textBox_p25=tk.Entry(newwindow_p2)
            textBox_p25.place(width=40,height=20,x=110,y=810) 
            label_p44=tk.Label(newwindow_p2,text="幅",anchor=tk.CENTER,bg=color8,font=(label_font_jp,9))
            label_p44.place(width=50,height=20,x=60,y=810) 

    def Cancelp():
        newwindow_p.destroy()

    btn_p1=tk.Button(newwindow_p,text="決定",command=OKp)
    btn_p1.place(width=80,height=25,x=680,y=150)
    btn_p2=tk.Button(newwindow_p,text="キャンセル",command=Cancelp)
    btn_p2.place(width=80,height=25,x=780,y=150)

menubar = tk.Menu(root)
root.config(menu = menubar)

save_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'ファイル', menu = save_menu)

savefig_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'グラフ保存', menu = savefig_menu)

tool_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'ツール', menu = tool_menu)

setting_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '設定', menu = setting_menu)

savefig_menu.add_command(label = '三角グラフ',command = savefig3)
savefig_menu.add_command(label = '組成分布',command = savefig5)
savefig_menu.add_command(label = 'カウント分布',command = savefig6)
save_menu.add_command(label = '名前を付けて保存',command = savelist)
save_menu.add_command(label = '開く',command = openlist)
save_menu.add_separator()
save_menu.add_command(label = '終了',command = end)
setting_menu.add_command(label = 'レイアウト設定',command = layout)
setting_menu.add_command(label = '参照値',command = sansyou)
tool_menu.add_command(label = "範囲指定",command = hannisitei)
tool_menu.add_command(label = "頂点設定",command = choutenplus)

root.mainloop()