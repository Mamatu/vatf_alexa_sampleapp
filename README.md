# vatf_alexa_sampleapp
Example of integration vatf with voice assitance in this case alexa sampleapp.

>> In sampleapp directory
>> docker build -f alexasampleapp.Dockerfile --build-arg jobs=4 --no-cache --tag=alexasampleapp:0.0.1 .
>> docker run -it --rm --device /dev/snd alexasampleapp:0.0.1
