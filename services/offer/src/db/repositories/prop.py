from datetime import datetime

import models
import schemas
from db.repositories.base import BaseRepository



class PropRepository(BaseRepository):
    async def get_by_id(self, *, id: int) -> models.Prop:
        return self.db.query(models.Prop) \
            .filter(models.Prop.id == id) \
            .first()

    async def create(self, *,prop: schemas.PropCreate):
        db_prop = models.Prop(**prop.dict())
        self.db.add(db_prop)
        self.db.commit()
        self.db.refresh(db_prop)
        return db_prop

    async def update(self, *, prop: schemas.PropUpdate):
        values = prop.dict()
        values['updated_at'] = datetime.now()

        self.db.query(models.Prop) \
            .filter(models.Prop.id == prop.id) \
            .update(values, synchronize_session=False)
        self.db.commit()

        return await self.get_by_id(id=prop.id)