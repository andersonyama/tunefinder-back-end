from src.main import create_app


def test_create_app_registers_main_routes():
    app = create_app()

    assert app is not None
    assert app.url_map is not None
    assert any(rule.rule.startswith('/auth') for rule in app.url_map.iter_rules())
    assert any(rule.rule.startswith('/artist') for rule in app.url_map.iter_rules())
    assert any(rule.rule.startswith('/recommend') for rule in app.url_map.iter_rules())
    assert any(rule.rule.startswith('/favoriteArtist') for rule in app.url_map.iter_rules())
