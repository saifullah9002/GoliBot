from instabot import Bot
import os
import time
from configparser import ConfigParser
from time import sleep
import  random

class InstagramAutoPostBot:

    # initialize object
    def __init__(self):

        self.bot = Bot()
        self.username_txt = "acvgummies_"
        self.password_txt = "5421263bbb"
        self.time_delay = 1  # delay after reposting media set to 1 hour
        self.user_counter = 0
        self.post_counter = 0
        self.current_file_name=0

        if (os.path.exists('config.ini')):
            self.read_config()
        else:
            self.save_config()

    # log in to instagram
    def login(self):
        bot = self.bot
        bot.login(username=self.username_txt, password=self.password_txt)

    # save config.ini file with object vars
    def save_config(self):
        config = ConfigParser()
        if (os.path.exists('config.ini')):
            os.remove('config.ini')
            print("config.ini exists. Now deleting: config.ini")
        config.read('config.ini')
        config.add_section('settings')
        config.set('settings', 'Username', value='acvgummies_')
        config.set('settings', 'Password', value='5421263b')
        config.set('settings', 'user_counter', value=str(self.user_counter))
        config.set('settings', 'post_counter', value=str(self.post_counter))
        config.set('settings', 'time_delay', value=str(self.time_delay))
        config.set('settings', 'current_file_name', value=str(self.current_file_name))
        with open('config.ini', 'w') as f:
            config.write(f)

    # reads config.ini file
    def read_config(self):
        config = ConfigParser()
        config.read('config.ini')
        self.username_txt = config.get('settings', 'Username')
        self.password_txt = config.get('settings', 'Password')
        self.user_counter = config.getint('settings', 'user_counter')
        self.post_counter = config.getint('settings', 'post_counter')
        self.time_delay = config.getint('settings', 'time_delay')
        self.current_file_name = config.getint('settings', 'current_file_name')

    #generates 29 random hashtags from a file
    def random_hashtag_generator(self):
        list1 = set()
        list2 = set()
        f = open("hashtags/hashtags.txt", 'r')
        for x in f:
            line = x.replace("\n", " ")
            list1.add(line)
        tt = False
        f.close()
        listx = list(list1)
        while (tt == False):
            r = random.randrange(0, len(list1))
            if (len(list2) == 28):
                print(list2)
                print(len(list2))
                strings = " \n"
                for x in list2:
                    strings += x
                print(strings)
                del list2, list1, listx
                return strings
                break
            else:
                list2.add(listx[r])

    # renames all files in folder
    def rename_all_files(self, folder_name):
        files = os.listdir(folder_name)
        for file in files:
            if (file.endswith('.REMOVE_ME')):
                new_name = file[:-10]
                os.rename(folder_name + '/' + file, folder_name + '/' + new_name)

    # reads file that contain caption text
    def read_file_data(self, file, folder_name):
        f = open(file = folder_name + '/' + file, mode = 'r')
        file_content = f.read()
        f.close()
        return file_content

    # posts image with caption
    def repost_photo(self, image_no):
        captions_path='captions'
        hashtags_path = 'hashtags'
        bot = self.bot
        caption_pre = "GOLI APPLE CIDER VINEGAR GUMMIES. SAVE 5% Using LINK IN BIO."
        caption_post = ""
        caption_txt = ""

        #select and create caption part 1
        #select_file = random.randrange(0, 5)
        #files = os.listdir(captions_path)
        #caption_pre = self.read_file_data(file=files[select_file],folder_name=captions_path)
        '''
        # select and create caption part 2
        select_caption_file = random.randrange(0, 7)
        files = os.listdir(hashtags_path)
        caption_post = self.read_file_data(file=files[select_file], folder_name=hashtags_path)
        '''
        caption_post = self.random_hashtag_generator()

        # create full caption
        caption_txt= caption_pre +"\n" +caption_post
        print(caption_txt)
        files = os.listdir("photos")

        if (self.current_file_name==len(files)):
            self.current_file_name = 0
            image_no=0

        #upload image
        print("posting image:  "+ files[image_no])
        bot.upload_photo(photo="photos/" + files[image_no], caption=caption_txt)


        self.rename_all_files("photos")
        image_no = image_no + 1
        self.current_file_name = image_no
        self.save_config()

    def AutoPost(self):
        while(1):
            self.repost_photo(self.current_file_name)
            self.time_delay=random.randrange(15000, 30000)
            sleep(self.time_delay)

        


        


my_bot = InstagramAutoPostBot()
my_bot.login()
my_bot.AutoPost()






















