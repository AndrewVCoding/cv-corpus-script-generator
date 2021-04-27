import json
import os

# Prepare a txt file to insert the data into the database
db = open('db_inserts.sql', 'a')

# get a list of all json files
files = []
directory = 'outputs\\'
j = 0
for fname in os.listdir(directory):
    if fname.endswith(".txt"):
        files.append(fname)
        j += 1

# open each json file
i = 0
for fname in files:
    with open('imported\\' + fname) as f:
        try:
            data = json.load(f)
            i += 1

            # Clean up the data
            fname = '\"' + fname.replace('.txt', '') + '\"'
            transcript = '\"' + data['transcript'].replace('\'', '\\\'').replace('"', '') + '\"'

            insert_record = '\nINSERT INTO records VALUES(' + fname + ', ' + transcript + ');'
            db.write(insert_record)

            for w in data['words']:
                if 'alignedWord' in w.keys() and w['alignedWord'] != '<unk>':
                    word = w['alignedWord'].replace('\'', '\\\'').replace('"', '')
                    start = str(w['start'])
                    end = str(w['end'])
                    insert_word = '\nINSERT INTO words (word) VALUES(\"' + word + '\");'
                    db.write(insert_word)
                    insert_clip = '\nINSERT INTO clips VALUES((SELECT (word_id) FROM words WHERE word=\'' + word + '\'), ' + fname + ', ' + start + ', ' + end + ');'
                    db.write(insert_clip)

        except json.decoder.JSONDecodeError:
            print("Could not decode json from file: ", fname)

    print(i, '/', j, ' files processed', end='\r')

db.close()
