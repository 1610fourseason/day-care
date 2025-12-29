from app.models.facility_info_db import FacilityInfo


def get_info_date():
    return FacilityInfo.query.get(1)