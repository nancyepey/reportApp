from PIL import Image
img = Image.open("m1.jpg")
largeur_image=30 #width
hauteur_image=28 #height
for y in range(hauteur_image):
    #height y axis vertical
    for x in range(largeur_image):
        #horizontal
        #r,v,b=img.getpixel((x,y))
        #print("rgb for x:",x ,"y:", y, "rouge : ",r,"vert : ",v,"bleu : ",b)
        r,g,b=img.getpixel((x,y))
        print("rgb for x:",x ,"y:", y, "=", "red : ",r,"green : ",g,"blue : ",b)
print("end")