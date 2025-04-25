identificator = ["secretphrase"]
from PIL import Image
import os
import importlib.resources
import webbrowser
import subprocess
import random
class kurzaj:
    def getbmi():
        return 16

    def say(thing):
        print(f'kurzaj: {thing}')

    def zajebidentifikator():
        print("successfully jewed")
        return identificator

    def wpierdolidentifikator(iden):
        if iden == identificator:
            return True
    def monologskryby():
        print("- Jak to jest być skrybą? Dobrze? Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w życiu najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam. I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie. Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać. Ja miałem szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję mu, życie to śpiew, życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że dzisiaj na przykład buduję maszyny, a jutro... kto wie, dlaczego by nie, oddam się pracy społecznej i będę ot, choćby sadzić... znaczy... marchew.")
    def capybara():
        with importlib.resources.open_binary('kurzaj', 'capybara.jpg') as img_file:
            image = Image.open(img_file)
            return image
    def showcapybara():
        with importlib.resources.open_binary('kurzaj', 'capybara.jpg') as img_file:
            image = Image.open(img_file)
            print(image)
            image.show()

    def togif(image):
        return image.save("togif.gif","GIF")
    def r6femaleavatars():
        subprocess.Popen(["start","chrome","https://www.roblox.com/games/106201290955067/CUTE-R6-Female-Outfits"],shell=True)
    def gayscale(name1,name2):
        rnd = random.randint(0,100)
        print(f'{name1} and {name2} are {rnd}% gay!')
    def symbol():
        import turtle
        ninja = turtle.Turtle()
        ninja.color("black")

        ninja.speed()

        for i in range(4):
            ninja.left(90)
            ninja.forward(90)
            ninja.forward(90)
            ninja.right(90)
            ninja.forward(100)
            ninja.left(90)
            
            ninja.penup()
            ninja.setposition(0, 0)
            ninja.pendown()
            
            ninja.right(0)
            
        turtle.done()

        t = turtle.Turtle()
    def nwd(num1,num2=None):
        lowest = None
        if num2 is not None:
            for i in range(1,min(num1,num2)+1):

                if num1 % i == 0 and num2%i==0:

                    lowest = i 
            return lowest
        else:
            for i in range(1,num1):
                if num1%i == 0:
                    lowest = i 
            return lowest


            


