from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "User"
    Id = Column(Integer, primary_key=True, index=True)
    FirstName  = Column(String)
    LastName = Column(String)
    Email = Column(String, unique=True)
    Password = Column(String)
    Country = Column(String)
    Status = Column(String)
    Type = Column(String)
    Date = Column(String)

    WritePkgSubscription = relationship('WritePkgSubscription', back_populates='User')
    ImagePkgSubscription = relationship('ImagePkgSubscription', back_populates='User')



class Category(Base):
    __tablename__ = "Category"
    Id = Column(Integer, primary_key=True, index=True)
    Name  = Column(String)
    Icon = Column(String)
    Status = Column(String)

    SubCategory = relationship('SubCategory', back_populates='Category')


class SubCategory(Base):
    __tablename__ = "SubCategory"
    Id = Column(Integer, primary_key=True, index=True)
    CategoryId = Column(Integer,ForeignKey("Category.Id"))
    Name  = Column(String)
    Summary = Column(String)
    Icon = Column(String)
    Prompt = Column(String)
    Status = Column(String)

    Category = relationship('Category', back_populates='SubCategory')
    WritePackages = relationship('WritePackages', back_populates='SubCategory')
    ImagePackages = relationship('ImagePackages', back_populates='SubCategory')



class WritePackages(Base):
    __tablename__ = "WritePackages"
    Id = Column(Integer, primary_key=True, index=True)
    Name  = Column(String)
    GeneratedCharacters = Column(Integer)
    SubCategoryId = Column(Integer, ForeignKey("SubCategory.Id"))
    WriteLanguage = Column(String)
    WriteTone = Column(String)
    Status = Column(String)
    IsTrail = Column(String)
    MonthlyPrice = Column(String)
    YearlyPrice = Column(String)

    SubCategory = relationship('SubCategory', back_populates='WritePackages')
    WritePkgSubscription = relationship('WritePkgSubscription', back_populates='WritePackages')



class ImagePackages(Base):
    __tablename__ = "ImagePackages"
    Id = Column(Integer, primary_key=True, index=True)
    Name  = Column(String)
    GeneratedImages = Column(Integer)
    SubCategoryId = Column(Integer, ForeignKey("SubCategory.Id"))
    Status = Column(String)
    IsTrail = Column(String)
    MonthlyPrice = Column(String)
    YearlyPrice = Column(String)

    SubCategory = relationship('SubCategory', back_populates='ImagePackages')
    ImagePkgSubscription = relationship('ImagePkgSubscription', back_populates='ImagePackages')



class WritePkgSubscription(Base):
    __tablename__ = "WritePkgSubscription"
    Id = Column (Integer, primary_key=True, index=True)
    PackageId = Column (Integer, ForeignKey('WritePackages.Id'))
    UserId = Column (Integer, ForeignKey('User.Id'))
    Status = Column (String)
    TotalCharacters = Column (Integer)
    RemainingCharacters = Column (Integer)

    WritePackages = relationship('WritePackages', back_populates='WritePkgSubscription')
    User = relationship('User', back_populates='WritePkgSubscription')
    WritePkgOrder = relationship('WritePkgOrder', back_populates='WritePkgSubscription')



class ImagePkgSubscription(Base):
    __tablename__ = "ImagePkgSubscription"
    Id = Column (Integer, primary_key=True, index=True)
    PackageId = Column (Integer, ForeignKey('ImagePackages.Id'))
    UserId = Column (Integer, ForeignKey('User.Id'))
    Status = Column (String)
    TotalImages = Column (Integer)
    RemainingImages = Column (Integer)

    ImagePackages = relationship('ImagePackages', back_populates='ImagePkgSubscription')
    User = relationship('User', back_populates='ImagePkgSubscription')
    ImagePkgOrder = relationship('ImagePkgOrder', back_populates='ImagePkgSubscription')


class WritePkgOrder(Base):
    __tablename__ = "WritePkgOrder"
    Id = Column(Integer, primary_key=True, index=True)
    SubscriptionId = Column(Integer, ForeignKey('WritePkgSubscription.Id'))
    Amount = Column (Float)
    TransactionId = Column (String)
    Status = Column (String)
    StartDate = Column (String)
    EndDate = Column (String)

    WritePkgSubscription = relationship('WritePkgSubscription', back_populates='WritePkgOrder')


class ImagePkgOrder(Base):
    __tablename__ = "ImagePkgOrder"
    Id = Column(Integer, primary_key=True, index=True)
    SubscriptionId = Column(Integer, ForeignKey('ImagePkgSubscription.Id'))
    Amount = Column (Float)
    TransactionId = Column (String)
    Status = Column (String)
    StartDate = Column (String)
    EndDate = Column (String)

    ImagePkgSubscription = relationship('ImagePkgSubscription', back_populates='ImagePkgOrder')



    

    