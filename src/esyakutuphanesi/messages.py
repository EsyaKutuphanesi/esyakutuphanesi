# -*- coding: utf-8 -*-

# security_messages = dict()
security_messages = {
    'UNAUTHORIZED': ('You do not have permission to view this resource.', 'error'),
    'CONFIRM_REGISTRATION': ('Thank you. Confirmation instructions have been sent to %(email)s.', 'success'),
    'EMAIL_CONFIRMED': (u'Teşekkürler. E-posta adresin doğrulandı.', 'success'),
    'ALREADY_CONFIRMED': (u'E-posta adresin çoktan doğrulandı.', 'info'),
    'INVALID_CONFIRMATION_TOKEN': ('Invalid confirmation token.', 'error'),
    'EMAIL_ALREADY_ASSOCIATED': (u'Bu e-posta başka bir hesap ile ilişkili.', 'error'),
    'PASSWORD_MISMATCH': (u'Parolalar eşleşmiyor', 'error'),
    'RETYPE_PASSWORD_MISMATCH': (u'Parolalar eşleşmiyor', 'error'),
    'INVALID_REDIRECT': ('Redirections outside the domain are forbidden', 'error'),
    'PASSWORD_RESET_REQUEST': (u'Parolanı sıfırlamak için gerekli bilgi e-posta adresine gönderildi.', 'info'),
    'PASSWORD_RESET_EXPIRED': ('You did not reset your password within %(within)s.\
        New instructions have been sent to %(email)s.', 'error'),
    'INVALID_RESET_PASSWORD_TOKEN': ('Invalid reset password token.', 'error'),
    'CONFIRMATION_REQUIRED': ('Email requires confirmation.', 'error'),
    'CONFIRMATION_REQUEST': ('Confirmation instructions have been sent to %(email)s.', 'info'),
    'CONFIRMATION_EXPIRED': ('You did not confirm your email within %(within)s.\
        New instructions to confirm your email have been sent to %(email)s.', 'error'),
    'LOGIN_EXPIRED': ('You did not login within %(within)s.\
        New instructions to login have been sent to %(email)s.', 'error'),
    'LOGIN_EMAIL_SENT': ('Instructions to login have been sent to %(email)s.', 'success'),
    'INVALID_LOGIN_TOKEN': ('Invalid login token.', 'error'),
    'DISABLED_ACCOUNT': (u'Hesap aktif değil', 'error'),
    'EMAIL_NOT_PROVIDED': (u'E-postanı girmelisin', 'error'),
    'INVALID_EMAIL_ADDRESS': (u'Geçersiz e-posta adresi', 'error'),
    'PASSWORD_NOT_PROVIDED': (u'Parolanı girmelisin', 'error'),
    'PASSWORD_NOT_SET': (u'Parolan oluşturulmamış', 'error'),
    'PASSWORD_INVALID_LENGTH': (u'Parolan en az 6 karakter olmalı.', 'error'),
    'USER_DOES_NOT_EXIST': (u'Böyle bir kullanıcı bulamadık', 'error'),
    'INVALID_PASSWORD': (u'Hatalı parola', 'error'),
    'PASSWORDLESS_LOGIN_SUCCESSFUL': (u'Başarıyla giriş yaptın.', 'success'),
    'PASSWORD_RESET': (u'Parolan başarıyla sıfırlandı.', 'success'),
    'PASSWORD_IS_THE_SAME': (u'Yeni parolan, bir önceki parolandan farklı olmalı', 'error'),
    'PASSWORD_CHANGE': (u'Parolanı başarıyla değiştirdin.', 'success'),
    'LOGIN': (u'Bu sayfaya ulaşmak için lütfen giriş yapın.', 'info'),
    'REFRESH': (u'Bu sayfaya ulaşmak için lütfen yeniden giriş yapın.', 'info'),

}

security_config = {
    # reautanticate
    'DEFAULT_HTTP_AUTH_REALM': 'Login Required',
    'EMAIL_SUBJECT_REGISTER': u'Kaydın alındı',
    'EMAIL_SUBJECT_CONFIRM': u'Lütfen e-postanı onayla',
    'EMAIL_SUBJECT_PASSWORDLESS': u'Giriş yönlendirmesi',
    'EMAIL_SUBJECT_PASSWORD_NOTICE': u'Parolan sıfırlandı',
    'EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE': u'Parolan değiştirildi',
    'EMAIL_SUBJECT_PASSWORD_RESET': u'Parola sıfırlama',
}
