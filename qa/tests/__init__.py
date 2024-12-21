from pytest import register_assert_rewrite

# Override asserts in module assert_actions (use pytest asserts).
register_assert_rewrite('trader_qa.actions.assertion_actions')
