import os
from google_images_download import google_images_download 
from PIL import Image

response = google_images_download.googleimagesdownload() 
Keyword = input("Enter query (divide queries using ;) : ")
limit = int(input("No. of images to be downloaded for each query: "))
nameInitiation = int(input("Enter image name beginning : "))
search_queries = Keyword.split(";") 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chromedriver = os.path.abspath(os.path.join(BASE_DIR,"darkflow/chromedriver"))   

tmp = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp = os.path.abspath(os.path.join(BASE_DIR,"darkflow/downloads/"))   


def downloadimages(query, chromedriver): 
    arguments = {"keywords": query, 
                "format": "png", 
                "limit":limit, 
                "print_urls":True, 
                "size": "medium",
                # CHANGE TYPE for type of image, e.g. face, photo, etc.
                # "type": "photo", 
                "chromedriver" : chromedriver} 
    try: 
        response.download(arguments) 
    except :
        print("No images found in URLs, retry running with different query.")
        
def Rename(folder, nameInitiation):
    count = 0
    extension1 = folder
    extension2 = os.path.join(os.getcwd(),"input/")
    for filename in os.listdir(extension1): 
        name = str(count + nameInitiation) + ".png"
        currentLoc = extension1 + filename 
        destLoc = extension2 + name
        try:
            im = Image.open(currentLoc)
            im.verify()
            os.rename(currentLoc, destLoc) 
            count += 1
        except:
            os.remove(currentLoc)

        im = Image.open(destLoc)
        im_conversion = im.convert('RGBA')
        im_conversion.save(destLoc, format = "PNG", quality = 80)
    return(count)
count = 0
for query in search_queries: 
    downloadimages(query, chromedriver)
    renameFolder = os.path.abspath(os.path.join(tmp,query))   
    count = count + Rename((renameFolder+"/"), (count + nameInitiation))
