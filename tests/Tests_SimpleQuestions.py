from vatf.generator import gen_tests
from vatf.api import audio, player, sleep, shell

def Test_One_Question():
    audio.record_inputs_outputs()
    shell.fg("echo 't' > /tmp/alexa_input.pipe")
    player.play_audio("alexa_are_you_there.wav")
    sleep.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    gen_tests.create_test(sys.argv[1], Test_One_Question.__name__, Test_One_Question)
