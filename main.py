import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import shutil
import requests


class DownloadWindow(Screen):
        #return baseUrl+str(chapter)+"/%20("+str(page)+").jpg"

    # Refactor the name of the file downloaded with information passed in params
    def fileNameFormat(self, manga, chapter, page, typeFile):
        return manga.replace(" ", "-")+"-"+"{:02d}".format(chapter)+"-"+"{:02d}".format(page)+"."+typeFile.lower()

    # Verify if a directory with the name of the manga is created
    def checkDir(self, manga):
        dirName = manga.replace(" ", "-").lower()
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        except FileExistsError:
            print("Directory ", dirName, " already exists")
        return dirName

    #def checkDownload(self, startChapter, endChapter):

    # Download the image by verifying links of the images. If the program miss some file,
    # it's probably because the links do not exists
    def downloadImage(self, url, manga, startChapter, endChapter, digit):
        digit = int(digit)
        print(digit)
        endChapter = int(endChapter)
        currentChapter = int(startChapter)
        currentPage = 1

        dirName = self.checkDir(manga)

        while currentChapter <= endChapter:
            typeFile = "jpg"
            if digit == 0:
                currentUrl = url+str(currentChapter)+"/"+str(currentPage)+".jpg"
            elif digit == 1:
                currentUrl = url + str(currentChapter) + "/" + "{:02d}".format(currentPage) + ".jpg"
            else:
                print("Error : Url digit format invalid")
                return

            response = requests.get(currentUrl, stream=True)

            if response.status_code == 404 and ".jpg" in currentUrl:
                if digit == 0:
                    currentUrl = url + str(currentChapter) + "/" + str(currentPage) + ".png"
                    typeFile = "png"
                elif digit == 1:
                    currentUrl = url + str(currentChapter) + "/" + "{:02d}".format(currentPage) + ".png"
                    typeFile = "png"
                response = requests.get(currentUrl, stream=True)

            if response.status_code == 404 and ".png" in currentUrl:
                print(
                    "chapter : ", currentChapter,
                    " | page : ", currentPage,
                    " | link : ", currentUrl,
                    " | code : ", response.status_code,
                    " | type : ", typeFile
                )
                currentPage = 1
                currentChapter = currentChapter + 1

            if response.status_code == 200:
                print(
                    "chapter : ", currentChapter,
                    " | page : ", currentPage,
                    " | link : ", currentUrl,
                    " | code : ", response.status_code,
                    " | type : ", typeFile
                )

                nameFile = self.fileNameFormat(manga, currentChapter, currentPage, typeFile)
                currentPage = currentPage+1
                with open(nameFile, 'wb') as output:
                    shutil.copyfileobj(response.raw, output)
                del response
                shutil.move(nameFile, dirName + "/" + nameFile)

            else:
                pass


# Future functionality
class ReaderWindow(Screen):
    pass


class ManagerWindow(ScreenManager):
    pass


kv = Builder.load_file("style.kv")


class MangaReader(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MangaReader().run()
