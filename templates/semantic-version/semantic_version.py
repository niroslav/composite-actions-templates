import re, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--latestTag', required = True)
parser.add_argument('--commitMessage', required = True)
parser.add_argument('--currentBranch', required = True)
parser.add_argument('--pullRequestEvent', required = True)
args = parser.parse_args()

latestTag        = args.latestTag
commitMessage    = args.commitMessage
currentBranch    = args.currentBranch
pullRequestEvent = args.pullRequestEvent

firstTag = "0.0.1"
tagSuffix = "d"
minorIncreasePattern = "(minor)"
majorIncreasePattern = "(major)"

def getNewVersion():
  
  if not isTagValid():
    return initializeTag()
  
  if isNewBranch():
    return initializeTag()
  
  versionArray = split_version()
  majorIndex = versionArray[0]
  minorIndex = versionArray[1]
  patchIndex = bump_version(versionArray[2])
    
  if matchFound(re.escape(majorIncreasePattern)):
    print("\n --> Matched Major. Bumping Major version...\n")
    return(f"{bump_version(majorIndex)}.0.{patchIndex}")
  
  if matchFound(re.escape(minorIncreasePattern)):
    print("\n --> Matched Minor. Bumping Minor version...\n")
    return(f"{majorIndex}.{bump_version(minorIndex)}.{patchIndex}")

  print ('\n --> No change was found. Incrementing Patch version...\n')
  return(f"{majorIndex}.{minorIndex}.{patchIndex}")
  
def isTagValid():
  return bool(re.search(r"(\d+\.){3}.*-" + tagSuffix, latestTag))

def isNewBranch():
  result = re.search("^\d+\.\d+\.\d+\.(.*)-d", latestTag)
  return result.group(1) != currentBranch
      
def initializeTag():
  print(f"\n --> No suitable tags were found for this branch. The version was initialized to '{firstTag}'.\n")
  return(firstTag)

def split_version():
  result = re.search("^(\d+)\.(\d+)\.(\d+)\.\w+", latestTag)
  return result.group(1), result.group(2), result.group(3)

def bump_version(index):
  return int(index)+1
   
def matchFound(pattern):
  reMatch = re.search(f"{pattern}", commitMessage, re.IGNORECASE)
  return reMatch != None  
  
print(f"\n --> script arguments: {args}\n")

if pullRequestEvent == "true":
  
  fullVersion = "1.2.3.fb-d"
  shortVersion = "1.2.3"
  print("\n --> Returning default version.\n")
  
else:

  fullVersion = getNewVersion() + "." + currentBranch + "-" + tagSuffix
  shortVersion = re.search('\d+\.\d+\.\d+', fullVersion)[0]
  print(f"\n --> Full version is: '{fullVersion}'. Short version is: '{shortVersion}'.\n")

#Will have to find an other way to set an output when the command is deprecated...
print(f"::set-output name=fullVersion::{fullVersion}")
print(f"::set-output name=shortVersion::{shortVersion}")
