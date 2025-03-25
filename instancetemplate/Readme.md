# Rollout repo for forgejo

1. make a new repo for your forgejo deployment
1. add the forgejo-okd repo as submodule: `git submodule add git@codeberg.org:ppflaeging/forgejo-okd.git`
1. copy the content of this directory to the root of the new repo `cp forgejo-okd/instancetemplate/* .`
1. edit the following files:

    - `admin-secret.env`

      - set your admin user and password

    - `kustomization.yaml`

      - configure the *namespace* (2 times)
      - configure how you get the helm chart
      - set the helm chart version (<https://code.forgejo.org/forgejo-helm/-/packages/container/forgejo/versions>)
      - give your release a *releaseName*
      - decide if you want a single or ha instance
      - adapt your secret name (also set the same secret name in `values.yaml`)

    - `values.yaml`

      - set your *defaultStorageClass* to your preferred block storage class
      - decide if you want to configure cert-manager
      - define your *storageClass* for shared storage (this is the place where the repos and assets are located)
      - set the *size* of your persistent storage
      - take the secretname from `kustomization.yaml` and put it in *existingSecret*
      - define your DOMAIN, ROOT_URL and APP_NAME
      - you can set other parameters of your installation (reference: <https://forgejo.org/docs/latest/admin/config-cheat-sheet/>)
      - if you want to allow access via ssh, you have to be sure that NodePorts are allowed in your installation.  
        Then you can define a NodePort in the *service.ssh* part. The *SSH_PORT* variable defines the displayed port in the Web-GUI. If you map the port with a load balancer in front of your cluster the mapped port should go here.

1. now you can deploy the instance with `oc kustomize . --enable-helm | oc apply -f -` or via ArgoCD or flux.