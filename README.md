Mailgun to Paperless-NGX
========================

This can receive mailgun forwards (webhooks) and send the attachments to paperless

```
$ docker build -t mailgun_to_paperless_ngx .
$ docker run -it -p 3000:3000 \
  -e BIND_PORT=3000 \
  -e API_KEY=foo \
  -e PAPERLESS_URL=http://......:80 \
  -e PAPERLESS_API_KEY=1234567 \
  -e FILE_DIR=/tmp \
  -e SECRET_KEY=asdlfkjasdf \
  mailgun_to_paperless_ngx
```

