from src.config import *
from src.utils import *

# import required by pytest: User must know Reservation
# from src.model.user import *

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    #id: Mapped[UUID] = db.Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)    
    # we come back do "int" at reservation id because we can identify easily the reservation number
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = db.relationship(
        back_populates="reservations",
        foreign_keys=[user_id])
    room_id: Mapped[int] = mapped_column(db.ForeignKey("rooms.id"), nullable=False)
    room: Mapped["Room"] = db.relationship(back_populates="reservations")
    
    date: Mapped[date] = mapped_column(db.Date, default=datetime.now, nullable=False)
    start_time: Mapped[time] = mapped_column(db.Time, default=current_time(), nullable=False)
    end_time: Mapped[time] = mapped_column(db.Time, default=current_time(), nullable=False)
    purpose: Mapped[str] =  mapped_column(db.String(1024), nullable=False)
    
    active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    details: Mapped[str] =  mapped_column(db.String(1024), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now, nullable=False)
    
    canceler_user_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("users.id"), nullable=True)
    canceler_user: Mapped[Optional["User"]] = db.relationship(
        backref="cancelations",
        foreign_keys=[canceler_user_id])

    batch_id: Mapped[UUID] = db.Column(Uuid(as_uuid=True), nullable=True)
 
    def __repr__(self):
        return f'''Reservation(id={self.id}, 
        date={self.date}, active={self.active},
        Purpose={self.purpose})'''