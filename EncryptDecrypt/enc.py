import random
from mido import Message, MidiFile, MidiTrack


def GenerateMatrix(seedval):
    import random
    random.seed(seedval)
    finalmatrix=dict()
    String="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z"
    news=String.split()
    channel=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    for i in news:
        finalmatrix[i]=[str(random.randint(1,100))+","+str(random.choice(channel)),str(random.randint(1,100))+","+str(random.choice(channel))
             ,str(random.randint(1,100))+","+str(random.choice(channel)),str(random.randint(1,100))+","+str(random.choice(channel))
             ,str(random.randint(1,100))+","+str(random.choice(channel)),str(random.randint(1,100))+","+str(random.choice(channel))
             ,str(random.randint(1,100))+","+str(random.choice(channel))]
            
    return finalmatrix
def encrypt(seed,message):
    keymatrix=GenerateMatrix(seed)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    timer=0
    finalmap=list()
    mapped=[keymatrix.get(char) for char in message]
    for i in mapped:
        notes=list()
        channels=list()
        for j in i:
            notes.append(int(j.split(",")[0]))
            channels.append(int(j.split(",")[1]))
        finalmap.append([notes,channels])
    for i in finalmap:
        for notes,channels in zip(i[0],i[1]):
            track.append(Message('program_change', program=12, time=timer))
            track.append(Message('note_off', note=0, channel=0, time=timer))
            track.append(Message('note_on', note=notes, channel=channels, time=timer))
            track.append(Message('note_off', note=64, channel=15, time=timer))
            timer=timer+2

    mid.save('new_songs.mid')

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def decrypt(seed,files,lengthdata):
    datalist=list()
    channellist=[]
    notelist=[]
    keymatrix=GenerateMatrix(10)
    sorted_x =sorted(keymatrix.items(), key=lambda t: t[0])
  
    for message in MidiFile(files).play():
        if message.type == 'note_on':
            datalist.append(message)
    for i in xrange(len(datalist)):
        channel=str(datalist[i]).split()[1]
        note=str(datalist[i]).split()[2]
        channellist.append(int(channel.split("=")[1]))
        notelist.append(int(note.split("=")[1]))
    if lengthdata==0:
        print "nothing to decrypt"

    datalis=list()
    decrypted=list()
    channel1=chunkIt(channellist,lengthdata)
    note1=chunkIt(notelist,lengthdata)
    for i, j  in zip(note1,channel1):
        newlis=[]
        for note,channel in zip(i,j):
            newlis.append(str(note)+","+str(channel))
        datalis.append(newlis)
    for values in sorted_x:
        for data in datalis:
            if values[1] == data:
               
                decrypted.append(values[0])
    decrypted.sort()
    return "".join(decrypted)
        
  
        

# message="midhun"
# encrypt(10,message)
# text=decrypt(10,'new_songs.mid',len(message))
# print text
