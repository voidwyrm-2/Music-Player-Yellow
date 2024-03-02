import pygame
from pygame import mixer
from pathlib import Path
import argparse



def limitmin(input, min):
    if input < min: return min
    else: return input

def limitminmax(input, min, max):
    if input < min: return min
    elif input > max: return max
    else: return input


def stringify(list):
    out = ''
    for i in list: out += str(i)
    return out




allowedexts = (
    '.mp3',
    '.wav',
    '.ogg'
)

files = []



'''parser = argparse.ArgumentParser()

parser.add_argument('path')
#parser.add_argument('usescss', choices=('y', 'n'))

args = parser.parse_args()

musicpath = Path(str(args.path))'''

def loadfiles():
    files.clear()
    if not Path('filepath.txt').exists():
        print('filepath.txt not found, creating new...')
        with open('filepath.txt', 'xt') as fp404: fp404.write('')

    with open('filepath.txt', 'rt') as fp: musicpath = fp.read()
    if musicpath in ('', ' ', None): print('musicpath is empty!'); raise SystemExit()
    musicpath = Path(musicpath)

    if not musicpath.exists(): print(f'path "{musicpath}" doesn\'t exist!'); raise SystemExit()

    if not musicpath.is_dir(): print(f'path "{musicpath}" isn\'t a folder!'); raise SystemExit()


    for file in musicpath.iterdir():
        if str(file).casefold().endswith(allowedexts) and file.is_file(): files.append(str(file))

    if files in ([], [''], [' '], None): print(f'path "{musicpath}" doesn\'t contain any compatible files!'); raise SystemExit()
    files.sort()



loadfiles()



# initialize game
pygame.init()


screenxy = 1400, 800
# creating a screen
screen = pygame.display.set_mode(screenxy)  # passing width and height

# title and icon
pygame.display.set_caption('Music Player Yellow', 'Music Player Yellow')
icon = pygame.image.load('MusicPlayerYellow.png')
pygame.display.set_icon(icon)



pygame.font.init()
mainfont = pygame.font.Font('freesansbold.ttf', 16)
searchfont = pygame.font.Font('freesansbold.ttf', 40)
clock = pygame.time.Clock()



cyclenum = 0


currentsongindex = 0
currentsong = currentsongindex
mixer.music.load(files[currentsongindex])

searchmode = False
queuemode = False
searching = ''


gunhat = 0



pathtofolder = str(files[0]).removesuffix('/' + str(files[0]).split('/')[-1]) + '/...'

def showfiles():
    color = 255, 255, 255
    if searchmode: color = 180, 180, 180
    folderpath = mainfont.render(f'from folder "{pathtofolder}"', True, color)
    screen.blit(folderpath, (0, 0))
    xstart = 0
    x = xstart
    ystart = 20
    y = ystart
    songnum = 0
    while songnum < len(files):
        sname = str(files[songnum]).split('/')[-1].split('.')[0]
        songname = mainfont.render(f'{songnum + 1}: {sname}', True, color)
        screen.blit(songname, (x, y))
        y += 16
        if y >= screenxy[1] - 30: x += 290; y = ystart
        if x >= screenxy[0]: return
        songnum += 1


def showselected(x, y):
    songname = mainfont.render('currently selected: ' + str(currentsongindex + 1), True, (255, 255, 255))
    screen.blit(songname, (x, y))


def showsearching(x, y):
    searched = searchfont.render(searching, True, (255, 255, 0))
    screen.blit(searched, (x, y))

def showsearchmode(x, y):
    searched = searchfont.render('search mode', True, (240, 240, 0))
    screen.blit(searched, (x, y))

def showqueuemode(x, y):
    searched = searchfont.render('queue mode', True, (240, 240, 0))
    screen.blit(searched, (x, y))


def showsongtime(x, y):
    seconds = int(mixer.music.get_pos() / 1000)
    minutes = limitmin(int((mixer.music.get_pos() / 1000) // 60), 0)
    songname = mainfont.render(f'current song time: {minutes}:{seconds}', True, (255, 255, 255))
    screen.blit(songname, (x, y))


def reload():
    global currentsongindex
    currentsongindex = limitminmax(currentsongindex, 0, len(files) - 1)
    mixer.music.stop()
    mixer.music.unload()
    mixer.music.load(files[currentsongindex])


def play(): mixer.music.play(0)

def pause():
    if mixer.music.get_busy(): mixer.music.pause()
    else: mixer.music.unpause()

def stop(): mixer.music.stop()


def queue(filename): mixer.music.queue(filename)

sqmtick = 0
smshow = False
sqshow = False
smtick = 0
running = True
while running:
    currentsongindex = limitminmax(currentsongindex, 0, len(files) - 1)
    #print('current cycle number: ' + str(cyclenum))
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: running = False; break

        if event.type == pygame.KEYDOWN:
            #print(f'pressed "{event.key}"!')
            if event.key == pygame.K_ESCAPE: running = False; break


            if not searchmode:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    currentsongindex += 1
                    currentsong = currentsongindex
                    reload()

                if event.key in (pygame.K_UP, pygame.K_w):
                    currentsongindex -= 1
                    currentsong = currentsongindex
                    reload()

                if event.key == pygame.K_f:
                    currentsongindex = limitminmax(currentsongindex, 0, len(files) - 1)
                    play()

                if event.key == pygame.K_g: pause()

                if event.key == pygame.K_h: stop()

                if event.key == pygame.K_q: searchmode = True

                if event.key == pygame.K_k: searchmode = True; queuemode = True

                if event.key == pygame.K_r: loadfiles(); reload(); pathtofolder = str(files[0]).removesuffix('/' + str(files[0]).split('/')[-1]) + '/...'

            else:
                if event.key == pygame.K_c and gunhat == 0: gunhat = 1
                if event.key == pygame.K_l and gunhat == 1: gunhat = 2
                if event.key == pygame.K_o and gunhat == 2: gunhat = 3
                if event.key == pygame.K_v and gunhat == 3: gunhat = 4
                if event.key == pygame.K_e and gunhat == 4: gunhat = 5
                if event.key == pygame.K_r and gunhat == 5: gunhat = 6

                num = event.key - 48
                if event.key == pygame.K_q and smtick > 2: searching = ''; searchmode = False; queuemode = False
                elif event.key == pygame.K_k and queuemode:  searching = ''; searchmode = False; queuemode = False
                elif event.key == pygame.K_RETURN:
                    if queuemode:
                        quefile = files[limitminmax(int(searching) - 1, 0, len(files) - 1)]
                        mixer.music.queue(quefile)
                        searching = ''
                        searchmode = False
                        queuemode = False
                    else:
                        currentsongindex = limitminmax(int(searching) - 1, 0, len(files) - 1); reload()
                        currentsong = currentsongindex
                        searching = ''
                        searchmode = False
                elif event.key == pygame.K_BACKSPACE:
                    if searching not in ('', ' ', None):
                        lser = list(searching)
                        del lser[-1]
                        searching = stringify(lser)
                else:
                    if num >= 0 and num <= 9: searching += str(num)

    showfiles()

    if searchmode: smtick += 1

    if gunhat >= 6:
        pygame.display.set_caption('Howdy, Gun-hat')
        pygame.display.set_icon(pygame.image.load('Clover.png'))

    if searchmode:
        showsearching(screenxy[0] // 4, screenxy[1] // 2)
        if queuemode:
            if sqmtick >= 70:
                if sqshow: sqshow = False
                else: sqshow = True
                sqmtick = 0
        else:
            if sqmtick >= 70:
                if smshow: smshow = False
                else: smshow = True
                sqmtick = 0
        sqmtick += 1
    else:
        sqmtick = 0
        sqshow = False
        smshow = False
        showselected(0, screenxy[1] - 20)
        showsongtime(200, screenxy[1] - 20)
    
    
    if sqshow: showqueuemode(screenxy[0] // 4, screenxy[1] // 1.5)
    if smshow: showsearchmode(screenxy[0] // 2 - 150, screenxy[1] // 1.5)

    clock.tick(60)
    
    pygame.display.update()
    #cyclenum += 1
    #print(sqmtick)

'''
If you couldn't tell already
This music player is semi-inspired(or something) by Undertale Yellow
I downloaded the soundtrack and made this so I could easily listen to it
'''




'''
Copyright 2024 Nuclear Pasta

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''