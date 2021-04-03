## Azure Storage Utility Function


Steps to Run

1. `pip install azure-storage-blob`
2. `env:AZURE_STORAGE_CONNECTION_STRING=<CONNECTION_STRIBG>` in powershell or `export AZURE_STORAGE_CONNECTION_STRING=<CONNECTION_STRIBG>` in Linux.
3. Change the conatainer name in the azureStorage.py

To upload file

`python ./azureStorage.py -u <source>,<destination>`

`python ./azureStorage.py -u <source>`


To delete a file

`python ./azureStorage.py -r <name>`

To get Complete List of Blobs: 

`python ./azureStorage.py -d`

