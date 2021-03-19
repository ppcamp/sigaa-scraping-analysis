

## How to install and configure:

1. To install:
   * You'll need to create a folder named `mongodb` in this project root, to store the mongo database files.
   * You should run this docker compose from this folder.
     ```bash
     docker-compose up
     ```
   * To access the mongodb interface, it's recommended to use [mongoDB compass][mongodb-compass]

2. To configure:
    * To access you'll need the [access string][access-string]
    ```bash
    # connection example
    mongodb://ppcamp:DRrPaRrHqmaWo43D@localhost:27017/?authSource=admin

    # internet sample
    mongodb+srv://ppcamp:DRrPaRrHqmaWo43D@cluster0.tgt68.mongodb.net/
    ```



<!-- Links -->
[mongodb-compass]: https://www.mongodb.com/try/download/compass
[access-string]: https://docs.mongodb.com/manual/reference/connection-string/