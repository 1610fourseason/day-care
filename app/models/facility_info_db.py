from ..extensions import db


class FacilityInfo(db.Model):
    __tablename__ = 'facility_info'

    id = db.Column(db.Integer, primary_key=True)
    # 基本情報
    name = db.Column(db.String(100), nullable=False)
    facility_type = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    accepted_age = db.Column(db.String(100), nullable=True)
    # 住所 
    postal_code = db.Column(db.String(8), nullable=True)   
    address = db.Column(db.String(255), nullable=True)     

    # 開所時間
    hours_weekday = db.Column(db.String(50), nullable=True)
    hours_saturday = db.Column(db.String(50), nullable=True)
    hours_holiday = db.Column(db.String(50), nullable=True)
    # 職種別職員数
    staff_teacher = db.Column(db.Integer, default=0)  # 保育士/幼稚園教諭
    staff_support = db.Column(db.Integer, default=0)  # 保育従事者/保育補助
    staff_nutrition = db.Column(db.Integer, default=0) # 栄養士/管理栄養士
    staff_cook = db.Column(db.Integer, default=0)      # 調理師
    staff_nurse = db.Column(db.Integer, default=0)     # 看護師
    staff_office = db.Column(db.Integer, default=0)  # その他

    childcare_fee_text = db.Column(db.String(100), nullable=True)
