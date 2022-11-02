import os
from uuid import uuid4

def createRandomCode():
    from random import randint
    return randint(10000,99999)


def sendSMS(mobile_number,message):
    pass




class FileUploader:
    def __init__(self,dir,prefix):
        self.dir=dir
        self.prefix=prefix

    def upload_image(self,instance,filename):
        filename,format = os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{format}'