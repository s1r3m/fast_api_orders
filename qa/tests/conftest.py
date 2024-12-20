from typing import Generator, TypeVar

import pytest

from trader_qa.actions import TraderActions


T = TypeVar('T')
YieldFixture = Generator[T, None, None]


@pytest.fixture
def actions() -> YieldFixture[TraderActions]:
    _actions = TraderActions()
    yield _actions
    _actions.cleanup()
