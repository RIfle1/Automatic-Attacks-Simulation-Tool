from gui.credential_stuffing.credential import Credential

cs_finished_list = []


def add_finish(keyword):
    global cs_finished_list
    cs_finished_list.append(keyword)


def get_finishes_length():
    global cs_finished_list
    return len(cs_finished_list)


def clear_finishes():
    global cs_finished_list
    cs_finished_list = []


cs_failed_requests = []


def add_failed_request(keyword):
    global cs_failed_requests
    cs_failed_requests.append(keyword)


def get_failed_requests_length():
    global cs_failed_requests
    return len(cs_failed_requests)


def clear_failed_requests():
    global cs_failed_requests
    cs_failed_requests = []


cs_tested_credential_list = []


def add_tested_credential(credential: Credential):
    global cs_tested_credential_list
    cs_tested_credential_list.append(credential)


def get_tested_credential_list():
    global cs_tested_credential_list
    return cs_tested_credential_list


def get_successful_credentials():
    global cs_tested_credential_list
    return [f"Username: {credential.username} \nPassword: {credential.password}" for credential in
            cs_tested_credential_list if credential.success]


def get_failed_credentials():
    global cs_tested_credential_list
    return [credential for credential in cs_tested_credential_list if not credential.success]


def clear_tested_credentials():
    global cs_tested_credential_list
    cs_tested_credential_list = []


def clear_all():
    clear_finishes()
    clear_failed_requests()
    clear_tested_credentials()
