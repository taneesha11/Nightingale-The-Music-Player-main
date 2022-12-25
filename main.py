from tkinter import * #Tkinter is the standard GUI library for Python
#Python when combined with Tkinter provides a fast and easy way to create GUI applications.
from tkinter import messagebox #MessageBox Widget is used to display the message boxes in the python applications
from tkinter import filedialog #filedialog module provides classes and factory functions for creating file/directory selection windows
#pygame is a Python wrapper for the SDL library, which stands for Simple DirectMedia Layer.
# SDL provides cross-platform access to your system's underlying multimedia hardware components, such as sound, video, mouse, keyboard, and joystick.
from pygame import mixer #mixer pygame module for loading and playing sounds
import os
import time #This function is used to pause the running of the program for few seconds. it takes time in milliseconds as parameter.
import threading #Threading in python is used to run multiple threads (tasks, function calls) at the same time.
from mutagen.mp3 import MP3 #Mutagen is a Python module to handle audio metadata.
from tkinter import ttk
import ttkthemes

#ttk stands for themed widgets and is used for making labels and buttons look better

def music_length(song_to_be_played):
    #os.path.splitext() can be used to extract extensions from filename
    file_data=os.path.splitext(song_to_be_played)
    if file_data[1]=='.mp3':
        audio=MP3(song_to_be_played)
        total_length=audio.info.length
    else:
        a=mixer.Sound(song_to_be_played)
        total_length=a.get_length() #total_length variable value is in seconds
    mins, secs=divmod(total_length, 60) #takes two numbers as arguments and returns a pair of numbers consisting of quotient and remainder.
    mins=round(mins) #roundoffs the number.
    secs=round(secs)
    time='{:02d}:{:02d}'.format(mins, secs) #this is called format string.values will be inserted in the placeholders{}
    lengthlabel['text'] = "Total Length" + ' - ' + time
    thread1=threading.Thread(target=current_length,args=(total_length,))
    thread1.start()
    #this thread will be destroyed once the function linked with the thread is executed(ie when stop func is pressed
    #or song is played upto end)

# problem 1:
#Here Threading is necessary because when current_length funct will be called our program will run while loop for
#time= total_length of music and during that particular time we won't be able to use other widgets/features. hence,
#multitasking is needed and thus, we use Threading .

def current_length(temp):
    while(temp and mixer.music.get_busy()):
        #mixer.music.get_busy() returns false when music is stopped
        global paused
        if paused:
            continue
        else:
            mins, secs=divmod(temp, 60)
            mins=round(mins)
            secs=round(secs)
            time_='{:02d}:{:02d}'.format(mins, secs) #this is called format string
            currenttimelabel['text'] = "Current Length" + ' - ' + time_
            time.sleep(1)
            temp-=1


paused=False
def play_btn():
    global paused
    if paused:   #if pause is true that means the app is paused and we just need to unpause
        mixer.music.unpause()
        statusbar['text'] = "Music is Resumed"
        paused = FALSE
    else:
        try:
            stop_btn()
            time.sleep(1) #used to add delay in execution of program


            #problem 2:
            #the above two steps are important for currenttimelabel to behave accurately bcz when one music is playing
            #and we select and play some other music from the playlist without stopping the current song then when
            #play_btn  func is called , instead of quitting the ongoing thread an additional thread will be created
            #and unexpected behaviour will be observed

            #curselection() func return a tuple containing pos of selected list item
            selected_song=lb.curselection()
            selected_song=int(selected_song[0])
            song_to_be_played=playlist[selected_song]
            mixer.music.load(song_to_be_played) #selected song will get loaded and played
            mixer.music.play()
            #changing the status of statusbar
            statusbar['text']='music is playing'+'-'+os.path.basename(song_to_be_played)
            music_length(song_to_be_played)

        except:
            messagebox.showerror('File not found', 'File not found')  #try and except are used to handle exception so tht our progran dont fail in some error case

def stop_btn():
    mixer.music.stop()
    #changing the status of statusbar
    statusbar['text']='music is stopped'

def pause_btn():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text']="music is paused"

def set_vol(val):
    #in tkinter whenever a function is called using widget then the value is stored in a variable val
    #so when u slide the scale widget the value will be stored in val variable
    volume=float(val)/100
    #this step is imp bcz only accepts value between 0 and 1
    mixer.music.set_volume(volume)

def about_us():
    messagebox.showinfo('Nightingale','Developer - Taneesha Gaur')

#Playlist contains the list of path of songs that are added in the list box
playlist=[] #emptty list

def open_file():
    global filename
    filename=filedialog.askopenfilename() #you may not require to specify the path of any file but you can directly open a file and read it’s content.
    add_song_to_playlist()

def add_song_to_playlist():
    index=0
    lb.insert(index,os.path.basename(filename))
    playlist.insert(index,filename)
    index+=1

muted=False
def mute_btn():
    global muted
    if muted: #already muted then play
        volbtn.config(image=volphoto)
        mixer.music.set_volume(0.60)
        scale.set(60)
        muted=False
        statusbar['text']='volume is unmuted'
    else:  #if not muted, mute.
        volbtn.config(image=mutephoto)
        mixer.music.set_volume(0) #set volume to 0'
        scale.set(0) #set sluder scale to 0
        muted=True
        statusbar['text']='volume is muted'

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): #The askokcancel() function shows a confirmation dialog that has two buttons: OK(true) and Cancel(false).
        stop_btn() #if ok pressed.
        root.destroy() #it destroys a widget

def del_song():
    selected_song=lb.curselection()
    selected_song=int(selected_song[0])
    lb.delete(selected_song)
    playlist.pop(selected_song)

def exit(): #option in file menu
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = ttkthemes.themed_tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

#setting size of root window
#root.geometry('500x500')
#setting title of the root window
root.title("Nightingale-The Music Player")

#used to add display boxes to add text and image
text = ttk.Label(root, text='welcome to the best music player of the century',relief=SUNKEN)
text.pack(fill=X,pady=10,padx=10) # packs widgets relative to the earlier widget

frame=Frame(root) #frames act like a containers to other widgets
frame.pack()

leftframe=Frame(frame)
leftframe.pack(side=LEFT)

rightframe=Frame(frame)
rightframe.pack(side=LEFT)

topframe=Frame(rightframe)
topframe.pack()

lb=Listbox(leftframe)
lb.pack(padx=10,pady=10)

addbtn=ttk.Button(leftframe,text='+add',command=open_file) #adds files to lsitboxx
addbtn.pack(side=LEFT,padx=20)

delbtn=ttk.Button(leftframe,text='-del',command=del_song) #remoe files fron listbox
delbtn.pack()

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu
subMenu = Menu(menubar, tearoff=0) #tearoff is used to remove dashhed lines from menubar
menubar.add_cascade(label="File", menu=subMenu) #adding a submenu to the menubar
subMenu.add_command(label="Open",command=open_file) #adding commands to the submenu #it will also add a file like add btn.
subMenu.add_command(label="Exit",command=exit) #it will close the program using askokcancel

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu) #another submenu in menubar
subMenu.add_command(label="About Us",command= about_us) #clicking this will open a messagebox

#initializing the mixer, this module contains classes for loading sound objects
mixer.init()

#creating label to display total length of the music
#label is used to implement display boxes where we can place text that can be changed by the developer
lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack()

#creating label to display current remaing time
currenttimelabel = ttk.Label(topframe, text='current time : --:--')
currenttimelabel.pack(pady=10)

buttonframe=Frame(rightframe,relief=RAISED,borderwidth=1) #this frame contains play,pause&stop button
buttonframe.pack(padx=10)

#play button
#creating image variable to include image in button
style = ttk.Style() #creating style object

# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).
style.configure('W.TButton', font =
               ('calibri', 10, 'bold'),
                background = 'red',foreground = 'red')  #style is used to render the button

playbtn=ttk.Button(buttonframe,text ="Play",command=play_btn,style = 'W.TButton')
playbtn.grid(row=0,column=0)

#stop button
# photo2=PhotoImage(file='./stop.png')
stopbtn=ttk.Button(buttonframe,text ="Stop",command=stop_btn,style = 'W.TButton')
stopbtn.grid(row=0,column=1) #The Grid geometry manager puts the widgets in a 2-dimensional table. The master widget is split into a number of rows and columns, and each “cell” in the resulting table can hold a widget.

#pause button
# photo3=PhotoImage(file='./pause.png')
pausebtn=ttk.Button(buttonframe,text ="Pause",command=pause_btn,style = 'W.TButton')
pausebtn.grid(row=0,column=2)

bottomframe=Frame(rightframe) #this frame contain rewind,vol and scale
bottomframe.pack(padx=10) #The Pack geometry manager packs widgets relative to the earlier widget.

#rewind button
# photo4=PhotoImage(file='./rewind.png')
rewindbtn=ttk.Button(bottomframe,text ="Rewind",command=play_btn,style = 'W.TButton') #it will play the selected song
rewindbtn.grid(row=0,column=0)

# mutephoto=PhotoImage(file='./mute.png')
# volphoto=PhotoImage(file='./vol.png')
volbtn=ttk.Button(bottomframe,text ="volume/mute",command=mute_btn,style = 'W.TButton') #this buttun will mute and unmute the song
volbtn.grid(row=0,column=1)

scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol) #it is used to provide graphical slider
#this will show default value of scale to 100
scale.set(60) #default value
#this will set default value to 100
mixer.music.set_volume(100)
scale.grid(row=0,column=2)

statusbar=ttk.Label(root,text='nightingale version 1.0 is running!!',relief=SUNKEN)#The Label is used to specify the container box where we can place the text or images
#RELIEF option is used to specify appearance of a decorative border around the label. The default value for this option is FLAT
statusbar.pack(side=BOTTOM, fill=X,pady=10,padx=10) #bottom is used so as to to make statusbar appear at bottom of root window
#fill paramter is used for spanning of statusbar .x means spanning along x axis

root.protocol("WM_DELETE_WINDOW", on_closing) #this will help to close the window using X button.
root.mainloop() #lets Tkinter to start running the application