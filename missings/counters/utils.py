import random
import string

from django.utils import text


def create_mpp_slug(mp_name, loss_date=None, add_rand_num=False, mpp_slug_len=50):
    chars_available = mpp_slug_len
    ld = ""
    rn = ""
    if loss_date:
        # Why "-= 11"?
        # 1 dash separator and a date in format YYYY-mm-dd (-1999-01-22)
        # PD: If this code still lives after 9999-12-31 this may cause a bug in the
        # slug generated.
        chars_available -= 11
        ld = "-" + loss_date.strftime("%Y-%m-%d")
    if add_rand_num:
        # Why "-= 6"?
        # 1 dash separator and a random number of 5 digits (-89123)
        chars_available -= 6
        rn = "-" + "".join(random.choices(string.digits, k=5))
    return text.slugify(mp_name[:chars_available] + ld + rn)
