from vatf_generator import play, ctx, recording, command, sleep, sampling
from vatf_generator.vatf_utils.config import Config

import logging
import sys

import logger

#recording_sink = "bluez_sink.88_D0_39_F4_B8_85.a2dp_sink.monitor.pcm"
recording_sink = "bluez_sink.F8_4B_3A_9E_8E_14.a2dp_sink.monitor.pcm"

def get_sampling_config(recording_path_cmd, config = None):
    config = sampling.SamplingConfig(config)
    config.count = -1
    #config.start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
    #config.end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    config.path_to_log = "/tmp/alexa_sampleapp.log"
    config.path_to_recording = recording_path_cmd
    config.path_to_recording_date = f"{recording_path_cmd}.date"
    config.from_line = 0
    config.lines_to_save = ""
    return config

def Test_One_Question():
    ctx.CleanupTrap()
    proxy_recording_dir_path = recording.Rec()
    logger.Start("log/session")
    command.Run("echo 't' > /tmp/alexa_input.pipe")
    play.PlayAudio("alexa_are_you_there.wav")
    sleep.Sleep(5)
    recording_path_cmd = f"$(cat {proxy_recording_dir_path}){recording_sink}"
    sampling.RunWithConfig(get_sampling_config(recording_path_cmd))
    cleanup()

def Test_Two_Questions():
    ctx.CleanupTrap()
    proxy_recording_dir_path = recording.Rec()
    logger.Start("log/session")
    command.Run("echo 't' > /tmp/alexa_input.pipe")
    play.PlayAudio("alexa_are_you_there.wav")
    sleep.Sleep(10)
    command.Run("echo 't' > /tmp/alexa_input.pipe")
    play.PlayAudio("alexa_tell_me_a_joke.wav")
    sleep.Sleep(10)
    recording_path_cmd = f"$(cat {proxy_recording_dir_path}){recording_sink}"
    sampling.RunWithConfig(get_sampling_config(recording_path_cmd))
    cleanup()

def Test_Two_Questions_SleepRegex():
    alexa_response_end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    alexa_path_to_log = "/tmp/alexa_output.log"
    ctx.CleanupTrap()
    proxy_recording_dir_path = recording.Rec()
    logger.Start("log/session")
    command.Run("echo 't' > /tmp/alexa_input.pipe")
    play.PlayAudio("alexa_are_you_there.wav")
    sleep.WaitForRegex(regex = alexa_response_end_regex, path_to_log = alexa_path_to_log)
    command.Run("echo 't' > /tmp/alexa_input.pipe")
    play.PlayAudio("alexa_tell_me_a_joke.wav")
    sleep.WaitForRegex(regex = alexa_response_end_regex, path_to_log = alexa_path_to_log)
    recording_path_cmd = f"$(cat {proxy_recording_dir_path}){recording_sink}"
    sampling.RunWithConfig(get_sampling_config(recording_path_cmd))
    cleanup()

def cleanup():
    recording.Stop()
    logger.Stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    config = Config("config.json")
    #setattr(config, "vatf_utils_branch", "develop_20220130")
    #setattr(config, "vatf_executor_branch", "issues/9")
    ctx.CreateTest(config, sys.argv[1], Test_One_Question.__name__, Test_One_Question, cleanup)
    ctx.CreateTest(config, sys.argv[1], Test_Two_Questions.__name__, Test_Two_Questions, cleanup)
    ctx.CreateTest(config, sys.argv[1], Test_Two_Questions_SleepRegex.__name__, Test_Two_Questions_SleepRegex, cleanup)
