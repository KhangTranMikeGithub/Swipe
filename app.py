import tkinter as tk
import cv2
from tkinter import *
from tkinter import filedialog as fd
from tkinter import font
import os
from PIL import Image, ImageTk
from miner import PDFMiner

class PDFViewer:
    def __init__(self, master):
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None    
        self.master = master
        self.master.title('Swipe')
        self.master.geometry('1200x600')
        self.master.configure(background='white')
        self.master.iconbitmap(self.master, 'public/logo.ico')
        self.fullYet = False
        self.buttOn = True

        self.borderTopFrame = tk.Frame(self.master, height=1, bg='#eb2a29')
        self.borderTopFrame.pack(fill='both', side=tk.TOP)
        self.topFrame = tk.Frame(self.master, bg='#FFFFFF', bd=0, highlightthickness=0)
        self.logo = PhotoImage(file='public/logo.png')
        self.logoSwipe = tk.Label(self.topFrame, image=self.logo, bd=0, highlightthickness=0)
        self.logoSwipe.pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=20)
        self.buttOnToggle = tk.Button(self.topFrame, text='Toggle webcam', font='Inter 11 bold', padx=7, pady=7, fg='#FFFFFF', bg='#eb2a29', activebackground='#f04343', bd=0, command=self.toggle)
        self.buttOnToggle.pack(side=tk.RIGHT, anchor=tk.NE, padx=20, pady=30)
        self.borderBottomFrame = tk.Frame(self.master, height=1, bg='#eb2a29')

        self.buttonFrame = tk.Frame(self.master, bg='#FFFFFF')
        self.buttonFrameNonFill = tk.Frame(self.buttonFrame, bg='#FFFFFF', width=200)
        self.buttonContainer = tk.Frame(self.buttonFrameNonFill, bg='#FFFFFF')
        self.buttonContainer2 = tk.Frame(self.buttonFrameNonFill, bg='#FFFFFF')
        self.shareI = PhotoImage(file='public/share.png')
        self.uploadI = PhotoImage(file='public/upload.png')
        self.offline = PhotoImage(file='public/firefox_cIp4VO5bPv.png')
        self.shareScreenButton = tk.Button(self.buttonContainer, image=self.shareI, bg='#FFFFFF', activebackground='#444444', bd=0, command=self.full_screen)
        self.uploadSlideButton = tk.Button(self.buttonContainer2, image=self.uploadI, bg='#FFFFFF', activebackground='#444444', bd=0, command=self.open_file)
        # self.labelFrame = tk.Frame(self.master, height=60, bg='#FFFFFF')
        # self.labelContainer = tk.Frame(self.labelFrame, bg='#eb2a29')
        self.share = tk.Label(self.buttonContainer, text='Share Screen', bg='#FFFFFF', font='Inter 11 bold',fg='#1d1d1d')
        self.upload = tk.Label(self.buttonContainer2, text='Upload File', bg='#FFFFFF', font='Inter 11 bold', fg='#1d1d1d')
        self.displayFrame = tk.Frame(self.master, height=500, bg='#FFFFFF')
        self.displayContainer = tk.Frame(self.displayFrame, bg='#FFFFFF')
        self.fileUpload = Canvas(self.displayContainer, width=500, height=282, highlightthickness=0)
        self.fileUpload.create_image(0, 0, anchor='nw', image=self.offline)
        self.screenShare = Canvas(self.displayContainer, width=500, height=282, highlightthickness=0)
        self.topFrame.pack(side=tk.TOP, fill='both')
        self.borderBottomFrame.pack(fill='both')
        self.buttonFrame.pack(fill='both')
        self.buttonFrameNonFill.pack(pady=35)
        self.buttonContainer.pack(side=tk.LEFT)
        self.buttonContainer2.pack(side=tk.RIGHT)
        self.shareScreenButton.pack(side=tk.TOP, padx=245)
        self.uploadSlideButton.pack(side=tk.TOP, padx=245)
        # self.labelFrame.pack(fill='both')
        # self.labelContainer.pack()
        self.share.pack(side=tk.BOTTOM)
        self.upload.pack(side=tk.BOTTOM)
        self.displayFrame.pack(fill='both')
        self.displayContainer.pack()
        self.fileUpload.pack(side=tk.RIGHT, padx=20)
        self.screenShare.pack(side=tk.LEFT, padx=20)
    def toggle(self):
        self.buttOn = not self.buttOn
        self.screenShare.create_image(0, 0, anchor='nw', image=self.offline)
    def close(self):
        self.fullYet = False
        self.new_window.destroy()
        self.new_window.quit()
    def full_screen(self):
        self.new_window = tk.Toplevel()
        self.new_window.title("Share")
        self.wid = self.miner.getDimensions()
        self.canvas = tk.Canvas(self.new_window, width=self.wid[0], height=self.wid[1])
        self.canvas.pack(side=TOP)
        if self.buttOn == True:
            self.scre = Canvas(self.new_window, bg='#ECE2F3', width=300, height=169, bd=0, highlightthickness=0)
            self.scre.place(relx=1.0, rely=1.0, anchor='se')
        self.fullYet = True
        self.display_page()
        self.new_window.protocol("WM_DELETE_WINDOW", self.close)
    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.miner = PDFMiner(self.path)
            data, numPages = self.miner.get_metadata()
            self.current_page = 0
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page, True)
            self.img_file2 = self.miner.get_page(self.current_page, False)
            self.fileUpload.create_image(0, 0, anchor='nw', image=self.img_file)
            if self.fullYet == True:
                self.canvas.create_image(0, 0, anchor='nw', image=self.img_file2)
    def next_page(self):
        if self.fileisopen:
            if self.current_page <= self.numPages - 1:
                self.current_page += 1
                self.display_page()
    def previous_page(self):
        if self.fileisopen:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page()
    def showCanvas(self, success, frame):
        if success and self.buttOn == True:
            image = cv2.resize(frame, (500, 282))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.screenShare.create_image(0, 0, image=self.photo, anchor=tk.NW)
            if self.fullYet == True:
                self.imgee = cv2.resize(frame, (300, 169))
                self.phot = ImageTk.PhotoImage(image=Image.fromarray(self.imgee))
                self.scre.create_image(0, 0, image=self.phot, anchor=tk.NW)