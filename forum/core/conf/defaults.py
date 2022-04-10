from devproject.settings import STATIC_URL

SIGNATURE_MAX_LENGTH = 1024

AVATARS_UPLOAD_TO = 'devproject/avatars'

AVATAR_WIDTH = 60

AVATAR_HEIGHT = 60

DEFAULT_MARKUP = 'bbcode'

FORUM_LOGO_UPLOAD_TO = 'forum/forum_logo'

FORUM_LOGO_WIDTH = 16

FORUM_LOGO_HEIGHT = 16

FORUM_BASE_TITLE = 'Django Bulletin Board'

FORUM_META_DESCRIPTION = ''

FORUM_META_KEYWORDS = ''

JQUERY_URL = '//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.0/jquery.min.js'

NOFOLLOW_LINKS = True

# SMILE Extension
SMILES_SUPPORT = True
EMOTION_SMILE = f'<img src="{STATIC_URL}forum/img/smilies/smile.png"/>'
EMOTION_NEUTRAL = f'<img src="{STATIC_URL}forum/img/smilies/neutral.png"/>'
EMOTION_SAD = f'<img src="{STATIC_URL}forum/img/smilies/sad.png"/>'
EMOTION_BIG_SMILE = f'<img src="{STATIC_URL}forum/img/smilies/big_smile.png" />'
EMOTION_YIKES = f'<img src="{STATIC_URL}forum/img/smilies/yikes.png" />'
EMOTION_WINK = f'<img src="{STATIC_URL}forum/img/smilies/wink.png" />'
EMOTION_HMM = f'<img src="{STATIC_URL}forum/img/smilies/hmm.png" />'
EMOTION_TONGUE = f'<img src="{STATIC_URL}forum/img/smilies/tongue.png" />'
EMOTION_LOL = f'<img src="{STATIC_URL}forum/img/smilies/lol.png" />'
EMOTION_MAD = f'<img src="{STATIC_URL}forum/img/smilies/mad.png" />'
EMOTION_ROLL = f'<img src="{STATIC_URL}forum/img/smilies/roll.png" />'
EMOTION_COOL = f'<img src="{STATIC_URL}forum/img/smilies/cool.png"/>'

_SMILES = ((r'(:|=)\)', EMOTION_SMILE),  # :), =)
           (r'(:|=)\|', EMOTION_NEUTRAL),  # :|, =|
           (r'(:|=)\(', EMOTION_SAD),  # :(, =(
           (r'(:|=)D', EMOTION_BIG_SMILE),  # :D, =D
           (r':o', EMOTION_YIKES),  # :o, :O
           (r';\)', EMOTION_WINK),  # ;\
           (r':/', EMOTION_HMM),  # :/
           (r':P', EMOTION_TONGUE),  # :P
           (r':lol:', EMOTION_LOL),
           (r':mad:', EMOTION_MAD),
           (r':rolleyes:', EMOTION_ROLL),
           (r':cool:', EMOTION_COOL)
           )

SMILES = _SMILES
