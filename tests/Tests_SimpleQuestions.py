from vatf.generator import gen_tests
from vatf.api import audio, player, wait, shell

def Test_One_Question():
    audio.record_inputs_outputs()
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.sleep(5)

def Test_Two_Questions():
    audio.record_inputs_outputs()
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    wait.wait_for_regex(regex = ".*DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true.*", log_path = None, timeout = 600, pause = 0.5)
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_tell_me_a_joke.wav")

if __name__ == "__main__":
    import sys
    import logging
    logging.basicConfig(level=logging.DEBUG)
    gen_tests.create_test(sys.argv[1], Test_One_Question.__name__, Test_One_Question)
    gen_tests.create_test(sys.argv[1], Test_Two_Questions.__name__, Test_Two_Questions)
