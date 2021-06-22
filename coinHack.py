import os
from pathlib import Path
from xml.etree import ElementTree as et
from winreg import ConnectRegistry, OpenKeyEx, QueryValueEx, HKEY_LOCAL_MACHINE

def getLastModifiedFilePath(basePath: Path) -> Path:
    files = os.listdir(basePath)
    fullFilePaths = [os.path.join(basePath, name) for name in files]
    return Path(max(fullFilePaths, key=os.path.getmtime))

def getProfileXmlPath() -> Path:
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    with OpenKeyEx(reg, "SOFTWARE\Wow6432Node\Valve\Steam") as regKey:
        steamFolder = QueryValueEx(regKey, "InstallPath")[0]

    if not steamFolder:
        raise Exception(f"Steam folder was not found.")

    steamFolder = Path(steamFolder)
    userDataFolder = steamFolder / "userdata"
    profileFolder = getLastModifiedFilePath(userDataFolder) / "632360" / "remote" / "UserProfiles"
    profileXml = getLastModifiedFilePath(profileFolder)
    print(f"User profile XML was fount at \"{profileXml}\"\n")
    return profileXml

def modifyCoinsValue(profileXmlPath: Path) -> None:
    xmlTree = et.parse(profileXmlPath)
    xmlTree.find("coins").text = str(2_147_483_647)
    xmlTree.write(profileXmlPath)
    print(f"Risk of Rain 2 lunar coin count was successfully modified.\n")

def main():
    modifyCoinsValue(getProfileXmlPath())
    # input("Press Enter to exit.")

if __name__ == "__main__":
    main()