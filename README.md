# fastapi-pydantic-v2

Sample implementation to validate requests with custom context.

```
$ rye sync
$ rye run main:app --reload
```

```
$ curl -s localhost:8000/items | jq
{
  "items": []
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "hoge"}' | jq
{
  "item": {
    "id": 0,
    "name": "hoge"
  }
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "hoge"}' | jq
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "name"
      ],
      "msg": "Value error, name must be unique.",
      "input": "hoge",
      "ctx": {
        "error": {}
      },
      "url": "https://errors.pydantic.dev/2.6/v/value_error"
    }
  ]
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "fuga"}' | jq
{
  "item": {
    "id": 1,
    "name": "fuga"
  }
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "piyo"}' | jq
{
  "item": {
    "id": 2,
    "name": "piyo"
  }
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "foo"}' | jq
{
  "item": {
    "id": 3,
    "name": "foo"
  }
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "bar"}' | jq
{
  "item": {
    "id": 4,
    "name": "bar"
  }
}
$ curl -s localhost:8000/items -XPOST -H 'content-type: application/json' -d '{"name": "baz"}' | jq
{
  "detail": [
    {
      "type": "value_error",
      "loc": [],
      "msg": "Value error, max 5 items.",
      "input": {
        "name": "baz"
      },
      "ctx": {
        "error": {}
      },
      "url": "https://errors.pydantic.dev/2.6/v/value_error"
    }
  ]
}
```
