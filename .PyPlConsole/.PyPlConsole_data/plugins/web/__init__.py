from requests import get
class main:
    def __init__(self, moduleDir, startDir,*a) -> None:
        pass
    
    def catch(self, cmd:str):
        split_cmd = cmd.split()

        if not len(split_cmd)==3:
            print("You need to give a Link and a file name as argument!")
            return
        
        link,file = split_cmd[1:]

        if not "http" in link:
            link = "http://"+link

        try:
            response = get(link)
        except:
            print("Err: Website not responding")
            return
        
        with open(file,"wb") as f:
            f.write(response.content)
            f.close()


        

