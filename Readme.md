# Forgejo on OKD / Openshift with kustomize

Special config for forgejo running in an OKD / OpenShift cluster with *Route* elements and Namespace Resourcequotas.

Install:

1. pull forgejo helm: `helm pull oci://code.forgejo.org/forgejo-helm/forgejo --untar --untardir charts/`
1. edit [./values.yaml](./values.yaml)
1. apply it to your cluster: `oc kustomize --enable-helm | oc apply -f -`

## disconnected use

If your cluster is disconnected, you have to mirror the correct images in your local registry.

(Skopeo has to be installed)

1. On an Internet connected host:

    - pull forgejo helm: `helm pull oci://code.forgejo.org/forgejo-helm/forgejo --untar --untardir charts/`
    - get the images and push them in your local registry:

      ```shell
      # get the image list and generate imagelist.csv and imagemirror.add.yaml
      ./get-and-make-image-list.sh mylocalregistry.mynetwork.lan/mymirrorproject
      # login to your local registry
      skopeo login mylocalregistry.mynetwork.lan --tls-verify=false 
      # get and push images
      ./image-mirror.py -v imagelist.csv
      ```

1. edit [./values.yaml](./values.yaml)
1. add the contents of `imagemirror.add.yaml` to the end of the [./kustomization.yaml](./kustomization.yaml)
1. apply it to your cluster: `oc kustomize --enable-helm | oc apply -f -`

---
Peter Pfläging <<peter@pflaeging.net>>
