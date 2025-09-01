from src.config import *

class Room(db.Model):
    __tablename__ = 'rooms'
    
    #id: Mapped[UUID] = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    
    # Sala de Aula, Laboratório de Informática, Ginásio, Auditório, Laboratório de Química, 
    type: Mapped[str] = mapped_column(String(150), nullable=False, default="Sala de Aula")
    
    reservations: Mapped[List["Reservation"]] = db.relationship("Reservation", back_populates="room")
    
    def __repr__(self):
        return f"Room(id={self.id}, name={self.name}, active={self.active})"