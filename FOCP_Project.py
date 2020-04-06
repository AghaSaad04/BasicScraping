from tkinter import *
import urllib.request
import re
import os
import requests
import lxml.html
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

#Function creating directory and subdirectory
def create_directory(directory,subdirectory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if not os.path.exists(directory+"/"+subdirectory):
        os.makedirs(directory+"/"+subdirectory)
#function for checking the URL
def check_url(url):

    if "." not in url:
        label_error.config(text="invalid URL!")
        return False
    try:
        URLValidator()('http://'+url)
        label_error.config(text="")
        return True
    except:
        label_error.config(text="invalid URL!")
        return False
def fetching(url):
    if check_url(url) == True:
        try:
            dom = lxml.html.fromstring(requests.get("http://"+url).content)
            list=[x for x in dom.xpath('//img/@src')]
            z=len(list)
            label_error.config(text="")
            if z==0:
                label_error.config(text="No Images Found!")
            else:
                y=0
#putting the subdirectory images here
                create_directory(url,"images")
                window=Toplevel()
                #window.geometry("500x500")
                #window.resize(width=False,height=Fals)
                #label2=Label(window)
                #label2.pack()
#Text() creates the textarea in which the final result is shown
                T = Text(window, height=30, width=100)
                S = Scrollbar(window)
                S.pack(side=RIGHT, fill=Y)
                T.pack(side=LEFT, fill=Y)

                S.config(command=T.yview)
                T.config(yscrollcommand=S.set)
#inserting text in the textarea
                T.insert(END,"Fetched Images URL\n")
                #label2.config(text=download)
                while y<z:
                    if list[y][:2]=="//":
                        list[y]="http:"+list[y]
                    T.insert(END,"\n"+"Image "+str(y+1)+": "+list[y])
                    try:
                        resource = urllib.request.urlopen(list[y])
                        output=open(url+"\images\image"+str(y+1)+".jpg","wb")
                        output.write(resource.read())
                        output.close()
                        y=int(y)
                        y+=1
                    except:
                        label_error.config(text="Check your internet connection and try again..")
                label_error.config(text=""+str(z)+" Images Downloaded..")
                T.insert(END,"\n\n"+str(z)+" Images Downloaded..")
        except:
            label_error.config(text="invalid URL!")
def cleanhtml(raw_html):
    try:
        cleanr = re.compile('<head>.*?</head>', re.DOTALL)
        cleantext = re.sub(cleanr, '', raw_html)
        cleanr = re.compile('<script>.*?</script>', re.DOTALL)
        cleantext = re.sub(cleanr, '', cleantext)
        cleanr = re.compile('<!--.*?-->', re.DOTALL)
        cleantext = re.sub(cleanr, '', cleantext)
        cleanr = re.compile('<.*?>', re.DOTALL)
        cleantext = re.sub(cleanr, '', cleantext)
        cleantext = cleantext.replace('  ',' ')
        cleantext = cleantext.strip()
        new.set(cleantext)
        window=Toplevel()
        
        T = Text(window, height=30, width=100)
        S = Scrollbar(window)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(END,cleantext)
    except:
        label_error.config(text="Check your internet connection and try again..")
                
    return cleantext
            
main_window=Tk()
main_window.geometry("300x300")
main_window.title("Web_Scraper 1.O")

try:
    bm=PhotoImage(file="appbg2.gif")
    label_img=Label(main_window,image=bm)
    label_img.pack()
    label_img.place(x=0,y=0,anchor=NW)
except:
    print("Background Image Not Found!")
entry1 = Entry(main_window)
entry1.place(x=115,y=106)
label_url=Label(text="Enter URL:")
label_url.place(x=45,y=106)
label_hint=Label(text="ex: www.example.com")
label_hint.place(x=110,y=126)
label_error=Label(text="")
label_error.place(x=100,y=60)
def file(url):
    myurl = urllib.request.urlopen("http://"+url)
    global html
    html=myurl.read().decode("ascii","ignore")
def pec():
    url=entry1.get()
    if check_url(url) == True:

        try:
            file(url)
            cleanhtml(html)
            file2(url)
        except:
            label_error.config(text="invalid URL!")
def file2(url):
    create_directory(url,"text")
    file = open(url+"/text/"+url+'.html', 'w')
    file.write(html)
    file.close()
    file = open(url+"/text/"+url+'.txt', 'w')
    file.write(new.get())
    file.close()
def images():
    url=entry1.get()
    fetching(url)
    
def finish():
    main_window.destroy()
    
button1 = Button(main_window, text="Text", command=pec)
button1.place(x=80,y=165)
new=StringVar()
button2 = Button(main_window, text="Download images", command=images)
button2.place(x=120,y=165)

button3 = Button(main_window,text="Quit",command=finish)
button3.place(x=130,y=230)
