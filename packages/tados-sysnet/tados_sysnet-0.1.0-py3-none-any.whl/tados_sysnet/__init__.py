import requests,base64,time

class SysnetError(Exception): pass
class SysnetRatelimit(Exception): pass
RATELIMIT="ratelimit"
def serverReq(endpoint,*args,**kw): return requests.post("http://localhost:8000/"+endpoint,*args,**kw)
def register(username,password):
    response=serverReq("register.php",data={"username":username,"password":password}).text
    if response==RATELIMIT: raise SysnetRatelimit("You are being ratelimited.")

    if response.isnumeric(): return int(response)
    elif response=="Username already in use": raise SysnetError(f"Username is already in use ({username})")
    elif response=="Error while saving user": raise SysnetError("Internal server error")
def login(username,password): 
    response=serverReq("login.php",data={"username":username,"password":password}).text
    if response==RATELIMIT: raise SysnetRatelimit("You are being ratelimited.")

    if response.isnumeric(): return int(response)
    else: return False

_urlsafe_b64encode=base64.urlsafe_b64encode
base64.urlsafe_b64encode=lambda s: _urlsafe_b64encode(s).rstrip(b"=")
_urlsafe_b64decode=base64.urlsafe_b64decode
base64.urlsafe_b64decode=lambda s: _urlsafe_b64decode(s+(len(s)%4)*("=" if isinstance(s,str) else b"="))

def getQueue(username,password): 
    result=[]
    response=serverReq("getQueue.php",data={"username":username,"password":password}).text
    if response==RATELIMIT: raise SysnetRatelimit("You are being ratelimited.")
    files=response.split("\n")
    if files[0]=="": return ()
    for file in files:
        try:
            spl=file.split("#")
            spl2=spl[0].split(";")
            senderID=int(spl2[0])
            senderName=base64.urlsafe_b64decode(spl2[1]).decode(errors="replace")
            uploadTime=int(spl[1])
            size=int(spl[2])
            filename=base64.urlsafe_b64decode(spl[3]).decode(errors="replace")
            result.append({"sender":{"ID":senderID,"name":senderName},"time":uploadTime,"size":size,"filename":filename})
        except Exception as e: print("Corrupted file: "+repr(e))
    return tuple(result)
def downloadQueueFile(username,password,file,stream,callback=lambda done: None):
    senderID=file["sender"]["ID"]
    senderName=file["sender"]["name"]
    filename=file["filename"]
    filesize=file["size"]
    uploadTime=file["time"]
    data={
        "username":username,
        "password":password,
        "sender":senderID,
        "time":uploadTime,
        "filename":filename,
    }
    response=serverReq("downloadQueue.php",data=data,stream=True)
    total=int(response.headers.get("content-length",0))
    downloaded=0
    for chunk in response.iter_content(1048576):
        stream.write(chunk)
        downloaded+=len(chunk)
        done=downloaded/total
        callback(done)

def uploadQueueFile(username,password,receiverID,stream):
    response=serverReq("uploadQueue.php",data={"username":username,"password":password,"receiver":receiverID},files={"file":stream}).text
    if response==RATELIMIT: raise SysnetRatelimit("You are being ratelimited.")

    if response=="Success": return True
    else: raise SysnetError("Internal server error")

def getSystemID(username): 
    response=serverReq("getSystemID.php",data={"username":username}).text
    if response==RATELIMIT: raise SysnetRatelimit("You are being ratelimited.")

    if response.isnumeric(): return int(response)
    else: return False
