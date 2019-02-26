import requests
import traceback

from rwords.core.exception import IcibaInvalidWordException, IcibaApiPasingException

key = "07D3900414F5CB4AFA8A6AC7B10714EC"
base_url = "http://dict-co.iciba.com/api/dictionary.php?key={}&type=json".format(key)


def get_word_info(word):
    """Return word_info from Iciba"""
    url = base_url+"&w={}".format(word)
    r = requests.get(url)
    info = r.json()

    if "word_name" not in info:
        raise IcibaInvalidWordException()

    try:
        symbol = info["symbols"][0]

        ph = ""
        for key in ['ph_en', 'ph_am', 'ph_other']:
            if symbol.get(key):
                ph = symbol[key]
                break

        mp3_url = ""
        for key in ['ph_en_mp3', 'ph_am_mp3', 'ph_tts_mp3']:
            if symbol.get(key):
                mp3_url = symbol[key]
                break

        tran_means = []
        for p in symbol['parts']:
            tran_means.append({
                'part': p['part'],
                'means': p['means'],
            })

        word_info = {
            "word_name": info["word_name"],
            "ph": ph,
            "tran_means": tran_means,
            "mp3_url": mp3_url,
        }
        return word_info
    except Exception:
        traceback.print_exc()
        traceback.format_exc()
        raise IcibaApiPasingException()
