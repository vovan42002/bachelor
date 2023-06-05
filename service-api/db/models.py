import uuid

from sqlalchemy import Column, ForeignKey, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    controllers = relationship(
        "Controller", passive_deletes=True, back_populates="user"
    )


class Controller(Base):
    __tablename__ = "controllers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    force_enable = Column(Boolean, nullable=False)
    start_time = Column(Integer, nullable=True)
    end_time = Column(Integer, nullable=True)
    repeat = Column(Boolean, nullable=False)
    status = Column(Boolean, nullable=False)
    last_changed = Column(Integer, nullable=False)
    user = relationship("User", back_populates="controllers")
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    sensors = relationship("Sensor", passive_deletes=True, back_populates="controller")


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    actual = Column(Integer, nullable=True)
    expected = Column(Integer, nullable=True)
    last_changed = Column(Integer, nullable=False)

    controller = relationship("Controller", back_populates="sensors")
    controller_id = Column(Integer, ForeignKey("controllers.id", ondelete="CASCADE"))
