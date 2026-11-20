### SQLite and PostgreSQL ###

FIRST, SQLite often leaves constraints unnamed by default, while PostgreSQL generates automatic names like tablename_columnname_fkey. Defining a MetaData(naming_convention=convention) forces SQLAlchemy to use identical, predictable names on both engines.

Alembic's batch mode (render_as_batch=True) requires explicit constraint names to recreate tables safely during migrations. This dictionary satisfies that requirement on SQLite while generating clean, standard ALTER TABLE commands on PostgreSQL.

Using explicit naming conventions across both databases keeps Alembic migrations reliable and prevents errors when altering or dropping constraints.

These naming conventions are normally defined in the extensions.py file.  This project already has them defined, but if not (or something has happenned to them), an example extensions.py can be found in this project's examples folder that does contain the naming conventions.

     One Small Caveat to Watch Out For

     • Check Constraints (ck): The "ck" rule uses %(constraint_name)s. Whenever a CheckConstraint is defined in the project's models, a name argument must explicitly be provided (for example, CheckConstraint('age > 0', name='positive_age')), otherwise SQLAlchemy will raise a KeyError during migration generation.

SECOND, enabling Alembic's batch mode can help with SQLite's ALTER TABLE and constraint limitations.  This COULD be done
in the extensions.py but is better done in the `_init_.py` where the app, the db, and the app context is available so that it can be checked and batch mode can be enabled for SQLite only while leaving any other database type alone.
```python
(_init_.py)

    with media_app.app_context():
        if media_db.engine.url.drivername == 'sqlite':
            # enable batch mode for sqlite to help solve
            # SQlite's ALTER TABLE and constraint limitations
            migrate.init_app(media_app, media_db, render_as_batch=True)
        else:
            migrate.init_app(media_app, media_db)
```
So, if you are running SQLAlchemy and SQLite in development but using SQLAlchemy and PostgreSQL in production, this configuration works nicely for both databases.
