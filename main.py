import csv
import json
import requests
from os import walk
from numpy import loadtxt


def main(ip='', port='', audio_dir='C:\\cv-corpus-5.1-2020-06-22\\en\\clips\\',
         out_dir='C:\\cv-corpus-singlewords\\singlewords\\', max_iter=1000):
    url = 'http://' + ip + ':' + port + '/transcriptions?async=false'
    num_clips = 0
    # Get the list of files already processed
    processed = []
    for (dirpath, dirnames, filenames) in walk(out_dir):
        processed.extend(filenames)
        break

    with open('C:\\cv-corpus-5.1-2020-06-22\\en\\train.txt', encoding='utf8') as f1:
        data = csv.reader(f1, delimiter='\t', quotechar='"')
        for row in data:
            num_clips += 1

    timeouts = loadtxt('timeouts.txt', dtype=int, delimiter='\n')

    # Open the table of recording data
    with open('C:\\cv-corpus-5.1-2020-06-22\\en\\train.txt', encoding='utf8') as f:
        data = csv.reader(f, delimiter='\t', quotechar='"')
        # For each row up to the maximum number of iterations, open the audio and transcript
        current_file = 0
        num_blank_transcripts = 0
        num_timeouts = len(timeouts)
        num_missing_files = 0
        for row in data:
            name = row[1].rstrip('.mp3') + '.txt'
            transcript = row[2]
            if transcript == '':
                num_blank_transcripts += 1
            elif current_file > 1 and name not in filenames and current_file not in timeouts:
                audio = audio_dir + row[1]
                # Pass the audio file and transcript to the API
                try:
                    f = {'audio': open(audio, 'rb'),
                         'transcript': transcript}
                    response = requests.post(url, files=f, timeout=4)

                    # Save the API response to the provided output directory
                    try:
                        out = out_dir + name
                        outfile = open(out, 'w')
                        json.dump(response.json(), outfile)
                    except FileNotFoundError:
                        print('Could not write to file: ', out)

                except FileNotFoundError:
                    num_missing_files += 1
                except requests.exceptions.ReadTimeout:
                    timeouts = open('timeouts.txt', 'a')
                    timeouts.write(str(current_file) + '\n')
                    timeouts.close()
                    num_timeouts += 1

            current_file += 1
            print(current_file, '/', num_clips, ' clips processed | ', num_blank_transcripts, ' empty transcripts | ', num_timeouts, ' timeouts | ',
                  num_missing_files, ' missing audio files', end='\r')


if __name__ == "__main__":
    main(out_dir='outputs\\', max_iter=0)
