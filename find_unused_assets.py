import sys
import os
import fnmatch
from os.path import join

path = sys.argv[1]

assets_path = join(path,"Assets");
project_settings_path = join(path,"ProjectSettings");

files_by_guid = {}
guid_used = {}

print("Searching files in "+path)

for root, subFolders, files in os.walk(assets_path):
    for filename in fnmatch.filter(files, '*.meta'):
        with open(join(root, filename)) as f:
            content = f.readlines()

        guid = ''
        for line in content:
            if line.find('guid:') != -1:
                guid = line[6:(len(line)-1)]
        # print(filename + ": " + guid)
        files_by_guid[guid] = join(root, filename)[:-5]
        guid_used[guid] = False

print("Found "+str(len(guid_used))+" guids")

for root, subFolders, files in os.walk(assets_path):
    for filename in fnmatch.filter(files, '*.prefab'):
        with open(join(root, filename)) as f:
            content = f.readlines()

        for line in content:
            for guid in files_by_guid:
                if line.find(guid) != -1:
                    guid_used[guid] = True
    for filename in fnmatch.filter(files, '*.unity'):
        with open(join(root, filename)) as f:
            content = f.readlines()

        for line in content:
            for guid in files_by_guid:
                if line.find(guid) != -1:
                    guid_used[guid] = True

for root, subFolders, files in os.walk(project_settings_path):
    for filename in fnmatch.filter(files, '*.asset'):
        with open(join(root, filename)) as f:
            content = f.readlines()

        for line in content:
            for guid in files_by_guid:
                if line.find(guid) != -1:
                    guid_used[guid] = True

print("Files not referencied by GUID:\n")

for guid in files_by_guid:
    if guid_used[guid] == False:
        print(files_by_guid[guid])