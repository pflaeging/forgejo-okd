# Forgejo on OKD / Openshift or gubernat with kustomize

Special config for forgejo running in an OKD / OpenShift cluster with *Route* elements and Namespace Resourcequotas, or in gubernat with Ingresses.

The method is complete GitOps based:

1. create an instance repo (look at the instancetemplate directory)
1. use this repo as submodule of the instance repo
1. make your customizings
1. if your in a disconnected scenario mirror the helm chart and the used images (use case: **disconnected installation**)

## internet connected installation

1. make an instance repo for your installation based on the description in [./instancetemplate/Readme.md](./instancetemplate/Readme.md)

## disconnected installation

If your cluster is disconnected, you have to mirror the correct images in your local registry.

(Skopeo has to be installed)

1. make an instance repo for your installation based on the description in [./instancetemplate/Readme.md](./instancetemplate/Readme.md) without the last step (dpeloyment in your cluster)
1. on an Internet connected host:

    - get the helm chart:

      - Method 1: push the oci helm in your local registry:

          ```shell
          # login to your registry
          helm registry login registry.local.lan --insecure
          # pull the gzipped tar from original
          helm pull oci://code.forgejo.org/forgejo-helm/forgejo --version=11.0.5
          # push the helm repo to your registry (org=myorg)
          helm push forgejo-11.0.5.tgz oci://registry.local.lan/myorg/forgejo-helm --insecure-skip-tls-verify
          ```

      - Method 2: get the helm chart local and use it from repo

        - pull forgejo helm: `helm pull oci://code.forgejo.org/forgejo-helm/forgejo --untar --untardir charts/`
        - modify the upper level `kustomization.yaml` so that you get the chart from this directory

    - get the images and push them in your local registry:

      ```shell
      # go to instance directory
      cd forgejo-instance-directory
      # get the image list and generate imagelist.csv and imagemirror.add.yaml
      ./forgejo-okd/get-and-make-image-list.sh mylocalregistry.mynetwork.lan/mymirrorproject
      # login to your local registry
      skopeo login mylocalregistry.mynetwork.lan --tls-verify=false 
      # get and push images
      ./forgejo-okd/image-mirror.py -v imagelist.csv
      ```

1. add the contents of `imagemirror.add.yaml` to the end of the `kustomization.yaml`
1. apply it to your cluster: `oc kustomize --enable-helm | oc apply -f -`

## Addendum

- The master admin is `forgejoadmin` like defined (password down there) in the secret  
  You can change the password in the secret on the cluster and then restart the pods to make it happen

---
Peter Pfläging <<peter@pflaeging.net>>
