# FastAPI Trader Autotests

This a demo project with autotests to the FastAPI Trader app.

[Last Allure Report](https://s1r3m.github.io/fast_api_orders/) on GitHub Pages.

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

* To see Allure report locally:
```bash
make report
```
**Important**: Make sure you have installed [Allure](https://allurereport.org/docs/install/) locally on your machine to see the report!


**Hint**: Make sure you run these commands on `qa` folder or state folder with -C: `make -C qa install`
