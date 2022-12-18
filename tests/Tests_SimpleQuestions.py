from vatf import vatf_init
from vatf.generator import gen_tests
from vatf.api import audio, player, wait, shell
from vatf.utils import config_handler

def setup_function():
    config_handler.init_configs(["./config.json"])
    #config_handler.init_configs(["./config.py"])

def test_example_1():
    audio.record_inputs_outputs_from_config()
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.sleep(5)

def test_example_2():
    audio.record_inputs_outputs_from_config()
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.wait_for_regex(regex = ".*DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true.*", timeout = 600, pause = 0.5)
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_tell_me_a_joke.wav")

if __name__ == "__main__":
    import sys
    import logging
    logging.basicConfig(level=logging.DEBUG)
    gen_tests.create_test(sys.argv[1], test_one_question.__name__, test_one_question)
    gen_tests.create_test(sys.argv[1], test_two_questions.__name__, test_two_questions)
