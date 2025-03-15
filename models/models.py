import uuid
from typing import Any, List, Optional

from sqlalchemy import BINARY, BigInteger, Column, Date, Double, Enum, ForeignKeyConstraint, Index, Integer, JSON, \
    String, Table, Text, text, ForeignKey
from sqlalchemy.dialects.mysql import BIT, DATETIME, MEDIUMTEXT, TINYTEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (
        ForeignKeyConstraint(['news_post_id'], ['news_post.id'], name='FK21p8hxq6osw1oiusy1o88oo76'),
        Index('FK21p8hxq6osw1oiusy1o88oo76', 'news_post_id'),
        Index('UKacatplu22q5d1andql2jbvjy7', 'code', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    code: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    position: Mapped[Optional[int]] = mapped_column(Integer)
    redirect_url: Mapped[Optional[str]] = mapped_column(String(255))
    news_post_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    news_post: Mapped[Optional['NewsPost']] = relationship('NewsPost', foreign_keys=[news_post_id], back_populates='category')
    news_post_: Mapped[List['NewsPost']] = relationship('NewsPost', foreign_keys='[NewsPost.category_id]', back_populates='category_')
    category_translation: Mapped[List['CategoryTranslation']] = relationship('CategoryTranslation', back_populates='category')
    rss_feed: Mapped[List['RssFeed']] = relationship('RssFeed', back_populates='category')
    tag: Mapped[List['Tag']] = relationship('Tag', back_populates='category')


t_category_seq = Table(
    'category_seq', Base.metadata,
    Column('next_val', BigInteger)
)


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    capital_en: Mapped[Optional[str]] = mapped_column(String(255))
    cca2: Mapped[Optional[str]] = mapped_column(String(255))
    cca3: Mapped[Optional[str]] = mapped_column(String(255))
    ccn3: Mapped[Optional[str]] = mapped_column(String(255))
    name_en: Mapped[Optional[str]] = mapped_column(String(255))
    region: Mapped[Optional[str]] = mapped_column(Enum('AFRICA', 'ALL', 'ASIA', 'EUROPE', 'MIDDLE_EAST', 'NORTH_AMERICA', 'OCEANIA', 'SOUTH_AMERICA'))
    region_en: Mapped[Optional[str]] = mapped_column(String(255))
    subregion_en: Mapped[Optional[str]] = mapped_column(String(255))

    stock_index: Mapped[List['StockIndex']] = relationship('StockIndex', secondary='country_stock_index', back_populates='country')
    news_post: Mapped[List['NewsPost']] = relationship('NewsPost', back_populates='country')
    country_translation: Mapped[List['CountryTranslation']] = relationship('CountryTranslation', back_populates='country')
    user: Mapped[List['User']] = relationship('User', back_populates='country')


t_country_seq = Table(
    'country_seq', Base.metadata,
    Column('next_val', BigInteger)
)

class NewsPostImage(Base):
    __tablename__ = "news_post_images"

    id: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    news_post_id: Mapped[int] = mapped_column(ForeignKey("news_post.id", ondelete="CASCADE"), nullable=False)
    images: Mapped[str] = mapped_column(String(1000), nullable=True)
    original_image_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    s3_image_base_url: Mapped[str] = mapped_column(String(1000), nullable=True)

    news_post: Mapped["NewsPost"] = relationship("NewsPost", back_populates="images")

class NewsPostVideo(Base):
    __tablename__ = "news_post_videos"

    news_post_id: Mapped[int] = mapped_column(ForeignKey("news_post.id", ondelete="CASCADE"), primary_key=True)
    videos: Mapped[str] = mapped_column(String(1000), nullable=True)

    news_post: Mapped["NewsPost"] = relationship("NewsPost", back_populates="videos")

class NewsPost(Base):
    __tablename__ = 'news_post'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['category.id'], name='FKcfnf04gs456gli02b4gdal6yk'),
        ForeignKeyConstraint(['country_id'], ['country.id'], name='FK22ro3yjlttnwau7v3y8aaicw6'),
        ForeignKeyConstraint(['source_id'], ['source.id'], name='FKc3e6qksgcy8fvbpgypnssedr8'),
        ForeignKeyConstraint(['user_id'], ['user.id'], name='FKtl98ql475lq5th89rxywif4bd'),
        Index('FK22ro3yjlttnwau7v3y8aaicw6', 'country_id'),
        Index('FKc3e6qksgcy8fvbpgypnssedr8', 'source_id'),
        Index('FKcfnf04gs456gli02b4gdal6yk', 'category_id'),
        Index('FKtl98ql475lq5th89rxywif4bd', 'user_id'),
        Index('fulltext_idx_title_content', 'title', 'content'),
        Index('idx_news_deleted_id_likes', 'deleted', 'id', 'likes'),
        Index('idx_news_language', 'language'),
        Index('title', 'title', 'content')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    content: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6), default=lambda: datetime.datetime.now())
    creator: Mapped[Optional[str]] = mapped_column(String(1000))
    description: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(255))
    likes: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    link: Mapped[Optional[str]] = mapped_column(String(1000))
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    remote_id: Mapped[Optional[str]] = mapped_column(String(1000))
    title: Mapped[Optional[str]] = mapped_column(String(5000))
    images_json: Mapped[Optional[str]] = mapped_column(JSON)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    world_region: Mapped[Optional[str]] = mapped_column(Enum('AFRICA', 'ALL', 'ASIA', 'EUROPE', 'MIDDLE_EAST', 'NORTH_AMERICA', 'OCEANIA', 'SOUTH_AMERICA'))
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    country_id: Mapped[Optional[int]] = mapped_column(Integer)
    source_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    formatting: Mapped[Optional[str]] = mapped_column(Enum('MARKDOWN', 'TEXT'))
    sub_category: Mapped[Optional[str]] = mapped_column(Enum('BADMINTON', 'BASKETBALL', 'CRICKET', 'F1_RACING', 'FOOTBALL', 'HOCKEY', 'TENNIS', 'VOLLEYBALL', 'BASEBALL', 'GOLF', 'UNITED_STATES', 'INDIA', 'CHINA', 'RUSSIA', 'EUROPE', 'ASIA', 'AFRICA', 'ENTERTAINMENT', 'FOOD', 'LIFESTYLE', 'ENVIRONMENT', 'HEALTH', 'FITNESS', 'MENTAL_HEALTH', 'NUTRITION', 'SCIENCE', 'GADGETS', 'INTERNET', 'SOFTWARE', 'MOBILE', 'DESKTOP', 'ARTIFICIAL_INTELLIGENCE', 'BUSINESS', 'MARKET', 'ECONOMY', 'REAL_ESTATE', 'TOURISM'))
    type: Mapped[Optional[str]] = mapped_column(Enum('ORGANISATION_POST', 'USER_POST'))

    category: Mapped[List['Category']] = relationship('Category', foreign_keys='[Category.news_post_id]', back_populates='news_post')
    category_: Mapped[Optional['Category']] = relationship('Category', foreign_keys=[category_id], back_populates='news_post_')
    country: Mapped[Optional['Country']] = relationship('Country', back_populates='news_post')
    source: Mapped[Optional['Source']] = relationship('Source', back_populates='news_post')
    user: Mapped[Optional['User']] = relationship('User', back_populates='news_post')
    tag: Mapped[List['Tag']] = relationship('Tag', secondary='news_post_tag', back_populates='news_post')
    user_: Mapped[List['User']] = relationship('User', secondary='user_bookmarks', back_populates='news')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='news_post')

    images: Mapped[list[NewsPostImage]] = relationship("NewsPostImage", back_populates="news_post",
                                                       cascade="all, delete-orphan")
    videos: Mapped[list[NewsPostVideo]] = relationship("NewsPostVideo", back_populates="news_post",
                                                       cascade="all, delete-orphan")




class Source(Base):
    __tablename__ = 'source'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    code: Mapped[Optional[str]] = mapped_column(String(255))
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(255))

    news_post: Mapped[List['NewsPost']] = relationship('NewsPost', back_populates='source')
    user: Mapped[List['User']] = relationship('User', secondary='user_sources', back_populates='source')


class StockIndex(Base):
    __tablename__ = 'stock_index'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    market: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    symbol: Mapped[Optional[str]] = mapped_column(String(255))

    country: Mapped[List['Country']] = relationship('Country', secondary='country_stock_index', back_populates='stock_index')
    stock_index_daily_data: Mapped[List['StockIndexDailyData']] = relationship('StockIndexDailyData', back_populates='stock_index')


t_stock_index_daily_data_seq = Table(
    'stock_index_daily_data_seq', Base.metadata,
    Column('next_val', BigInteger)
)


t_stock_index_seq = Table(
    'stock_index_seq', Base.metadata,
    Column('next_val', BigInteger)
)


class Test(Base):
    __tablename__ = 'test'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    node_schema: Mapped[Optional[dict]] = mapped_column(JSON)


t_user_seq = Table(
    'user_seq', Base.metadata,
    Column('next_val', BigInteger)
)


class CategoryTranslation(Base):
    __tablename__ = 'category_translation'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['category.id'], name='FKo2l26f7i3uncfy08y5196hrxd'),
        Index('FKo2l26f7i3uncfy08y5196hrxd', 'category_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    language: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[int]] = mapped_column(Integer)

    category: Mapped[Optional['Category']] = relationship('Category', back_populates='category_translation')


t_country_stock_index = Table(
    'country_stock_index', Base.metadata,
    Column('country_id', Integer, nullable=False),
    Column('stock_index_id', Integer, nullable=False),
    ForeignKeyConstraint(['country_id'], ['country.id'], name='FKdunekersyc1fx42niydfdeb3u'),
    ForeignKeyConstraint(['stock_index_id'], ['stock_index.id'], name='FKp8j8wy8hbfgudm3acky5psh65'),
    Index('FKdunekersyc1fx42niydfdeb3u', 'country_id'),
    Index('FKp8j8wy8hbfgudm3acky5psh65', 'stock_index_id')
)


class CountryTranslation(Base):
    __tablename__ = 'country_translation'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['country.id'], name='FKpqmitn8i8ghcttxskjj1dy7ms'),
        Index('FKpqmitn8i8ghcttxskjj1dy7ms', 'country_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    capital: Mapped[Optional[str]] = mapped_column(String(255))
    language: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    region: Mapped[Optional[str]] = mapped_column(String(255))
    subregion: Mapped[Optional[str]] = mapped_column(String(255))
    country_id: Mapped[Optional[int]] = mapped_column(Integer)

    country: Mapped[Optional['Country']] = relationship('Country', back_populates='country_translation')




class RssFeed(Base):
    __tablename__ = 'rss_feed'
    __table_args__ = (
        ForeignKeyConstraint(['category_code'], ['category.code'], name='FKkyhveo81bc5f91eb3itkc6str'),
        Index('FKkyhveo81bc5f91eb3itkc6str', 'category_code')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    category_code: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    creator: Mapped[Optional[str]] = mapped_column(String(1000))
    description: Mapped[Optional[str]] = mapped_column(Text)
    guid: Mapped[Optional[str]] = mapped_column(String(1000))
    language: Mapped[Optional[str]] = mapped_column(String(255))
    link: Mapped[Optional[str]] = mapped_column(String(1000))
    media_url: Mapped[Optional[str]] = mapped_column(String(1000))
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    title: Mapped[Optional[str]] = mapped_column(String(5000))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))

    category: Mapped['Category'] = relationship('Category', back_populates='rss_feed')


class StockIndexDailyData(Base):
    __tablename__ = 'stock_index_daily_data'
    __table_args__ = (
        ForeignKeyConstraint(['stock_index_id'], ['stock_index.id'], name='FK3v85xxd4k8o9s8d27t40aoamu'),
        Index('FK3v85xxd4k8o9s8d27t40aoamu', 'stock_index_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    change_percent: Mapped[Optional[decimal.Decimal]] = mapped_column(Double(asdecimal=True))
    close_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Double(asdecimal=True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    high_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Double(asdecimal=True))
    low_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Double(asdecimal=True))
    open_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Double(asdecimal=True))
    stock_index_id: Mapped[Optional[int]] = mapped_column(Integer)

    stock_index: Mapped[Optional['StockIndex']] = relationship('StockIndex', back_populates='stock_index_daily_data')


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        ForeignKeyConstraint(['category_code'], ['category.code'], name='FK1febqpc7xqk0ac20g31hq3wjh'),
        Index('FK1febqpc7xqk0ac20g31hq3wjh', 'category_code')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    code: Mapped[Optional[str]] = mapped_column(String(255))
    category_code: Mapped[Optional[str]] = mapped_column(String(255))

    news_post: Mapped[List['NewsPost']] = relationship('NewsPost', secondary='news_post_tag', back_populates='tag')
    category: Mapped[Optional['Category']] = relationship('Category', back_populates='tag')
    user: Mapped[List['User']] = relationship('User', secondary='user_interest', back_populates='tag')
    tag_translation: Mapped[List['TagTranslation']] = relationship('TagTranslation', back_populates='tag')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['country.id'], name='FKge8lxibk9q3wf206s600otk61'),
        Index('FKge8lxibk9q3wf206s600otk61', 'country_id'),
        Index('UKob8kqyqqgmefl0aco34akdtpe', 'email', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(String(255))
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    followers_count: Mapped[Optional[int]] = mapped_column(Integer)
    following_count: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[str]] = mapped_column(Enum('FEMALE', 'MALE', 'OTHER'))
    is_new_user: Mapped[Optional[Any]] = mapped_column(BIT(1))
    language: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    posts_count: Mapped[Optional[int]] = mapped_column(Integer)
    role: Mapped[Optional[str]] = mapped_column(String(255))
    username: Mapped[Optional[str]] = mapped_column(String(255))
    country_id: Mapped[Optional[int]] = mapped_column(Integer)
    profile_pic_url: Mapped[Optional[str]] = mapped_column(String(255))

    news_post: Mapped[List['NewsPost']] = relationship('NewsPost', back_populates='user')
    news: Mapped[List['NewsPost']] = relationship('NewsPost', secondary='user_bookmarks', back_populates='user_')
    source: Mapped[List['Source']] = relationship('Source', secondary='user_sources', back_populates='user')
    tag: Mapped[List['Tag']] = relationship('Tag', secondary='user_interest', back_populates='user')
    country: Mapped[Optional['Country']] = relationship('Country', back_populates='user')
    user: Mapped[List['User']] = relationship('User', secondary='user_following', primaryjoin=lambda: User.id == t_user_following.c.following_id, secondaryjoin=lambda: User.id == t_user_following.c.user_id, back_populates='following')
    following: Mapped[List['User']] = relationship('User', secondary='user_following', primaryjoin=lambda: User.id == t_user_following.c.user_id, secondaryjoin=lambda: User.id == t_user_following.c.following_id, back_populates='user')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='user')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['news_post_id'], ['news_post.id'], name='FKedt56d8kc0jwmr59v0g5gfsm'),
        ForeignKeyConstraint(['user_id'], ['user.id'], name='FK8kcum44fvpupyw6f5baccx25c'),
        Index('FK8kcum44fvpupyw6f5baccx25c', 'user_id'),
        Index('FKedt56d8kc0jwmr59v0g5gfsm', 'news_post_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    likes: Mapped[int] = mapped_column(Integer)
    deleted: Mapped[Any] = mapped_column(BIT(1), comment='Soft-delete indicator')
    content: Mapped[Optional[str]] = mapped_column(TINYTEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    news_post_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    news_post: Mapped[Optional['NewsPost']] = relationship('NewsPost', back_populates='comment')
    user: Mapped[Optional['User']] = relationship('User', back_populates='comment')


t_news_post_tag = Table(
    'news_post_tag', Base.metadata,
    Column('news_post_id', BigInteger, nullable=False),
    Column('tag_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['news_post_id'], ['news_post.id'], name='FKhic3de2g4frf024ex5p78gcvr'),
    ForeignKeyConstraint(['tag_id'], ['tag.id'], name='FK8acwyv4g2n2okpis3h87l0l1d'),
    Index('FK8acwyv4g2n2okpis3h87l0l1d', 'tag_id'),
    Index('FKhic3de2g4frf024ex5p78gcvr', 'news_post_id')
)


class TagTranslation(Base):
    __tablename__ = 'tag_translation'
    __table_args__ = (
        ForeignKeyConstraint(['tag_id'], ['tag.id'], name='FK36i52exo8bxh7vy9o7iohuvci'),
        Index('FK36i52exo8bxh7vy9o7iohuvci', 'tag_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    language_code: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    tag_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    tag: Mapped[Optional['Tag']] = relationship('Tag', back_populates='tag_translation')


t_user_bookmarks = Table(
    'user_bookmarks', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('news_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['news_id'], ['news_post.id'], name='FKegogshmx4t09hjq4bjilgty75'),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='FKa58034qcx0kqh8v7x95kgys9m'),
    Index('FKa58034qcx0kqh8v7x95kgys9m', 'user_id'),
    Index('FKegogshmx4t09hjq4bjilgty75', 'news_id')
)


t_user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('following_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['following_id'], ['user.id'], name='FKj0avh5q4feap4g0rkus640u4d'),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='FKn4mj5gtsm47fikwbu41b6wi9k'),
    Index('FKj0avh5q4feap4g0rkus640u4d', 'following_id'),
    Index('FKn4mj5gtsm47fikwbu41b6wi9k', 'user_id')
)


t_user_interest = Table(
    'user_interest', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('tag_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['tag_id'], ['tag.id'], name='FKhx66crya257ijivo6496qy8mj'),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='FKdi9smphhv09dottb2sc1j3k64'),
    Index('FKdi9smphhv09dottb2sc1j3k64', 'user_id'),
    Index('FKhx66crya257ijivo6496qy8mj', 'tag_id')
)


t_user_sources = Table(
    'user_sources', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('source_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['source_id'], ['source.id'], name='FK93r1lnu68kwkhh71b0rarfw2b'),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='FKto8geogm2r2iulpmp1wl87ar6'),
    Index('FK93r1lnu68kwkhh71b0rarfw2b', 'source_id'),
    Index('FKto8geogm2r2iulpmp1wl87ar6', 'user_id')
)
