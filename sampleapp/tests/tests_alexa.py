from vatf import vatf_init
from vatf.generator import gen_tests
from vatf.api import audio, player, wait, shell, log_snapshot
from vatf.utils import config_handler
from vatf.utils import wait_types as w_t

def setup_function():
    config_handler.init_configs(["/home/tests/config/config.json"])
    #config_handler.init_configs(["./config.py"])
    audio.record_inputs_outputs_from_config()
    log_snapshot.start_from_config()

def teardown_function():
    audio.stop()
    log_snapshot.stop()

def regex_alexa_from_state_to_state(state_1, state_2):
    return f"DialogUXStateAggregator:executeSetState:from={state_1},to={state_2},validTransition=true"

def regex_speaking_to_idle():
    return regex_alexa_from_state_to_state("SPEAKING", "IDLE")

def regex_listening_to_idle():
    return regex_alexa_from_state_to_state("LISTENING", "IDLE")

def play_audio(utt):
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio(utt)

def test_1():
    play_audio("/home/assets/audio_files/alexa_are_you_there.wav")
    wait.wait_for_regex(regex = regex_speaking_to_idle(), timeout = 10, pause = 0.5)

def test_2():
    play_audio("/home/assets/audio_files/alexa_dasfas.wav")
    labels = {}
    assert wait.wait_for_regex(regex = [[regex_speaking_to_idle(), w_t.Label("s_t_i")], [regex_listening_to_idle(), w_t.Label("l_t_i")], w_t.RegexOperator.OR], timeout = 10, pause = 0.5, labels = labels)
    assert labels["l_t_i"] or labels["s_t_i"]
    if labels["l_t_i"]:
        play_audio("/home/assets/audio_files/alexa_are_you_there.wav")
        labels = {}
        assert wait.wait_for_regex(regex = [[regex_speaking_to_idle(), w_t.Label("s_t_i")], [regex_listening_to_idle(), w_t.Label("l_t_i")], w_t.RegexOperator.OR], timeout = 10, pause = 0.5, labels = labels)
        assert labels["s_t_i"]
        assert not labels["l_t_i"]
    play_audio("/home/assets/audio_files/alexa_tell_me_a_joke.wav")
    assert wait.wait_for_regex(regex = regex_speaking_to_idle(), timeout = 10, pause = 0.5)
