# ---Music Player Project---

# Add Libraries

from tkinter import *
import os.path
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('Hossein Music Player')
root.geometry("500x350")
root.resizable(False, False)

pygame.mixer.init()


# grab song length info
def play_time():

    # check for double timing slider after couple of stops
    if stopped:
        return

    # grab currents song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    # throw up temporary label to get data
    # slider_label.config(text=f'Slider : {int(my_slider.get())}  and Song pos: {int(current_time)}')

    # convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # get currently playing song
    # current_song = song_box.curselection()

    # grab song name
    song = song_box.get(ACTIVE)
    # load song with mutagen
    song_mut = MP3(song)

    # get song lenght
    global song_length
    song_length = song_mut.info.length

    # convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # increase current time by 1 second
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed:  {converted_song_length}  of  {converted_song_length}   ')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        # slider hasn't been moved

        # Update slider to position
        slider_position = int(song_length)

        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # slide has been moved

        # Update slider to position
        slider_position = int(song_length)

        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # output time to status bar
        status_bar.config(text=f'Time Elapsed:  {converted_current_time}  of  {converted_song_length}   ')

        # moving this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # output time to status bar
    # status_bar.config(text=f'Time Elapsed:  {converted_current_time}  of  {converted_song_length}   ')

    # update slider value to current song position
    # my_slider.config(value=int(current_time))

    # updating the function
    status_bar.after(1000,play_time)


# add song function
def add_song():
    song = filedialog.askopenfilename(title = "Choose A Song" , filetypes = (("MP3 Files" , "*.mp3") , ))

    song_box.insert(END, song)


# add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(title="Choose A Song", filetypes=(("MP3 Files", "*.mp3"),))
    for song in songs:
        song_box.insert(END, song)


# play song function
def play():

    # set stop variable to false so play_time() could call it
    global stopped
    stopped=False

    status_bar.config(text='')

    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # calling the play_time function to get the length of the music
    play_time()

    # Update slider to position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position , value=0)

# stop song function
global stopped
stopped=False


def stop():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # stop song from playing
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

    # clear status bar
    status_bar.config(text='')

    # set stop variable to true
    global stopped
    stopped=True

# next song function


def next_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # get the current song number
    next_one = song_box.curselection()

    # add one to the current song
    next_one = next_one[0]+1
    # grab song name
    song = song_box.get(next_one)

    # load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move active bar in playlist
    song_box.select_clear(0,END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

# previous song function


def previous_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # get the current song number
    next_one = song_box.curselection()

    # add one to the current song
    next_one = next_one[0] - 1
    # grab song name
    song = song_box.get(next_one)

    # load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move active bar in playlist
    song_box.select_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


# create global pause variable
global paused
paused = False


# pause button function
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True

# create slider function


def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)} ')

    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume=pygame.mixer.music.get_volume()


# delete a song function
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# delete all songs function
def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()


# create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)


# Create Playlist box
song_box=Listbox(master_frame, bg="black", fg="green", width=60 , selectbackground="gray" , selectforeground="black")
song_box.grid(row=0, column=0)


# create player control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0,pady=20)

# create volume slider frame
volume_frame = LabelFrame(master_frame, text="میزان صدا")
volume_frame.grid(row=0, column=1, padx=20)


# create player control buttons

backward_button = Button(controls_frame, text="قبلی", command= previous_song)
forward_button = Button(controls_frame, text="بعدی", command = next_song)
play_button = Button(controls_frame,text="پخش", command=play)
pause_button = Button(controls_frame, text="مکث", command=lambda : pause(paused))
stop_button = Button(controls_frame, text="توقف", command=stop)

backward_button.grid(row=0 , column=0 , padx=5)
forward_button.grid(row=0 , column=1 , padx=5)
play_button.grid(row=0 , column=2 , padx=5)
pause_button.grid(row=0 , column=3 , padx=5)
stop_button.grid(row=0 , column=4 , padx=5)

# create manu
my_menu = Menu(root)
root.config(menu=my_menu)

# add add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="اضافه کردن" , menu=add_song_menu)
add_song_menu.add_command(label="اضافه کردن تک آهنگ" , command = add_song )
# add many songs to list
add_song_menu.add_command(label="اضافه کردن چند آهنگ" , command = add_many_songs )

# create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="حذف کردن" , menu=remove_song_menu)
remove_song_menu.add_command(label="حذف کردن تک آهنگ" , command = delete_song)
remove_song_menu.add_command(label="حذف کردن چند آهنگ" , command = delete_all_songs)

# create status bar
status_bar = Label(root, text='', bd=1 , relief=GROOVE , anchor=E)
status_bar.pack(fill=X, side=BOTTOM , ipady=2)

# create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)


# Create volume slider

volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)


# create temporary slide label
# slider_label = Label(root, text="0" )
# slider_label.pack(pady=10)


root.mainloop()
