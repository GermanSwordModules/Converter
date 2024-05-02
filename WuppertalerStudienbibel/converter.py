import os, subprocess
import unicodedata as ud
import pdfplumber
import re
titelfilename = "wupp-titel.txt"
titel2filename = "wupp-titel+verse.txt"
sbfile = "wupp.txt"
outfile = "WSB.xml"

wupbooks = {"Mt":"Matt", 
          "Mk":"Mark",
         "Lk":"Luke", "Luk.":"Luke",
          "Joh":"John", "Jo":"John",
           "Apg":"Acts",
          "Röm":"Rom", "Rö":"Rom","Rom":"Rom",
           "1.Kor":"1Cor", "1 Kor":"1Cor", "1. Kor":"1Cor",
          "2.Kor":"2Cor", "2 Kor":"2Cor", "2. Kor":"2Cor",
          "Gal":"Gal",
          "Eph":"Eph",
          "Phil":"Phil",
          "Kol":"Col", "Kol.":"Col",
          "1.Thess":"1Thess","1 Th":"1Thess",
          "2.Thess":"2Thess","2 Th":"2Thess",
          "1.Tim":"1Tim","1 Tim":"1Tim", "1. Tim.":"1Tim",
          "2.Tim":"2Tim","2 Tim":"2Tim", "2. Tim.":"2Tim",
          "Tit":"Titus",
          "Phlm":"Phlm",
          "1.Petr":"1Pet", "1 Pt":"1Pet", "1 Petr":"1Pet",
          "2.Petr":"2Pet", "2 Pt":"2Pet", "2 Petr":"2Pet",
          "1.Joh":"1John", "1 Jh":"1John",
          "2.Joh":"2John", "2 Jh":"2John",
          "3.Joh":"3John", "3 Jh":"3John",
          "Hebr":"Heb",
          "Jak":"Jas", 
           "Jud":"Jude",
          "Offb": "Rev", "Ofb":"Rev"} 
          
filter = {"1Mo":"Gen","1 Mo":"Gen", "Gen":"Gen", "1Mose":"Gen",
          "2Mo":"Exod","2 MO":"Exod","2 Mo":"Exod", "Ex":"Exod", "Exod":"Exod",  "2Mose":"Exod", 
          "3Mo":"Lev","3 Mo":"Lev", "Lev":"Lev", "3Mose":"Lev", 
          "Neh":"Neh", 
          "4Mo":"Num","4 Mo":"Num", "Num":"Num", "4Mose":"Num",
          "5Mo":"Deut", "5 Mo":"Deut", "Dtn":"Deut", "Deut":"Deut", "5Mose":"Deut",
          "Dan":"Dan",
          "Ri":"Judg","Richt":"Judg",
          "Rth":"Ruth",
          "1 Sam":"1Sam", "1Sam":"1Sam", "2 Sam":"2Sam", "2Sam":"2Sam",
          "1Kön":"1Kgs","2Kön":"2Kgs","1 Kö":"1Kgs","2 Kö":"2Kgs","1Kö":"1Kgs","2Kö":"2Kgs","1Kö":"1Kgs","2Kö":"2Kgs",
          "1 Ko":"1Kgs", "2 Ko":"2Kgs",
          "1 Chro":"1Chr", "1 Chr":"1Chr", "2 Chr":"2Chr", "2 Chro":"2Chr", 
          "1 Kön":"1Kgs", "2 Kön":"2Kgs",
          "1 Chron":"1Chr", "1 Chr":"1Chr", "2 Chr":"2Chr", "2 Chron":"2Chr", 
          "Esr":"Ezra",
          "Neh":"Neh",
          "Esth":"Esth","Weis":"Wis",
          "Hio":"Job", 
           "Ps":"Ps", 
         "Spr":"Prov","Jdt":"Jdt",
          "Pred":"Eccl",
          "Hoh":"Song",
          "Jes":"Jes",
          "Jer":"Jer",
          "Jos":"Josh",
          "Kla":"Lam",
          "Kl":"Lam",
          "Hes":"Ezek",
          "Dan":"Dan", "Da":"Dan", 
          "Hos":"Hos",
          "Joe":"Joel","Joel":"Joel",
          "Am":"Amos",
          "Ob":"Obad",
          "Jon":"Jonah",
          "Mi":"Mic","Micha":"Mic",
          "Nah":"Nah",
          "Hab":"Hab",
          "Ze":"Zeph", "Zef":"Zeph","Zeph":"Zeph",
          "Hag":"Hag",
          "Sach":"Zech",
          "Mal":"Mal", 
          "Mt":"Matt", 
          "Mk":"Mark","MK":"Mark",
         "Lk":"Luke", "Luk.":"Luke","LK":"Luke",
          "Joh":"John", "Jo":"John",
           "Apg":"Acts",
          "Röm":"Rom", "Rö":"Rom","Rom":"Rom",
           "1Kor":"1Cor", "1 Kor":"1Cor", "1. Kor":"1Cor",
          "2Kor":"2Cor", "2 Kor":"2Cor", "2. Kor":"2Cor",
          "Gal":"Gal",
          "Eph":"Eph",
          "Phil":"Phil","Phi":"Phil","Ph":"Phil",
          "Kol":"Col", "Kol.":"Col",
          "1Th":"1Thess","1 Th":"1Thess",
          "2Th":"2Thess","2 Th":"2Thess",
          "1Tim":"1Tim","1 Tim":"1Tim", "1. Tim.":"1Tim",
          "2Tim":"2Tim","2 Tim":"2Tim", "2. Tim.":"2Tim",
          "Tit":"Titus",
          "Phlm":"Phlm",
          "1Petr":"1Pet", "1 Pt":"1Pet", "1 Petr":"1Pet",
          "2Petr":"2Pet", "2 Pt":"2Pet", "2 Petr":"2Pet",
          "1Joh":"1John", "1 Jh":"1John",
          "2Joh":"2John", "2 Jh":"2John",
          "3Joh":"3John", "3 Jh":"3John","1 Joh":"1John", "1 Jh":"1John",
          "2 Joh":"2John", "2 Jh":"2John", "2 Jo":"2John", "1 Jo":"1John", "3 Jo":"3John", "2Jo":"2John", "1Jo":"1John", "3Jo":"3John", 
          "3 Joh":"3John", "3 Jh":"3John",
          "Hebr":"Heb","Hbr":"Heb","Hb":"Heb",
          "Jak":"Jas", "Jk":"Jas",
           "Jud":"Jude",
          "Offb": "Rev", "Ofb":"Rev", 
         # Apokryphen
           "Sir":"Sir", "Tob":"Tob"}
def markbooks (text):
    for book in filter:
        #print (book)
        #ret = re.findall( )
        bookn = str(filter[book])
        text = re.sub (   r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)" ,
                       '<reference osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+r'>\g<0>'+'</reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(-+)[ ]?(\.?)([0-9]*)" ,
                       '<reference osisRef="'+bookn+r'.\g<2>.\g<3>\g<4>'+bookn+r'.\g<2>.\g<6>'+'"'+r'>\g<0></reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
        # One more Iteration
        text = re.sub (        r"("+book.replace(" ", "[\s]")+")[\.]?[ ]?([0-9]+?),[ ]?([0-9]*)(?!-)[ ]?.*?(\.?)([0-9]*)</reference>[;]?[:]?[ ]?([0-9]+?),[ ]?([0-9]*)" ,
                       '<reference osisRef="'+str(filter[book])+r'.\g<2>.\g<3>\g<4>'+'"'+'>'+book+r' \g<2> \g<3>,\g<4>'+'</reference>'+'; <reference osisRef="'+str(filter[book])+r'.\g<6>.\g<7>'+'"'+r'>\g<6>,\g<7>'+'</reference>'
                    #r'<reference osisRef="'+filter[book]+'.\2.\3\4\5\">\1 \2 \3\4\5\6\7</reference>'
                    , text)
    return text
filter = filter | wupbooks

def markparallels (text):
    refs = text.split(";")
    book = "" 
    ret = '<title type="parallel">(\n'
    for r in refs:
        try:
            r = r.strip()
            ori = r
            r = r.replace(" ff", "").replace("ff", "")
            #print (r)
            if " " in r:
                try:
                    book = filter[r.rsplit(" ",1)[0].strip().replace(".","")]
                except:
                    print ("No book for "+r.rsplit(" ",1)[0])
                    continue
                vv = r.rsplit(" ",1)[1]
            else:
                vv = r
            if len(vv.split(","))>2:
                ch = vv.split(",")[0]
                vv = vv.split(",")[1]+"."+vv.split(",")[2]
                if "-" in vv:
                    osis = book+"."+ch+"."+vv.split("-")[0]+"-"+book+"."+vv.split("-")[1]
            if len(vv.split(","))==1:
                osis = book+"."+vv
            else:
                #print (vv)
                ch = vv.split(",")[0]
                vv = vv.split(",")[1]
                if "-" in vv:
                    osis = book+"."+ch+"."+vv.split("-")[0]+"-"+book+"."+ch+"."+vv.split("-")[1]
                if "." in vv:
                    osis = book+"."+ch+"."+vv.split(".")[0]+"-"+book+"."+ch+"."+vv.split(".")[1]
                else:
                    osis = osis = book+"."+ch+"."+vv
            ret = ret + '<reference type="parallel" osisRef="'+osis+'">'+ori+'</reference>\n'
        except:
            print ("Exception in : "+r)
    ret = ret + ')\n</title>'
    return ret
books = []
titles = []
verse = []
with open(titelfilename) as file:
    for line in file:
        if " : " in line:
            books.append(line.strip())
            titles.append(line.strip())
        else:
            titles.append(line.strip())
with open(titel2filename) as file:
    for line in file:
        if line.strip() != "":
            rein = False
            for tr in line.split(" "):
                if len(tr)>2:
                    rein = True
            if rein:
                verse.append(line.strip())
def convert_char(old):
    if len(old) != 1:
        return 0
    new = ord(old)
    if 65 <= new <= 90:
        # Upper case letter
        return new - 64
    elif 97 <= new <= 122:
        # Lower case letter
        return new - 96
    # Unrecognized character
    return 0
k = 0
i = 0
j = 0
text = ""
vs = ""
vsl = []
aktbook = ""
chapter = 0
lastv = "3000"
textbuffer = ""
refs = {}
pre = ""
with open(sbfile) as file:
    for line in file:#file:
        if line.strip()=="":
            continue
        line = line.strip()
        numeric = 0
        notnum = False
        for part in line.split(";"):
            for p2 in part.split(" "):
                for p3 in part.split(","):
                    if p3.isnumeric():
                        #print (p2)
                        numeric = numeric + 1
                    else: 
                        for p6 in p3.split(" "):
                            if p6.isnumeric():
                                numeric=numeric+1
                            else:
                                if (len(p6)>5):
                                    #print (p3)
                                    notnum = True
        if ( (len(line.split(";"))+len(line.split(","))) >= 7 or numeric>=4) and not line.strip() in verse and not "die" in line and not "Anm" in line and not "Ich" in line and not "Siehe" in line and not "ich" in line and not "der" in line and not "will" in line and not "Kap" in line and not "seid" in line and not "und" in line and not "Ohren" in line and not "aber" in line and not "wer" in line and not "=" in line and not "wer" in line and (not notnum) and len(line.strip())<90 and not "S." in line and not "Meine" in line and not "wer" in line and not "an" in line and not "Jesus" in line and not "wer" in line and not "V" in line and not "bis" in line and not "ob." in line and not "Ob" in line and not "Vergl" in line and not "+" in line and not "(" in line and not ")" in line:
            # Querverweise
            vs = vs + '\n'+markparallels(line.strip().replace(", ", ","))+"\n"
            continue
        if textbuffer == "":
            try:
                if line.strip().split(" ")[0][-1]==")":
                    links = line.split(" ")[0][:-1].strip()
                    rechts = '<note  n="'+str(convert_char(links))+'">'+ line.replace(line.split(" ")[0], "").strip()+'</note>'
                    #print ("--"+ textbuffer)
                    #if ' '+links+' ' in textbuffer:
                    #    textbuffer = rechts.join(textbuffer.rsplit(' '+links+' ', 1))
                    if ' '+links+' ' in vs:
                        vs = rechts.join(vs.rsplit(' '+links+' ', 1))
                    else:
                        vs = vs + "\n<p>"+line.strip()+" </p>"
                    continue
            except:
                print ("FN in VS")
        #if j > 80:
        #    break
        if line.strip() in verse: #  line.strip() == verse[j] or 
            #print (line)
            ## textbuffer leeren
            #print (textbuffer)
            if textbuffer != "":
                #print (vsl)
                pre = ""
                if len (vsl)>1:
                    if not vsl[0].startswith("1.1"):
                        #print ("--_>"+text[-400:])
                        #print ("===============")
                        pre=text.rsplit("</div>",1)[1]
                        text=text.rsplit("</div>",1)[0]+"</div>"
                        #print (pre)
                    ann = aktbook+"."+vsl[0]+"-"+aktbook+"."+vsl[-1]
                    text = text +  '<div type="section" annotateType="commentary" annotateRef="'+ann+'">\n'+pre
                    text = text + vs+"\n"
                    text = text + (textbuffer)+"\n</div>"
                    textbuffer = ""
                    vs = ""
                    vsl = []
                    #print ("<"+textbuffer)
                    #print (ann)
                elif len (vsl)==1:
                    if not vsl[0].startswith("1.1"):
                        #print ("--_>"+text[-400:])
                        #print ("===============")
                        pre=text.rsplit("</div>",1)[1]
                        text=text.rsplit("</div>",1)[0]+"</div>"
                        #print (pre)
                    ann = aktbook+"."+vsl[0]
                    text = text +  '<div type="section" annotateType="commentary" annotateRef="'+ann+'">\n'+pre 
                    text = text + vs+"\n"
                    text = text + (textbuffer)+"\n</div>"
                    textbuffer = ""
                    vs = ""
                    vsl = []
                    #print ("<"+textbuffer)
                    #print (ann)
                else:
                    text = text + (textbuffer)+"\n"
                textbuffer = ""
                vs = ""
                vsl = []
            ## count
            j = j + 1
            # mindestens vers
            if  line.strip() in titles: # line.strip() == titles[i] or
                i = i + 1
                # mindestens Titel
                if  line.strip() in books: # line.strip() == books[k] or
                    k = k + 1
                    # Buch
                    if aktbook == "":
                        aktbook = filter[line.split(" : ")[0]]
                        text = text + '<div type="book" osisID="'+aktbook+'">\n'
                    else:
                        aktbook = filter[line.split(" : ")[0]]
                        text = text + '</div></div>\n\n<div type="book" osisID="'+aktbook+'">\n'
                    chapter = 0
                    print (aktbook)
                else:
                    # Titel
                    text = text + '\n<title>'+line.strip()+" </title>\n"
            else:
                # Vers
                #print (line)
                vv3 = line.split(" ")[0].replace(".", "").strip()
                
                #try:
                
                if not vv3.isnumeric():
                    textbuffer = textbuffer + "\n<p>"+line.strip()+" </p>"
                else:
                    vv = vv3
                    vs = vs + '\n<p><hi type="italic">'+line.strip()+" </hi></p>"
                    if int(vv)<int(lastv) and int(vv) ==1:
                        
                        chapter = chapter + 1
                        print (vv+"-"+lastv+" --> "+str(chapter))
                        print (line)
                    lastv = vv
                    vsl.append (str(chapter)+"."+lastv)
                #print (vsl)
                #except:
                #    bzw = 2#print ( "Same verse")
        else:
            # Nur text
            #print (line)
            try:
                if line.strip().split(" ")[0][-1]==")":
                    links = line.split(" ")[0][:-1].strip()
                    rechts = '<note  n="'+str(convert_char(links))+'">'+ line.replace(line.split(" ")[0], "").strip()+'</note>'
                    #print ("--"+ textbuffer)
                    if ' '+links+' ' in textbuffer:
                        textbuffer = rechts.join(textbuffer.rsplit(' '+links+' ', 1))
                    elif ' '+links+' ' in vs:
                        vs = rechts.join(vs.rsplit(' '+links+' ', 1))
                    else:
                        textbuffer = textbuffer + "\n<p>"+line.strip()+" </p>"
                else:
                    textbuffer = textbuffer + "\n<p>"+line.strip()+" </p>"
            except:
                print ("ERROR"+line)
                textbuffer = textbuffer + "\n<p>"+line.strip()+" </p>"
if textbuffer != "":
    if len (vsl)>1:
        ann = aktbook+"."+vsl[0]+"-"+aktbook+"."+vsl[-1]
    if len (vsl)==1:
        ann = aktbook+"."+vsl[0]
        text = text + '<div type="section" annotateType="commentary" annotateRef="'+ann+'">\n'
        text = text + vs+"\n"
        text = text + (textbuffer)+"\n</div>"
    else:
        text = text + (textbuffer)+"\n"
text= text+"\n</div>\n</div>"
with open(outfile, "w") as f:
    f.write ('''<?xml version="1.0" encoding="UTF-8"?>
<osis
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"
	xmlns:osis="http://www.bibletechnologies.net/2003/OSIS/namespace"
	xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace http://www.bibletechnologies.net/osisCore.2.1.1.xsd">
	<osisText osisIDWork="WSB" osisRefWork="Commentary" xml:lang="de" canonical="true">
		<header>
			<work osisWork="WSB">
            <title>WSB</title>
            <identifier type="OSIS">KJV.TutorEncoding</identifier>
            <refSystem>Bible.KJV</refSystem>
        </work>
        <work osisWork="defaultReferenceScheme">
            <refSystem>Bible.KJV</refSystem>
        </work>
		</header>
		<div type="bookGroup">
			'''+text+'''
		</div>
	</osisText>
</osis>''')
