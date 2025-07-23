from config import *

class Room(db.Model):
    __tablename__ = 'rooms'
    
    #id: Mapped[UUID] = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"Room(id={self.id}, name={self.name}, active={self.active})"