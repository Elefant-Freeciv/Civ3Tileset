import requests
import os
import shutil
import numpy as np
from PIL import Image, ImageSequence
from PIL.Image import Palette
from guizero import App, Text, PushButton, Window, TextBox

app = App(title="C3TS Civ 3 Tileset")
space = Text(app, text="")
text1 = Text(app, text="Choose C3TS Input File")
space1 = Text(app, text="")
textbox1 = TextBox(app, text="Civ 3 Standard.c3ts")

def make_spec(tag, folder):
    spec = open(folder+tag+"/"+tag+".spec","w+")
    spec.write('''
;Made by Civ III Tileset for freeciv
;All graphics remain the property of their creators and are subject to their licenses

[spec]

; Format and options of this spec file:
options = "+Freeciv-3.0-spec"

[info]

;

artists = "
    Civ III Graphics Community
"

[extra]
sprites =
	{	"tag", "file"\n''')
    spec.write('		"u.'+tag[2:len(tag)]+'_s", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_s"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_se", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_se"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_e", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_e"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_ne", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_ne"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_n", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_n"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_nw", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_nw"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_w", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_w"\n')
    spec.write('		"u.'+tag[2:len(tag)]+'_sw", "Civ3Tileset v3.0/'+folder+tag+'/final_'+tag+'_sw"\n')
    spec.write('''		}

*include override/flags.spec''')
    spec.close()



    

def convert_img_bg(pic):
    palette = np.array(pic.getpalette(), dtype=np.uint8).reshape((256,3))
    alpha = [
        [25, 0, 25],
        [40,0,40],
        [56,0,56],
        [70,0,70],
        [100,0,100],
        [100,0,100],
        [100,0,100],
        [100,0,100],
        [100,0,100],
        [120,0,120],
        [140,0,140],
        [160,0,160],
        [180,0,180],
        [200,0,200],
        [220,0,220],
        [255,0,255],
        [255,0,255],
        [255,0,255],
        [255,0,255]
        ]
    new_palette = []
    a=0
    i=0
    for colour in palette:
        i += 1
        if i < 239:
            new_palette.append(colour[0])
            new_palette.append(colour[1])
            new_palette.append(colour[2])
            #new_palette.append(255)
        else:
            new_palette.append(alpha[a][0])
            new_palette.append(alpha[a][1])
            new_palette.append(alpha[a][2])
            #new_palette.append(alpha[a][3])
            a+=1
    pic.putpalette(new_palette, rawmode="RGB")
    return pic

def convert_to_transparent(path):
    pic = Image.open(path)
    pic = pic.quantize(colors=128)
    palette = np.array(pic.getpalette(), dtype=np.uint8).reshape((256,3))
    #print(palette)
    new_palette = []
    #print(pic.getpixel((0,0)))
    for colour in palette:
#         if colour.all() == palette[pic.getpixel((0,0))].all():
#             new_palette.append(0)
#             new_palette.append(0)
#             new_palette.append(0)
#             new_palette.append(0)
#             #print(colour)
#             #print(palette[pic.getpixel((0,0))])
        if colour[0] == colour[2]+1 or colour[0] == colour[2] and colour[1] <= colour[0]/2:
            new_palette.append(colour[0])
            new_palette.append(colour[0])
            new_palette.append(colour[0])
            new_palette.append(255 - colour[0])
        else:
            new_palette.append(colour[0])
            new_palette.append(colour[1])
            new_palette.append(colour[2])
            new_palette.append(255)
    pic.putpalette(new_palette, rawmode="RGBA")
    pic.save(path)
    
def crop_to_cimpletoon(path, name, outputpath):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    imgs   =  {}
    imgs["sw"] = Image.open(path+"/d_sw.png")
    imgs["s"]  = Image.open(path+"/d_s.png")
    imgs["se"] = Image.open(path+"/d_se.png")
    imgs["e"]  = Image.open(path+"/d_e.png")
    imgs["ne"] = Image.open(path+"/d_ne.png")
    imgs["n"]  = Image.open(path+"/d_n.png")
    imgs["nw"] = Image.open(path+"/d_nw.png")
    imgs["w"]  = Image.open(path+"/d_w.png")

    for img in imgs:
        #print("next pic")
        zero = imgs[img].getpixel((0,0))
        for x in range(imgs[img].width):
            for y in range(imgs[img].height):
                if imgs[img].getpixel((x,y)) == zero:
                    pass
                else:
                    if x > maxx:
                        maxx = x
                    if x < minx or minx == 0:
                        minx = x
                    if y > maxy:
                        maxy = y
                    if y < miny or miny == 0:
                        miny = y
    print([minx, maxx, miny, maxy])
    print("\n")
    if (maxx-minx)/64 > (maxy-miny)/48:
        yoffset = (48*((maxx-minx)/64)-(maxy-miny))/2
        for img in imgs:
            to_be_saved = imgs[img].crop((minx, miny-yoffset, maxx, maxy+yoffset)).copy()
            to_be_saved.save(path+"/cropped_"+img+".png")
            to_be_saved.resize((64,48), resample=Image.LANCZOS).save((outputpath+name+"/final_"+name+"_"+img+".png"))
    if (maxx-minx)/64 < (maxy-miny)/48:
        xoffset = (64*((maxy-miny)/48)-(maxx-minx))/2
        for img in imgs:
            to_be_saved = imgs[img].crop((minx-xoffset, miny, maxx+xoffset, maxy)).copy()
            to_be_saved.save(path+"/cropped_"+img+".png")
            to_be_saved.resize((64,48), resample=Image.LANCZOS).save((outputpath+name+"/final_"+name+"_"+img+".png"))
    make_spec(name, outputpath)

def convert():
    units=open(textbox1.value, "r")
    line_num=0
    finalPath="output/tileset/"
    tags=[]
    urls=[]
    for line in units:
        if line[0] == "h":
            urls.append(line)
        elif line[0] == "u":
            tags.append(line)
        elif line[0] == "P":
            finalPath = line[1:len(line)].strip()
        elif line[0] == "C":
            finalPath =  line.strip()
        else:
            pass
        
    for link in urls:
        tag = tags[urls.index(link)].strip()
        cwd = os.getcwd()
        os.makedirs(cwd+"/output/tileset/"+tag)
        os.makedirs(cwd+"/"+finalPath+tag)
        if os.path.exists(tag+".rar") == False:
            file = requests.get(link)
            open(tag+".rar", "wb").write(file.content)
        os.system('cmd /c "7z.exe e "'+tag+'".rar -ooutput/temp/"'+tag+'" -y"')
        for file in os.listdir("output/temp/"+tag):
            if file.endswith('.flc') and file.count("Strafe") == 0 and file.count("VTOL") == 0 and os.path.exists("output/tileset/"+tag+"/d_sw.png") == False:
                temp_img = Image.open("output/temp/"+tag+"/"+file)
                try:
                    temp_img.save("output/temp/"+tag+"/test.gif", save_all=True, loop=0)
                except OSError:
                    print("Couldn't Save GIF File")
                else:
#                     try:
#                         test_img = Image.open("output/temp/"+tag+"/Default.flc")
#                         test_img.save("output/temp/"+tag+"/test.gif", save_all=True, loop=0)
#                     except FileNotFoundError:
#                         print("Loading prefered .flc failed. Using Fallback")
#                     except OSError:
#                         print("Loading prefered .flc failed. Using Fallback")
#                     else:
#                         temp_img=test_img
                    convert_img_bg(temp_img).save("output/temp/"+tag+"/test.gif", save_all=True, loop=0)
                    img = temp_img.copy()
                    gif = Image.open("output/temp/"+tag+"/test.gif")
                    print(gif.is_animated)
                    print("frames: "+str(gif.n_frames))
                    frame_loc = 0
                    for frame in ImageSequence.Iterator(gif):
                        frame_loc += 1
                        if frame_loc == 1:
                            try:
                                frame.save("output/tileset/"+tag+"/d_s.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == (gif.n_frames/8)+2:
                            try:
                                frame.save("output/tileset/"+tag+"/d_se.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == (gif.n_frames/4)+3:
                            try:
                                frame.save("output/tileset/"+tag+"/d_e.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == ((gif.n_frames/8)*3)+4:
                            try:
                                frame.save("output/tileset/"+tag+"/d_ne.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == ((gif.n_frames/8)*4)+5:
                            try:
                                frame.save("output/tileset/"+tag+"/d_n.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == ((gif.n_frames/8)*5)+6:
                            try:
                                frame.save("output/tileset/"+tag+"/d_nw.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == ((gif.n_frames/8)*6)+7:
                            try:
                                frame.save("output/tileset/"+tag+"/d_w.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                        elif frame_loc == ((gif.n_frames/8)*7)+8:
                            try:
                                frame.save("output/tileset/"+tag+"/d_sw.png")
                            except OSError:
                               #End of sequence
                               print("Couldn't Save PNG File")
                    convert_to_transparent("output/tileset/"+tag+"/d_s.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_se.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_e.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_ne.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_n.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_nw.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_w.png")
                    convert_to_transparent("output/tileset/"+tag+"/d_sw.png")
                    crop_to_cimpletoon("output/tileset/"+tag, tag, finalPath)

space2 = Text(app, text="")
button1 = PushButton(app, text="Convert", command=convert)
app.display()
    
