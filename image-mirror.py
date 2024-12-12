#! env python3
# Copying the containers from one registry to another based on a list.
# Hacked together by peter@pflaeging.net
# cmdline options:
# -v be verbose what we're doing
# -n just print out what you want to do (for debugging)
#

import os, argparse, textwrap

skopeocmd = "skopeo copy --override-arch amd64 --override-os linux --src-tls-verify=false --dest-tls-verify=false"


cmd = argparse.ArgumentParser(description='Copy containers from one registry to another', 
                              epilog='''You have to login to both registries first. 
For example openshift:
    oc login -u myfamoususer api.a2.cp.cna.at:6443
    skopeo login default-route-openshift-image-registry.apps.a2.cp.cna.at --tls-verify=false -u $(oc whoami) -p $(oc whoami -t)
or for gitlab:
    skopeo login -u myuser registry.apps.a2.cp.cna.at --tls-verify=false''',
                              formatter_class=argparse.RawTextHelpFormatter)
cmd.add_argument("-v", "--verbose", help="verbose output", action="store_true")
cmd.add_argument("-n", "--donothing", help="only show the commands, do nothing", action="store_true")
cmd.add_argument("imgfile", help="file with the images to import: source-image,dest-image")

settings = cmd.parse_args()

def executor(cmd):
    if settings.donothing:
        print(cmd)
        return
    if settings.verbose:
        print("Executing: %s" % cmd)
        print(os.popen(cmd).read())
        return

if settings.verbose:
    print("Imagefile: ", settings.imgfile)
try:
    images = open(settings.imgfile, 'r')
except:
    print("Could not open the file with images")
    exit()


for line in images:
    # extract images
    imageline = line.strip().split(',')
    sourceimage = imageline[0]
    destimage = imageline[1]
    executor("%s docker://%s docker://%s" % (skopeocmd, sourceimage, destimage))
