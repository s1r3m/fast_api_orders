# FastAPI Trader

This a demo project with an app and its autotests.

### Usage
The project comes with `Makefile`.

* For local usage you have to init environment:
```bash
make install
```

* To start DB and the application locally:
```bash
make start
```

* To run unittests locally:
```bash
make test
```

## For QA
The project comes with autotests that utilize a separate environment in order not to interfere with the application.

To work on autotests locally you have to make `qa` folder your source root.

This can be achieved by setting env variable `PYTHONPATH=$(pwd)/qa` or via your IDE if you use one.

### Usage
* To quick start the environment simply run:
```bash
make -C qa install
```

* To start DB and the application in docker:
```bash
make -C qa start
```

* To run autotests locally:
```bash
make -C qa test
```

**Hint**: you can `cd qa/` to omit `-C qa` part of the commands above.
