# Rollout repo for forgejo

1. make a new repo for your forgejo deployment
1. add the forgejo-okd repo as submodule: `git submodule add git@codeberg.org:ppflaeging/forgejo-okd.git`
1. copy the content of this directory to the root of the new repo `cp forgejo-okd/instancetemplate/* .`
1. edit the following files:

    - `forgejo-admin-secret.env`

      - set your admin user and password

    - `kustomization.yaml`

      - configure the *namespace*
      - define prefix and suffix for your installation (we use the application instance as prefix and stage as suffix)
      - configure how you get the helm chart
      - set the helm chart version (<https://code.forgejo.org/forgejo-helm/-/packages/container/forgejo/versions>)

    - `forgejo-config.yaml`

      - fill the 4 variables on top of the file as declared in the comments
      - set your *defaultStorageClass* to your preferred block storage class
      - decide if you want to configure cert-manager
      - define your *storageClass* for shared storage (this is the place where the repos and assets are located)
      - set the *size* of your persistent storage
      - define your APP_NAME
      - you can set other parameters of your installation (reference: <https://forgejo.org/docs/latest/admin/config-cheat-sheet/>)
      - if you want to allow access via ssh, you have to be sure that NodePorts are allowed in your installation.  
        Then you can define a NodePort in the *service.ssh* part. The *SSH_PORT* variable defines the displayed port in the Web-GUI. If you map the port with a load balancer in front of your cluster the mapped port should go here.

    - `postgres-config.yaml` and `valkey-config.yaml`

      - adapt the storageClasses and sizes to your needs

1. now you can deploy the instance with `oc kustomize . --enable-helm | oc apply -f -` or via ArgoCD or flux.
