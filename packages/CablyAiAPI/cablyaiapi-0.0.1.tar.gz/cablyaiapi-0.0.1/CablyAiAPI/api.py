class CablyAIAPI:
    import requests as re, inspect as ins
    from io import BytesIO as bi
    tk = None 

    @classmethod
    def __gam(cls):
        if cls.ins.stack()[1].frame.f_globals["__name__"] != __name__:
            raise PermissionError("No no no, you can't use this function.")
        mo = cls.re.get("https://cablyai.com/models")
        if mo.status_code == 200:
            return mo.json()
        else:
            return "API is down."

    @classmethod
    def __ct(cls):
        if cls.ins.stack()[1].frame.f_globals["__name__"] != __name__:
            raise PermissionError("No no no, you can't use this function.")
        
        if not cls.tk:
            return "Pls set token first, use this in your code: CablyAIAPI.tk = 'your CablyAI token.'"
        return None

    @classmethod
    def ask_ai(cls, md: str, ro: str, p: str):
        ms = cls.__ct()
        if ms:
            return ms

        mds = cls.__gam()
        if mds == "API is down.":
            return mds
        
        ids = [i["id"] for i in mds["data"] if "id" in i and i.get("type") and "chat" in i["type"]]
        if md not in ids:
            return f"Model {md} not found. Avaible models are: {ids}"
        
        mdp = next((i["type"] for i in mds["data"] if i.get("id") == md), None)
        ld = {"model": md, "messages": [{"role": ro,"content": p}], "stream": False} 
        ha = {"Authorization": f"Bearer {cls.tk}", "Content-Type": "application/json"}
        rea = cls.re.post(f"https://cablyai.com/{mdp}", json=ld, headers=ha)
        if rea.status_code == 200:
            return rea.json()["choices"][0]["message"]["content"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 502:
            return "You dont have enoung money to use this model."
        elif rea.status_code == 400:
            return rea.json()["error"]["message"]
        else:
            return "API ERROR."
        
    @classmethod
    def gen_image(cls, md: str, p: str, si: str):
        ms = cls.__ct()
        if ms:
            return ms

        mds = cls.__gam()
        if mds == "API is down.":
            return mds
        
        ids = [i["id"] for i in mds["data"] if "id" in i and i.get("type") and "images" in i["type"]]
        if md not in ids:
            return f"Model {md} not found. Avaible models are: {ids}"
        
        mdp = next((i["type"] for i in mds["data"] if i.get("id") == md), None)
        ld = {"prompt": p, "n": 1, "size": si, "response_format": "url", "model": md}
        ha = {"Authorization": f"Bearer {cls.tk}", "Content-Type": "application/json"}
        rea = cls.re.post(f"https://cablyai.com/{mdp}", json=ld, headers=ha)
        if rea.status_code == 200:
            return rea.json()["data"][0]["url"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 502:
            return "You dont have enoung money to use this model."
        elif rea.status_code == 400:
            return rea.json()["error"]["message"]
        else:
            return "API ERROR."
        
    @classmethod        
    def moderation(cls, md: str, t: str):
        ms = cls.__ct()
        if ms:
            return ms

        mds = cls.__gam()
        if mds == "API is down.":
            return mds
        
        ids = [i["id"] for i in mds["data"] if "id" in i and i.get("type") and "moderations" in i["type"]]
        if md not in ids:
            return f"Model {md} not found. Avaible models are: {ids}"
        
        mdp = next((i["type"] for i in mds["data"] if i.get("id") == md), None)
        ld = {"input": t, "model": md}
        ha = {"Authorization": f"Bearer {cls.tk}", "Content-Type": "application/json"}
        rea = cls.re.post(f"https://cablyai.com/{mdp}", json=ld, headers=ha)
        if rea.status_code == 200:
            return rea.json()["results"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 400:
            return rea.json()["error"]
        else:
            return "API ERROR."

    @classmethod        
    def usage(cls):
        ms = cls.__ct()
        if ms:
            return ms
        ha = {"Authorization": f"Bearer {cls.tk}", "Content-Type": "application/json"}
        rea = cls.re.post(f"https://cablyai.com/usage", headers=ha)
        if rea.status_code == 200:
            return rea.json()
        else:
            return "API is down."
        
    @classmethod        
    def embeddings(cls, md: str, t: str):
        ms = cls.__ct()
        if ms:
            return ms

        mds = cls.__gam()
        if mds == "API is down.":
            return mds
        
        ids = [i["id"] for i in mds["data"] if "id" in i and i.get("type") and "embeddings" in i["type"]]
        if md not in ids:
            return f"Model {md} not found. Avaible models are: {ids}"
        
        mdp = next((i["type"] for i in mds["data"] if i.get("id") == md), None)
        ld = {"input": t, "model": md}
        ha = {"Authorization": f"Bearer {cls.tk}", "Content-Type": "application/json"}
        rea = cls.re.post(f"https://cablyai.com/{mdp}", json=ld, headers=ha)
        if rea.status_code == 200:
            return rea.json()["data"][0]["embedding"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 400:
            return rea.json()["error"]["message"]
        else:
            return "API ERROR."
        
    @classmethod        
    def upscale_image(cls, ip: str):
        ms = cls.__ct()
        if ms:
            return ms

        ha = {'accept': 'image/*', 'Authorization': f'Bearer {cls.tk}'}
        try:
            try:
                fil = cls.re.get(ip)
                con = cls.bi(fil.content)
                fi = {'file': ('i.png', con, 'image/png')}
            except:
                fi = {'file': (ip, open(ip, 'rb'), 'image/png')}
        except:
            return "Image not found. Please provide a valid file path or url."
        rea = cls.re.post("https://cablyai.com/v1/images/upscale", headers=ha, files=fi)
        if rea.status_code == 200:
            try:
                return rea.content
            except:
                return rea.json()["error"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 400:
            return rea.json()["error"]
        else:
            return "API ERROR."
        
    @classmethod        
    def voice_to_text(cls, ip: str):
        ms = cls.__ct()
        if ms:
            return ms

        ha = {'accept': 'application/json', 'Authorization': f'Bearer {cls.tk}'}
        try:
            try:
                fil = cls.re.get(ip)
                con = cls.bi(fil.content)
                fi = {'file': ('i.png', con, 'audio/mpeg')}
            except:
                fi = {'file': (ip, open(ip, 'rb'), 'audio/mpeg')}
        except:
            return "Music not found. Please provide a valid file path or url."
        rea = cls.re.post("https://cablyai.com/v1/audio/transcriptions", headers=ha, files=fi)
        if rea.status_code == 200:
            try:
                return rea.json()["text"]
            except:
                return rea.json()["error"]
        elif rea.status_code == 401:
            return "Token is invalid."
        elif rea.status_code == 400:
            return rea.json()["error"]
        else:
            return "API ERROR."