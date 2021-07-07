import time

def uncipher(key):
    global inp,out
    s = 7
    m = ''
    for i in range(len(out)):
        tmp = key.index(out[i])
        s = tmp ^ s
        m += hex(key[s])[2:]
    print(bytes.fromhex(m))
def back_track(key,check,offset,const):
    #print(key)
    #print(check)
    #print(offset)
    global inp,out
    if(offset == len(inp)):
#        print('wow!!',key)
        uncipher(key)
        return 
    inpval = inp[offset]
    outval = out[offset]
    if(check[inpval] == 1):
        tmpval = key.index(inpval) ^ const
        if(check[outval] == 1):
            if(key[tmpval] == outval):
                #print("First Track!!",inpval,outval)
                back_track(key,check,offset+1,key.index(inpval))
            else:
                return 
        elif(key[tmpval] !=-1):
            return
        else:
            key[tmpval] = outval
            check[outval] = 1
            #print("Second Track!!",inpval,outval)
            back_track(key,check,offset+1,key.index(inpval))
            check[outval] = 0
            key[tmpval] = -1
    else:
        if(check[outval] == 1):
            ind = key.index(outval) ^ const
            if(key[ind] != -1):
                return
            key[ind] = inpval
            check[inpval] = 1
            #print("Third Track!!",inpval,outval)
            back_track(key,check,offset+1,key.index(inpval))
            check[inpval] = 0
            key[ind] = -1
        else:
            for i in range(16):
                if(key[i] != -1):
                    continue
                tmpval = i ^ const
                if(key[tmpval] != -1):
                    continue
                key[i] = inpval
                check[inpval] = 1
                

                key[tmpval] = outval
                check[outval] = 1
                #print("Fourth Track!!",inpval,outval)
                back_track(key,check,offset+1,i)
                key[tmpval] = -1
                check[outval] = 0

                check[inpval] = 0
                key[i] = -1




inputs = b'The secret message is:'.hex()
inputs += b' Nice job! I hope you enjoyed the challenge. Here\'s your flag: '.hex()
inp = []
for i in range(len(inputs)):
    inp.append(int(inputs[i],16))
outs = '85677bc8302bb20f3be728f99be0002ee88bc8fdc045b80e1dd22bc8fcc0034dd809e8f77023fbc83cd02ec8fbb11cc02cdbb62837677bc8f2277eeaaaabb1188bc998087bef3bcf40683cd02eef48f44aaee805b8045453a546815639e6592c173e4994e044a9084ea4000049e1e7e9873fc90ab9e1d4437fc9836aa80423cc2198882a'
out = []
for i in range(len(outs)):
    out.append(int(outs[i],16))

key = [-1 for i in range(16)]
check = [ 0 for i in range(16)]
back_track(key,check,0,7)