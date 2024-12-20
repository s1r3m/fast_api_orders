# FastAPI Trader Autotests

This a demo project with autotests to the FastAPI Trader app.

### Usage
The project comes with `Makefile`.

To work on autotests locally you have to make `qa` folder your source root.

This can be achieved by setting env variable `PYTHONPATH=$(pwd)/qa` or via your IDE if you use one.


* For local usage you have to init environment:
```bash
make install
```

* To start DB and the application locally:
```bash
make start
```

* To run autotests locally:
```bash
make test
```

**Hint**: Make sure you run these commands on `qa` folder or state folder with -C: `make -C qa install`
