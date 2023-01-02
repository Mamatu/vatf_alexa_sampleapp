from vatf import vatf_init
from vatf.generator import gen_tests
from vatf.api import audio, player, wait, shell, log_snapshot
from vatf.utils import config_handler

def setup_function():
    config_handler.init_configs(["./config.json"])
    #config_handler.init_configs(["./config.py"])
    audio.record_inputs_outputs_from_config()
    log_snapshot.start_from_config()

def teardown_function():
    audio.stop()
    log_snapshot.stop()

def test_1():
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.wait_for_regex(regex = ".*DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true.*", timeout = 600, pause = 0.5)

def test_2():
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.wait_for_regex(regex = ".*DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true.*", timeout = 600, pause = 0.5)
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_tell_me_a_joke.wav")
