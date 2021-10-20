
import schemas
import models
from database import Session



async def property_added(db: Session, prop: schemas.PropertyCreate):
    user_prop = models.UserProperty(
        prop_id = prop.id,
        user_id = prop.user_id,
        price = prop.price,
        transfer_date = prop.updated_at or prop.created_at
    )
    db.add(user_prop)
    db.commit()
    db.refresh(user_prop)
    return user_prop


async def property_updated(db: Session, prop: schemas.PropertyUpdate):
    print('------ > updateing', prop)
    #TODO: transfer date can have wrong value.
    values = {
        'prop_id': prop.id,
        'user_id': prop.user_id,
        'price': prop.price,
        'transfer_date': prop.updated_at or prop.created_at
    }
    schemas.PropertyUpdate.parse_obj(values)

    update_count = db.query(models.UserProperty) \
        .filter(
            models.UserProperty.prop_id == prop.id,
            models.UserProperty.user_id == prop.user_id) \
        .update(values, synchronize_session=False)
    db.commit()
    return update_count


# def update_property(db: Session, prop: schemas.PropertyUpdate):
#     values = prop.dict()
#     values['updated_at'] = datetime.now()
#     update_count = db.query(models.Property) \
#         .filter(models.Property.id == prop.id) \
#         .update(values, synchronize_session=False)
#     db.commit()
#     return update_count

