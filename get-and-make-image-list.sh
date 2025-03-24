#! /bin/sh
# Script helper for generating image mirroring configuration files.
#
# Description:
# This script generates two files based on the provided registry path:
#   - imagelist.csv: A comma-separated list of Docker images with their respective mirrored versions in the new registry.
#   - imagemirror.add.yaml: YAML additions to append to your kustomization.yaml file for mirroring images from the original registry to the specified new registry.
#
# Usage:
#   Usage: $0 new-registry-path (like myregistry.pflaeging.net/myproject)
#
if [ $# -ne 1 ]; then
  echo "Usage: $0 new-registry-path"
  echo "     (like myregistry.pflaeging.net/myproject)"
  echo "     This command generates 2 files:"
  echo "      - imagelist.csv for image-mirror.py"
  echo "      - imagemirror.add.yaml to append it on your kustomization.yaml"
  exit 0
fi

NEWREGISTRY=$1


# make a csv for image mirroring
kubectl kustomize . --enable-helm | grep image: | awk '{print $2}' | sort -u \
    | sed  -E "s/(.+\/)(.+)(:.*)/\1\2\3,MYNEWREGISTRY\/\2\3/g" \
    | sed -E "s/@sha256(:production)$/\1/g" \
    | sed -E "s&MYNEWREGISTRY&$NEWREGISTRY&g" \
    > imagelist.csv

# create a image mirror addendum for kustomize
echo "images: " > imagemirror.add.yaml
sed  -E "s/(.+\/)(.+)(:.*),(.+):(.+)/- name: \1\2\n  newName: \4\n  newTag: \5/g" \
  < imagelist.csv \
  | sed "s/@sha256//g" \
  >> imagemirror.add.yaml