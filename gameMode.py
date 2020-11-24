from cmu_112_graphics import *
from tkinter import *
import random
import os

class GameMode(Mode):
    def appStarted(mode):
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "termProject/images/background.jpg")
        mode.background = mode.loadImage(img_dir)
        
        mode.customerScreen = True
        mode.gameScreen = False
        mode.scoringScreen = False

        mode.timeLeft = 61
        mode.timerCount = 0
        mode.timeEnd = False
        mode.pause = False

        mode.customer()
        mode.colorPicker()
        mode.productImages()

    def customer(mode):
        parentDir = os.path.abspath("..")
        # Customers generated with: https://www.cartoonify.de/#cartoonify
        customers = ["customer1.png", "customer2.png", "customer3.png","customer4.png","customer5.png","customer6.png"]
        customer = random.choice(customers)
        img_dir = os.path.join(parentDir, f"termProject/images/customers/{customer}")
        mode.customer = mode.scaleImage(mode.loadImage(img_dir), 2/3)
    
    def productImages(mode):
        parentDir = os.path.abspath("..")
        # Eyeshadow image: http://clipart-library.com/clipart/1401830.htm 
        img_dir = os.path.join(parentDir, "termProject/images/eyeshadow.png")
        mode.eyeshadow = mode.scaleImage(mode.loadImage(img_dir), 1/6)
        # Blush image: https://webstockreview.net/pict/getfirst 
        img_dir = os.path.join(parentDir, "termProject/images/blush.png")
        mode.blush = mode.scaleImage(mode.loadImage(img_dir), 1/5)
        # Lipstick image: https://pngriver.com/pink-lipstick-png-transparent-clipart-image-2-5461/women-lipstick-png-transparent-images-transparent-backgrounds-pink-lipstick-png-12/ 
        img_dir = os.path.join(parentDir, "termProject/images/lipstick.png")
        mode.lipstick = mode.scaleImage(mode.loadImage(img_dir), 1/9)
        # Eraser image: http://clipart-library.com/clipart/15308.htm 
        img_dir = os.path.join(parentDir, "termProject/images/erase.png")
        mode.erase = mode.scaleImage(mode.loadImage(img_dir), 1/5)


    def colorPicker(mode):
        eyeshadowColors = ["pink", "orange", "yellow", "green", "blue", "purple"]
        mode.eyeshadowColor = random.choice(eyeshadowColors)
        blushColors = ["pink", "red", "peach", "orange"]
        mode.blushColor = random.choice(blushColors)
        lipstickColors = ["pink", "red", "nude", "purple"]
        mode.lipstickColor = random.choice(lipstickColors)
    
    def mousePressed(mode, event):
        if mode.timeEnd:
            return

        if mode.pause == False:

            if mode.customerScreen:
                if (700 <= event.x <= 800) and (350 <= event.y < 400):
                    mode.customerScreen = False
                    mode.gameScreen = True
            
            if mode.gameScreen:
                #click on each thing appears color options
                #if click on mode.eyeshadowSelection: rest is false
                #click on a color in color option = can draw
                pass

    def mouseDrag(mode, event):
        if mode.pause == False:
            #color on face
            pass

    def keyPressed(mode, event):
        if event.key == "h":
            mode.pause = True
            mode.app.setActiveMode(mode.app.helpMode)
            mode.pause = False

        if event.key == "p":
            mode.pause = not mode.pause

    def timerFired(mode):
        if mode.pause == False:
            if mode.gameScreen:
                if mode.timerCount % 10 == 0: 
                    if mode.timeLeft > 0:
                        mode.timeLeft -= 1
                    else:
                        mode.timeEnd = True
                mode.timerCount += 1

        if mode.timeEnd:
            mode.scoringScreen = True

    def drawCustomerScreen(mode, canvas):
        cx, cy = mode.width // 2, mode.height // 2

        canvas.create_text(cx, 70, text = "A customer has arrived!", font = "Arial 50 bold", fill = "black")
        canvas.create_image(cx - 150, cy + 50, image = ImageTk.PhotoImage(mode.customer))
        canvas.create_oval(cx + 225 + 220, cy + 100, cx + 225 - 220, cy - 100, fill = "white", outline = "pink")
        canvas.create_text(cx + 225, cy, text = f"\"I would like \n{mode.eyeshadowColor} eyeshadow, \nwith {mode.blushColor} blush, \nand {mode.lipstickColor} lipstick.\"",
                                font = "Arial 30 bold")
        canvas.create_rectangle(cx + 175, mode.height - 125, cx + 275, mode.height - 75, fill = "pink", outline = "")
        canvas.create_text(cx + 225, mode.height - 100, text = "Go!", font = "Arial 30 bold", fill = "black")

        #instructions to open help
        canvas.create_rectangle(10, mode.height - 45, 180, mode.height - 10, fill = "white", outline = "")
        canvas.create_text(20, mode.height - 15, anchor = 'sw', text = "Press H for Help", font = "Arial 20 bold", fill = "black")

    def drawGameScreen(mode, canvas):
        cx, cy = mode.width // 2, mode.height // 2

        #timer
        canvas.create_line(cx - 30, 0, cx - 30, mode.height, fill = "black", width = 5)
        canvas.create_rectangle(cx - 80 - 30, 0, cx + 80 - 30, 40, fill = "white", outline = "black")
        canvas.create_text(cx - 30, 20, text=f'{mode.timeLeft}s remaining', font="Arial 20 bold")

        #customer and order
        canvas.create_text(cx // 2 - 30, 70, text='Opponent', font="Arial 30 bold")
        canvas.create_image(cx // 2 - 30, cy + 50, image = ImageTk.PhotoImage(mode.customer))
        canvas.create_text(cx + cx // 2 - 60, 70, text='You', font="Arial 30 bold")
        canvas.create_image(cx + cx // 2 - 60, cy + 50, image = ImageTk.PhotoImage(mode.customer))
        canvas.create_rectangle(cx - 100 - 30, 50, cx + 100 - 30, 160, fill = "white", outline = "black")
        canvas.create_text(cx - 30, 60, text = f"Check List:\n- {mode.eyeshadowColor} eyeshadow\n- {mode.blushColor} blush\n- {mode.lipstickColor} lipstick",
                                font = "Arial 20", anchor = "n")
            
        #makeup
        products = ["Eyeshadow", "Blush", "Lipstick", "Erase"]
        pictures = [mode.eyeshadow, mode.blush, mode.lipstick, mode.erase]
        for i in range(len(products)):
            boxHeight = mode.height // 4
            canvas.create_rectangle(mode.width - 100, i * boxHeight, mode.width, (i+1) * boxHeight, fill = "pink", outline = "black")
            canvas.create_image(mode.width - 50, (i + 0.4) * boxHeight, image = ImageTk.PhotoImage(pictures[i]))
            canvas.create_text(mode.width - 50, (i + 0.8) * boxHeight, text = f'{products[i]}', font = "Arial 15 bold")

        #instructions to open help and pause
        canvas.create_rectangle(10, mode.height - 70, 190, mode.height - 10, fill = "white", outline = "")
        canvas.create_text(20, mode.height - 15, anchor = 'sw', text = "Press H for Help \nPress P to Pause", font = "Arial 20 bold", fill = "black")
    
        if mode.timeEnd:
                canvas.create_rectangle(cx - 200, cy - 100, cx + 200, cy + 100, fill = "gray", outline = "black")
                canvas.create_text(cx, cy, text="Time is Up!", font="Arial 50 bold")

    def drawColorOptions(mode, canvas):
        #if mode.eyeshadowSelection == True:
            #draw color options
        #elif mode.blushSelection == True:
        #elif mode.lipstickSelection == True:
        pass

    def redrawAll(mode, canvas):
        cx, cy = mode.width // 2, mode.height // 2

        #background
        canvas.create_image(cx, cy, image = ImageTk.PhotoImage(mode.background))

        if mode.customerScreen:
            GameMode.drawCustomerScreen(mode, canvas)
        elif mode.gameScreen:
            GameMode.drawGameScreen(mode,canvas)
            GameMode.drawColorOptions(mode, canvas)
        
