from django.utils.translation import gettext_lazy as _


class MessageTxt:
    # 200 OK
    Success200 = _('عملیات مورد نظر با موفقیت انجام شد')
    SuccessDelete200 = _('حذف  با موفقیت انجام شد')

    PasswordChange200 = _("کلمه عبور با موفقیت تغییر کرد")
    # 400 Errors
    BadRequest400 = _('درخواست نامعتبر')
    UniqueUserName400 = _('نام کاربری تکراری است')
    # 401 Errors
    LoginFailNoUser401 = _('نام کاربری یا کلمه عبور اشتباه است')
    InputValidData = _('لطفا اطلاعات را به درستی وارد کنید')
    InvalidInput400 = _('ورودی نامعتبر')
    UniqueMobile = _('شماره موبایل تکراری است')
    WrongPassword400 = _('کلمه عبور اشتباه است')
    UserNotActive = _('کاربر غیر فعال است')

    # 403 Forbidden client error status
    DontHavePermission403 = _('اجازه دسترسی ندارید')

    # 404 Errors
    NotFound404 = _('موردی پیدا نشد')

    # chat
    InvalidChatMembers = _('کاربران انتخاب شده معتبر نیستند')
    ChatExist= _('چتی با این کاربران وجود دارد')
