from chatbase import Message
from multiprocessing import Process


def send_statistic(token, uid, message, intent, user_type=None):
    try:
        if user_type is not None:
            msg = Message(api_key=token,
                          platform="tg",
                          version="0.1",
                          user_id=uid,
                          message=message,
                          type=user_type)
        else:
            msg = Message(api_key=token,
                          platform="tg",
                          version="0.1",
                          user_id=uid,
                          message=message,
                          intent=intent)
        return str(msg.send())
    except:
        pass


def track(token, uid, message, intent, user_type=None):
    Process(target=send_statistic, args=(token, uid, message, intent, user_type)).start()
