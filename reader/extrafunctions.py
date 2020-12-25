def encrypt(message):
    message=message.upper()
    newmess=""
    for i in message:
        if(i>='A' and i<='Z'):
            newmess+=chr(ord('A')+ord('z')-ord(i))
        elif(i>='0' and i<='9'):
            newmess+=str(9-int(i))
        else:
            newmess+=i
    return newmess.upper()
