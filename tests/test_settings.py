from lespy.confs import CONFIGS

def test_debug():
    assert CONFIGS.DEBUG

def test_change_configs():
    CONFIGS.DEBUG = 1
    assert CONFIGS.DEBUG == 1
