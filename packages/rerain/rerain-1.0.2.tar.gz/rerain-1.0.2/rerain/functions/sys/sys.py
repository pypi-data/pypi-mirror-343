import os
import json
import psutil

# # # --- FIND/F/ALL --- # # #

def get_available_drives():
    drives = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.fstype:
            drives.append(partition.device)
    return drives

def find(file_name, max='all', min=1):
    if max == 0 or min == 0:
        return 'ERR_NOT_FOUND'

    try:
        max = int(max) if max != 'all' else float('inf')
        min = int(min) if min != 'all' else 1
    except ValueError:
        pass

    if min > max:
        return 'ERR_MIN_HIGHER'

    profile = os.environ.get('USERPROFILE')
    drives = get_available_drives()
    
    found_files = []
    
    for drive in drives:
        try:
            for root, dirs, files in os.walk(drive + '\\'):
                for file in files:
                    if file.lower() == file_name.lower():
                        found_files.append(os.path.join(root, file))
        except PermissionError:
            continue
        except FileNotFoundError:
            return 'ERR_HARDWARE_DISCONNECTED'
    
    if len(found_files) < min:
        return 'ERR_NOT_FOUND'
    
    if max == 'all':
        return json.dumps(found_files, indent=4)
    else:
        return json.dumps(found_files[:max], indent=4)

def findf(folder_name, max='all', min=1):
    if max == 0 or min == 0:
        return 'ERR_NOT_FOUND'

    try:
        max = int(max) if max != 'all' else float('inf')
        min = int(min) if min != 'all' else 1
    except ValueError:
        pass

    if min > max:
        return 'ERR_MIN_HIGHER'

    profile = os.environ.get('USERPROFILE')
    drives = get_available_drives()

    found_folders = []
    
    for drive in drives:
        try:
            for root, dirs, files in os.walk(drive + '\\'):
                for folder in dirs:
                    if folder.lower() == folder_name.lower():
                        found_folders.append(os.path.join(root, folder))
        except PermissionError:
            continue
        except FileNotFoundError:
            return 'ERR_HARDWARE_DISCONNECTED'
    
    if len(found_folders) < min:
        return 'ERR_NOT_FOUND'
    
    if max == 'all':
        return json.dumps(found_folders, indent=4)
    else:
        return json.dumps(found_folders[:max], indent=4)

def findall(criteria, max='all', min=1):
    if max == 0 or min == 0:
        return 'ERR_NOT_FOUND'

    try:
        max = int(max) if max != 'all' else float('inf')
        min = int(min) if min != 'all' else 1
    except ValueError:
        pass

    if min > max:
        return 'ERR_MIN_HIGHER'

    profile = os.environ.get('USERPROFILE')
    drives = get_available_drives()
    
    extensions = criteria.get('extensions', None)
    files = criteria.get('files', None)
    folders = criteria.get('folders', None)

    found_files = []
    found_folders = []

    for drive in drives:
        try:
            for root, dirs, files_in_root in os.walk(drive + '\\'):
                for file in files_in_root:
                    if files:
                        if any(file.lower() == f.lower() for f in files):
                            if extensions is None or any(file.lower().endswith(ext.lower()) for ext in extensions):
                                found_files.append(os.path.join(root, file))

                for folder in dirs:
                    if folders:
                        if any(folder.lower() == f.lower() for f in folders):
                            found_folders.append(os.path.join(root, folder))
        except PermissionError:
            continue
        except FileNotFoundError:
            return 'ERR_HARDWARE_DISCONNECTED'
    
    result = {}
    
    if found_files:
        result['files'] = found_files
    if found_folders:
        result['folders'] = found_folders
    
    if len(found_files) < min and len(found_folders) < min:
        return 'ERR_NOT_FOUND'
    
    if max == 'all':
        return json.dumps(result, indent=4) if result else 'ERR_NOT_FOUND'
    else:
        if len(found_files) < max or len(found_folders) < max:
            return json.dumps(result, indent=4) if result else 'ERR_NOT_FOUND'
        return json.dumps(result, indent=4) if result else 'ERR_NOT_FOUND'

# # # --- FIND/F/ALL --- # # #

# # # --- RM/CREATE --- # # #

SUCCESS_CREATE_FILE = "SUCCESS_CREATE_FILE"
ERR_CREATE_FILE = "ERR_CREATE_FILE"
SUCCESS_DELETE_FILE = "SUCCESS_DELETE_FILE"
ERR_DELETE_FILE = "ERR_DELETE_FILE"
ERR_NO_PERMS = "ERR_NO_PERMS"
ERR_FILE_NOT_FOUND = "ERR_FILE_NOT_FOUND"

def create(file_path, content=""):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return SUCCESS_CREATE_FILE
    except PermissionError:
        return ERR_NO_PERMS
    except Exception:
        return ERR_CREATE_FILE

def rm(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return SUCCESS_DELETE_FILE
        else:
            return ERR_FILE_NOT_FOUND
    except PermissionError:
        return ERR_NO_PERMS
    except Exception:
        return ERR_DELETE_FILE

# # # --- RM/CREATE --- # # #