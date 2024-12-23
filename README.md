# FastAPI Trader

This a demo project with an app and its autotests. The app runs on FastAPI in docker behind Nginx.
Autotests are based on pytest and allure report, are run in docker, too.

## To developers
The app code is in `trader` folder. All commands are supposed to be called from root folder.

Virtual environments are handled with `poetry`. To add a package: `poetry add your_package`. Don't modify manually `poetry.lock`!

Aware of `qa` folder with its own `Makefile` and a separate env! 

Autotests and linters are run on every pull-request. Allure report is published to [GitHub Pages](https://s1r3m.github.io/fast_api_orders/)

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

* To see Allure report locally:
```bash
make -C qa report
```
**Important**: Make sure you have installed [Allure](https://allurereport.org/docs/install/) locally on your machine to see the report!


**Hint**: you can `cd qa/` to omit `-C qa` part of the commands above.
