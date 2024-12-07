from sqlalchemy.orm import Session
import models, schemas

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(filename=image.filename, filepath=image.filepath)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
