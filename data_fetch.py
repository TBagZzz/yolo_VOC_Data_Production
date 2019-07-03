import os
from google_images_download import google_images_download 

response = google_images_download.googleimagesdownload() 
Keyword = input("Enter query : ")
limit = int(input("No. of images to be downloaded : "))
search_queries = [Keyword]
BASE_DIR = os.getcwd()
cd = os.path.join(BASE_DIR,"chromedriver")
tmp = os.path.join(BASE_DIR,"downloads/")   


def downloadimages(query): 
    arguments = {"keywords": query, 
                "format": "png", 
                "limit":limit, 
                "print_urls":True, 
                "size": "medium", 
                "chromedriver" : cd,} 
    try: 
        response.download(arguments) 
    
    except FileNotFoundError: 
        arguments = {"keywords": query, 
                    "format": "png", 
                    "limit":limit, 
                    "print_urls":True, 
                    "size": "medium"} 
                    
        try: 
            response.download(arguments) 
        except: 
            pass
def Rename(folder):
    count = 0    
    extension = folder
    for filename in os.listdir(extension): 
        dst = str(count) + ".png"
        src = extension + filename 
        dst = extension + dst 
        os.rename(src, dst) 
        count += 1
    print("Files Renamed.")

for query in search_queries: 
    downloadimages(query)
    renameFolder = os.path.abspath(os.path.join(tmp,query))   
    Rename(renameFolder+"/")