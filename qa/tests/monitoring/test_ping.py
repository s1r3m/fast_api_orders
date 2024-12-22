def test_ping__always__pong_response(actions):
    response = actions.user.get_ping()
    actions.assertion.check_ping_response(response)
