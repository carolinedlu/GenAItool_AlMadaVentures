import dropbox
DROPBOX_ACCESS_TOKEN = 'sl.Bij4WZdzAAvgifcLQ0Icsb6Mp5nEabogQD25djEC76CeIUajQDl1xL-zFcv7qwDpxxTNZhTM1_YBO5FbLVVKyCI-oIsEgMj-7X9oE7b5i7o98HjS75vyYfNfiT0zEgEGqTFOdpLYKEOF'
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
from urllib.parse import quote

import dropbox

# Dropbox access token
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'

# Create Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

try:
    # List contents of the root folder (empty string as path)
    result = dbx.files_list_folder('')
    
    # Filter out folders from the list of entries
    folder_names = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata)]

    if not folder_names:
        print("No folders found in your Dropbox account.")
    else:
        print("Folders in your Dropbox account:")
        for folder_name in folder_names:
            print(folder_name)
except dropbox.exceptions.AuthError as e:
    print("Error: Invalid Dropbox access token.")
except dropbox.exceptions.ApiError as e:
    print("Error listing folders from Dropbox:", e)
