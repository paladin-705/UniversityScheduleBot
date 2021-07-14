from multiprocessing import Process


def send_statistic(token, uid, message, intent, user_type=None):
    try:
        if user_type is not None:
            pass
        else:
            if intent != 'unknown':
                pass
            else:
                pass

        return ''
    except:
        pass


def track(token, uid, message, intent, user_type=None):
    Process(target=send_statistic, args=(token, uid, message, intent, user_type)).start()
