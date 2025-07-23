from config import *

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)
    admin: Mapped[bool] = mapped_column(db.Boolean, default=False)
    active: Mapped[bool] = mapped_column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, "+\
                "password={self.password}, admin={self.admin}, active={self.active})>"