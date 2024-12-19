from tools import SMSService
from tools import Mail

def test_sms(sms_client: SMSService):
    sms_client.send_sms("+32476880256", "dit is een test")
    assert True

def test_mail(mail_client: Mail):
    mail_client.delete_all_mail
    mail_client.send_email("This is the subject", "this is the body", "20240182b@gmail.com")
    message = mail_client.get_last_mail()
    assert message.body == "this is the body"
    assert message.subject == "This is the subject"






