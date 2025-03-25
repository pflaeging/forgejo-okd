# Give your go containers an additional custom root ca

in your deployment add:

```yaml
template:
  spec:
    containers:
      env:
      - name: SSL_CERT_DIR
        value: '/var/tmp/ca-trust:/etc/ssl/certs'
      volumeMounts:
        - name: ca-trust
          readOnly: true
          mountPath: /var/tmp/ca-trust
    volumes:
      - name: ca-trust
        projected:
          sources:
            - configMap:
                name: manual-ca-bundle
```

create a configmap with a ca-bundle.crt of all your custom root CA's

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: manual-ca-bundle
data:
  ca-bundle.crt: |-
   
``` 