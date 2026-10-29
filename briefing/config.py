"""Fixed standards for every TBV portfolio briefing. Change these only on purpose:
every film built from this repo inherits them."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
COMPANIES = ROOT / 'companies'
BUILD = ROOT / 'build'
WEB = ROOT / 'web'

FPS = 25
W, H = 1920, 1080
SR = 48000

# brand (TBV guidelines + film look)
COLORS = dict(dark='#282524', warm='#ECE9E4', lg='#F5F5F5', gray='#B4B4B4', mid='#7d7873', orange='#EF7619')

# film structure: block order is fixed for every company
SCRIPT_SECTIONS = ['problem', 'handover', 'how', 'q_ds', 'why', 'ds_a', 'ds_b', 'ds_c', 'ds_d',
                   'q_founders', 'q_words', 'close']
INTERVIEW_SEGMENTS = ['f1', 'f2', 'f3', 'f4']
BLOCK_ORDER = ['problem', 'handover', 'f1', 'how', 'q_ds', 'f2', 'why', 'ds_a', 'ds_b', 'ds_c', 'ds_d',
               'q_founders', 'f3', 'q_words', 'f4', 'close']
CHAPTERS = {'problem': ('01', 'The problem'), 'how': ('02', 'How it works'),
            'why': ('03', 'Why we invested'), 'ds': ('04', 'With Drees & Sommer')}

# readability: every on-screen text must stay readable this long (seconds)
MIN_TEXT_S = 2.4
def reading_time(text):
    """Seconds a viewer needs for one line of on-screen text."""
    n = len(str(text).split())
    return max(MIN_TEXT_S, 0.9 + 0.32 * n)

# audio
VO_LUFS = -16.0                  # voice-over loudnorm target before the mix
MIX_LUFS_RANGE = (-17.5, -15.5)  # integrated loudness of the final mix
PEAK_MAX_DB = -1.0
MUSIC_FILE = ASSETS / 'music' / 'music.mp3'
# loop points in the music file: (position s, loop length s)
INTRO = (11.6798, 6.1006)
ALOOP = (18.32 + 16.274, 16.274)
TWO = (55.58 - 16.274, 4.0657)
BLOOP = (51.249 + 24.3988, 24.3988)
MUSIC_TRIM_TARGET = 0.6          # seconds cut from the music start (fixed so every ident sounds the same)

# delivery
SIZE_LIMIT_BYTES = 29_500_000    # stays under 30 MB for device sync / mail
AUDIO_KBPS = 160
TAG_IMAGE = ASSETS / 'img' / 'tag_internal.png'   # "Internal use only", always on

# ElevenLabs (documented here so every take sounds the same)
ELEVEN = dict(vo_voice='Jessica - Playful, Bright, Warm', intro_voice='Jarnathan', model='Eleven v4',
              stability='50%', notes='Use [pause] tags between sentences. Spell abbreviations as spoken: A I, H S E, C O two.')
INTRO_TEXT = ("The Bau Ventures. [pause] Portfolio briefing number {num_word}. [pause] "
              "Who we backed, why, and what it means for Drees and Sommer. [pause] This is our latest investment.")
NUM_WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
             'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']
