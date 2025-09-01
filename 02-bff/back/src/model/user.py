from src.config import *

# import required by pytest: Reservation must know User
# from src.model.reservation import *

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)
    admin: Mapped[bool] = mapped_column(db.Boolean, default=False)
    active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    
    reservations: Mapped[List["Reservation"]] = db.relationship(
        "Reservation", 
        back_populates="user", 
        foreign_keys="Reservation.user_id")
    
    '''
    cancelations: Mapped[List["Reservation"]] = db.relationship(
        "Reservation", 
        back_populates="canceler_user", 
        foreign_keys="Reservation.canceler_user_id")
    '''
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, "+\
                "password={self.password}, admin={self.admin}, active={self.active})>"
    
    def check_password(self, password):
        return self.password == password
        # return check_password_hash(self.password, password)
        # return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        
