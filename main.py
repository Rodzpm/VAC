from colorama import init, Fore
import os
import cv2
import sys
import shutil
from PIL import Image
import subprocess
import pygame
import fpstimer

class AsciiConverter:

    def __init__(self, image, nb):
        # ascii characters used to build the output text
        self.ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        self.image = Image.open(image)
        self.nb = nb

    # resize image according to a new width
    def resize_image(self, image, new_width=100):
        width, height = image.size
        ratio = height/width
        new_height = int(new_width * ratio)
        resized_image = image.resize((new_width, new_height))
        return(resized_image)

    # convert each pixel to grayscale
    def grayify(self, image):
        grayscale_image = image.convert("L")
        return(grayscale_image)
        
    # convert pixels to a string of ascii characters
    def pixels_to_ascii(self, image):
        pixels = image.getdata()
        characters = "".join([self.ASCII_CHARS[pixel//25] for pixel in pixels])
        return(characters)    

    def main(self, new_width=100):
        # convert image to ascii    
        new_image_data = self.pixels_to_ascii(self.grayify(self.resize_image(self.image)))
        
        # format
        pixel_count = len(new_image_data)  
        ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, pixel_count, new_width)])
         
        # save result to "ascii_image.txt"
        with open("ressources/ascii/frame"+str(self.nb)+".txt", "w") as f:
            f.write(ascii_image)


class NewVideo:

    def __init__(self, path):
        self.path = path

    def video_or_not(self):
        if not os.path.exists("ressources/frame"):
            os.makedirs("ressources/frame")
            os.makedirs("ressources/ascii")
        else:
            shutil.rmtree("ressources/frame")
            os.makedirs("ressources/frame")
            shutil.rmtree("ressources/ascii")
            os.makedirs("ressources/ascii")

        command = "ffmpeg.exe -i "+self.path+" -ab 160k -ac 2 -ar 44100 -vn ressources/ascii/audio.wav"
        subprocess.call(command, shell=True)

        self.cut_frame()
        files = [f for f in os.listdir("ressources/frame") if os.path.isfile(os.path.join("ressources/frame", f))]
        file_count = len(files)
        self.convert_ascii(file_count)
    
    def cut_frame(self):
        vidcap = cv2.VideoCapture(self.path)
        success, image = vidcap.read()
        count = 0
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        clear()
        print("Download all current frames...")
        while success:
            progress_bar(count,length)
            cv2.imwrite("ressources/frame/frame%d.jpg" % count, image)  # save frame as JPEG file
            success, image = vidcap.read()
            count += 1
    
    def convert_ascii(self,file_count):
        print(f"{Fore.LIGHTBLUE_EX}\nConverting frames to ascii...")
        for img in range(file_count):
            progress_bar(img,file_count)
            src = "ressources/frame/frame"+str(img)+".jpg"
            ascii = AsciiConverter(src,img)
            ascii.main()

class PlayVideo:

    def __init__(self):
        self.files = [f for f in os.listdir("ressources/frame") if os.path.isfile(os.path.join("ressources/frame", f))]
        self.file_count = len(self.files)
        self.timer = fpstimer.FPSTimer(30)

    def play(self):
        #60 images par secondes
        os.system('mode con: cols=100 lines=75')
        print('\033[39m')
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load("ressources/ascii/audio.wav")
        pygame.mixer.music.play()
        for i in range(self.file_count):
            with open("ressources/ascii/frame"+str(i)+".txt", "r") as f:
                print(f.read())
            self.timer.sleep()


def main():
    
    clear()
    
    print(f"""   
         {Fore.LIGHTBLUE_EX}_  _  {Fore.LIGHTCYAN_EX}   __  {Fore.LIGHTBLUE_EX}    ___ 
        {Fore.LIGHTBLUE_EX}/ )( \  {Fore.LIGHTCYAN_EX} / _\  {Fore.LIGHTBLUE_EX}  / __)
        {Fore.LIGHTBLUE_EX}\ \/ /  {Fore.LIGHTCYAN_EX}/    \  {Fore.LIGHTBLUE_EX}( (__ 
         {Fore.LIGHTBLUE_EX}\__/{Fore.LIGHTWHITE_EX}(){Fore.LIGHTCYAN_EX} \_/\_/{Fore.LIGHTWHITE_EX}(){Fore.LIGHTBLUE_EX} \___) {Fore.LIGHTMAGENTA_EX}https://github.com/0FA-git
         Version 1.0{Fore.LIGHTBLUE_EX} 
         
    """)

    choice = input("[1] Play video\n\n[2] New video\n\n[3] Exit\n\n > ")
    if choice == "1":
        try:
            with open("ressources/frame/frame0.jpg"): pass
        except IOError:
            print("No video has been converted")
            input("Press any key to continue...")
            main()
        pvideo = PlayVideo()
        pvideo.play()
        main()
    elif choice == "2":
        v = input(f"{Fore.LIGHTBLUE_EX}Provide a valid path for your video: ")
        try:
            with open(v): pass
        except IOError:
            print("Error! The file could not be opened")
            input("Press any key to continue...")
            main()
        video = NewVideo(v)
        video.video_or_not()
        print("\nyour video has been successfully converted. You can now play the video.")
        input("Press any key to continue...")
        main()
    elif choice == "3":
        quit()
    else:
        print("wrong")
        input("Press any key to continue...")
        main()


def progress_bar(current, total, barLength=25):
    progress = int(current) * 100 // total
    arrow = '\033[31m'+'#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write(f'{Fore.LIGHTBLUE_EX}\rProgress: [{arrow}'+'\033[39m'+f'{spaces}] {progress}% {current}/{total}')




if __name__ == "__main__":
    clear = lambda: os.system('cls')
    init(convert=True)
            try:
            with open("ffmpeg.exe"): pass
        except IOError:
            print("Please, install ffmpeg.exe")
            input("Press any key to continue...")
            exit()
    main()
