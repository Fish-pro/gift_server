import uuid


def get_token():
    """
    生成数据库uuid
    :return:
    """
    return "".join(str(uuid.uuid4()).split("-")).upper()
