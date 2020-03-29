from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app
from os.path import join

from app.main import helpers

main = Blueprint('main', __name__)


@main.route('/')
def index():
    plot_name = request.args.get('plot')

    if plot_name:
        plot_web_path = join(app.config['PLOTS_WEB_PATH'], plot_name)
    else:
        plot_web_path = None

    return render_template('index.html', plot_web_path=plot_web_path)


@main.route('upload-audio', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        flash('No audio file provided.', 'error')
        return redirect(url_for('main.index'))

    audio = request.files['audio']

    if audio.filename == '':
        flash('No audio file provided.', 'error')
        return redirect(url_for('main.index'))

    if not helpers.is_mp3(audio):
        flash('mp3 files only are allowed.', 'error')
        return redirect(url_for('main.index'))

    uploads_path = join(app.root_path, app.config['UPLOADS_PATH'])
    plots_path = join(app.root_path, app.config['PLOTS_PATH'])

    saved_file = helpers.save_file(audio, uploads_path)

    img_name = helpers.create_spectrogram(saved_file, plots_path)

    flash('Success! "%s" is handled.' % audio.filename)

    return redirect(url_for('main.index', plot=img_name))
