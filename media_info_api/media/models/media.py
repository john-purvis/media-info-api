# media_info_api/media/models/media.py


from media_info_api.extensions import media_db


class Media(media_db.Model):
    __tablename__ = "media"
    id = media_db.Column(media_db.Integer, primary_key=True)
    catalog_id = media_db.Column(media_db.Integer, nullable=True, unique=True) # must be nullable for media create and catalog create
    # user_id = media_db.Column(media_db.Integer, nullable=False)
    # Updated with ForeignKey pointing to users.id
    user_id = media_db.Column(
        media_db.Integer, media_db.ForeignKey("users.id"), nullable=False
    )
    type = media_db.Column(media_db.Text, nullable=False)                       # movie, tv_series, tv_episode
    title = media_db.Column(media_db.Text, nullable=False, unique=True)
    year = media_db.Column(media_db.Integer, nullable=True)
    duration = media_db.Column(media_db.Integer, nullable=True)                 # duration in seconds
    certificate = media_db.Column(media_db.Text, nullable=True)                 # "R", PG-13, TV-MA, etc
    genres = media_db.Column(media_db.Text, nullable=True)                      # comma delimited list of genres "Action", "Sci-Fi", etc
    description = media_db.Column(media_db.Text, nullable=True)                 # short description or plot
    imdb_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # IMDB id
    tmdb_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # TMDB id
    wiki_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # Wikipedia id

    # Optional: access the owner via media.user
    user = media_db.relationship("User", back_populates="media_items")
