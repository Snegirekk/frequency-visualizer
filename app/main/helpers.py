from hashlib import md5
from os.path import join, isfile

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plot


def save_file(file, path):
    filename = md5(file.read()).hexdigest()

    existing_file = ExistingFile(path, filename, 'mp3', file.filename, True)

    if isfile(existing_file.get_full_path()):
        existing_file.is_new = False
    else:
        file.stream.seek(0)
        file.save(existing_file.get_full_path())

    return existing_file


def create_spectrogram(file, plots_path):
    img_name = file.plain_filename + '.png'
    img_path = join(plots_path, img_name)

    if isfile(img_path):
        return img_name

    y, sr = librosa.load(file.get_full_path())
    amplitude = np.absolute(librosa.stft(y))
    librosa.display.specshow(librosa.amplitude_to_db(amplitude, ref=np.max), y_axis='log', x_axis='time')

    plot.title('"%s" spectrogram' % file.original_filename)
    plot.colorbar(format='%+2.0f dB')
    plot.tight_layout()
    plot.savefig(img_path)

    return img_name


def is_mp3(file):
    filename = file.filename
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp3'


class ExistingFile:
    path = None
    plain_filename = None
    extension = None
    original_filename = None
    is_new = True

    def __init__(self, path, plain_filename, extension, original_filename, is_new):
        self.path = path
        self.plain_filename = plain_filename
        self.extension = extension
        self.original_filename = original_filename
        self.is_new = is_new

    def get_full_path(self):
        return join(self.path, '%s.%s' % (self.plain_filename, self.extension))
