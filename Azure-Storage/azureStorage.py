import argparse
import os, uuid, json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__, ContentSettings

class AzureBlob:
    def __init__(self):
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = 'abhis'
        con_val = self.parseString(connect_str)
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        self.container_client = self.blob_service_client.get_container_client(container= container_name)
        self.blobSite = f"{con_val['DefaultEndpointsProtocol']}://{con_val['AccountName']}.blob.{con_val['EndpointSuffix']}/{container_name}"
        file = open("mime.json", 'r')
        self.mimes = json.loads(file.read().strip())
        file.close()
    
    def parseString(self, con_str):
        dic = {}
        for field in con_str.split(';'):
            for i in range(len(field)):
                if(field[i] == '='):
                    key = field[:i]
                    value = field[i+1:]
            dic[key] = value
        return dic

    def getMimeType(self, fileName):
        extension = fileName.split('.')[-1]
        return self.mimes.get(extension, 'application/octet-stream')

    def upload(self, filePath, fileName):
        if(fileName is None):
            fileName = filePath.split('\\')[-1]
        mimeType = self.getMimeType(fileName)
        contentType = ContentSettings(content_type=mimeType)
        blob_client = self.container_client.get_blob_client(fileName)

        print("\nUploading to Azure Storage as blob:\n\t" + fileName)
        # Upload the created file
        with open(filePath, "rb") as data:
            blob_client.upload_blob(data, content_settings=contentType)
        print("Uploaded", blob_client.url)

    def removeBlob(self, fileName):
        print("trying to remove", fileName)
        try:
            blob_client = self.container_client.get_blob_client(fileName).delete_blob()
        except:
            print("file doesn`t exist\n")
        else:
            print("removed\n",fileName)
    
    def display(self):
        print("Files in the Azure Blob Storage")
        print("{:<50} {:<12} {:<30} {:<60}".format("Name", "Size", "Content-Type", "URL"))
        print("{:<50} {:<12} {:<30} {:<60}".format("----", "----", "------------", "---"))
        for i in self.container_client.list_blobs():
            print("{:<50} {:<12} {:<30} {:<60}".format(i['name'][:50], i['size'], i['content_settings']['content_type'][:30], f"{self.blobSite}/{i['name']}"))
        print()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--Upload", help = "File to be uploaded")
parser.add_argument("-d", "--Display",action='store_true', help = "display complete blob with url")
parser.add_argument("-r", "--Remove", help = "Name of File to be deleted")
args = parser.parse_args()

azureClient = AzureBlob()
if args.Remove:
    azureClient.removeBlob(args.Remove)
if args.Upload:
    tmp = args.Upload.strip().split(',')
    if(len(tmp) == 2):
        azureClient.upload(tmp[0], tmp[1])
    else:
        azureClient.upload(tmp[0], None)
if args.Display:
    azureClient.display()
