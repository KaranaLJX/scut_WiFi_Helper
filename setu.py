import requests
import re
import progressbar
try:
    print("色图gkd...\n")
    HPicurl = "https://raw.githubusercontent.com/alexkimxyz/nsfw_data_scraper/master/raw_data/hentai/urls_hentai.txt"
    rawdata = requests.get(HPicurl)
    print("冲冲冲！\n")
    urlfile = open("tmp_url","r+")
    urlfile.write(str(rawdata.content).replace("\\n","\n"))
    maxn = str(rawdata.content).count("\\n")
    print("找到了%d张色图!\n"%(maxn))

    urlfile.seek(0)
    #urlfile.close()
    #urlfile = open("tmp_url", "r")
    savepath = ".\\"
    global pic,i
    i = 1
    pic = str(urlfile.readline()).replace("b'","").replace("\n","")
    bar = progressbar.ProgressBar(maxval=100,widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage()])
    bar.start()
    while pic:
        r = requests.get(pic)
        savefile = ".\\" + str(i) + "." + str(pic).split("/")[-1].split(".")[-1]
        file = open(savefile, "wb")
        file.write(r.content)
        file.close()
        bar.update(i / maxn)
        pic = urlfile.readline().replace("b'","").replace("\n","")
        i += 1
    urlfile.close()
    bar.finish()
except IOError as e:
    print ("Cannot Read URL file!\n")
