'''Utilities and helpers
'''
import os
import time 
import zipfile
import datetime
import xml.etree.ElementTree as etree

import _mssql


def binary(i):
    b = ''
    while i > 0:
        j = i & 1
        b = str(j) + b
        i >>= 1
    return b



def xml_code(node, cmd=False):
    tab=0
    CR=u'\u0010'+u'\u2028'
    code=""
    text=etree.tostring(node)
    for elem in text.split("<"):
        if elem!="":
            if elem[0]=="/": tab-=2
            if cmd: code+= ("".rjust(tab)+"<"+elem)[0:79]+"\n"
            else: code+= ("".rjust(tab)+"<"+elem)+CR
            if elem[0]!="/" and not "/>" in elem: tab+=2
    return code





def timestamp(timer=None):
    if timer is None: timer = time.time()
    dt_obj = datetime.datetime.fromtimestamp(timer)
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")



def filestamp(timer=None):
    if timer is None: timer = time.time()
    dt_obj = datetime.datetime.fromtimestamp(timer)
    return dt_obj.strftime("%Y%m%d-%H%M%S")



def zip_extract(path, dest):
    try:
        zip = zipfile.ZipFile(path, 'r')
    except:
        return 0
    if zip.testzip() is not None: 
        print("ZIP CORRUPT: "+path)
        return 0
    n=0
    #try:
    if True:
        for archive in zip.namelist():
            #print os.path.join(dest, archive)
            zip.extract(archive, dest)
            n+=1
        print(str(n)+" files extracted")
        return n
    #except:
    #    raise Exception()
    #    print "ZIP ERROR: "+path
    #    return 0




def folder(path):
    if not os.path.exists(path): 
        os.makedirs(path)
    return path



def htmlchars(text): 
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")




def ping(host):
    """
    Returns True if host responds to a ping request
    """
    
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0

def internet_on():
    try:
        response=urlopen('http://google.com',timeout=1)
        return True
    except URLError as err: pass
    return False


