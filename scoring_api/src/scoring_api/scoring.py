import datetime
import hashlib
import json
import random


def get_score(store, phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    key_parts = [
        first_name or "",
        last_name or "",
        phone or "",
        datetime.datetime.strptime(birthday, '%d.%m.%Y').strftime("%Y%m%d") if birthday is not None else "",
    ]
    key = "uid:" + hashlib.md5("".join(key_parts).encode()).hexdigest()
    # try get from cache,
    # fallback to heavy calculation in case of cache miss
    score = store.cache_get(key) or 0
    if score:
        return score
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    # cache for 60 minutes
    store.cache_set(key, score, 60 * 60)
    return score


def get_interests(cid, store):
    r = store.get("i:%s" % cid)
    r = []
    return json.loads(r) if r else []
