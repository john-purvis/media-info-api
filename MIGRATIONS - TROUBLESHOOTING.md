### Migration Baseline ###

Before attempting to run any migration (and after having dealt with Sqlite/PostgreSQL constraint issues), including creating the baseline:

     In your terminal, ensure that you are in the project's root folder `media-info-api`
     which is NOT `media_info_api`, and have run "`.venv\Scripts\Activate.ps1`" and see
     the prompt `(.venv) PS media-info-api>`.

To enable migrations:
```bash
   flask db init
```
This will create the `env.py` and `alembi.ini` files in the migrations folder.  These files are usually minimal and I
have always needed to edit the files or use files from another project and edit those.

Edit the alembic.ini file...

If you get a `script location error`, you will at least need to add `script_location = %(here)s` to the `[alembic]` section of the `alembic.ini` file.  If you still get an error, then overwrite the ini file you have with the one that is in the `examples/migrations` folder.  This file contains that line and more.

Edit the env.py:

In the section that reads:

     # add your model's MetaData object here
     # for 'autogenerate' support
     # from myapp import mymodel
     # target_metadata = mymodel.Base.metadata

You need to add the following lines:

     from media_info_api import create_app
     from media_info_api.extensions import media_db

     app = create_app("development")  # <- THIS makes it use recipes.config.DevelopmentConfig
     target_metadata = media_db.metadata

So that the file looks like:

     # add your model's MetaData object here
     # for 'autogenerate' support
     # from myapp import mymodel
     # target_metadata = mymodel.Base.metadata
     from media_info_api import create_app
     from media_info_api.extensions import media_db

     app = create_app("development")  # <- THIS makes it use recipes.config.DevelopmentConfig
     target_metadata = media_db.metadata

Then in both sections `run_migrations_offline` and `run_migrations_offline`, where `context.configure` is called you need to add:
```python
     render_as_batch=True, # <-- Needed for SQLite migrations to drop constraints
```
If you have issues after adding that line, use the eny.py file that is in `examples/migrations` folder.  This file contains the neccessary edits and works.  It creates the engine and connectable in a different way.

After the edits (or file replacement) run the following to create the baseline files:

```python
   alembic -c migrations/alembic.ini revision --autogenerate -m "database baseline"
```

Verify the files it creates in the versions folder.  Make sure that it only creates / updates the things that need updating, and MAKE SURE THAT ANY CONSTRAINTS THAT GET CREATED HAVE EXPLICIT NAMES, then run:

```python
   alembic -c migrations/alembic.ini upgrade head
```

This performs the migration and creates the baseline. It will create your database schema and add the alembic table to your database. It will add a record to the alembic table and and stamp it with a version which is used by later migrations.


   if any error occurs, delete ONLY the .py file in the versions folder
   for this migration, fix whateer is wrong, and try again

   if the error is REALLY severe or unrecoverable, you can delete the
   entire migrations folder and rerun the baseline for the the database
   THIS WILL DELETE EVERYTHING AND YOU WILL BE STARTING FROM THE BEGINNING
   at `flask db init`


If you DO NOT encounter errors and your database has been created with the correct schema, and the constraints have explicit names, then

     !!! CONGRATULATIONS !!!

At this point your migrations are setup and safe to move forward.

From this point forward the normal flow is:

1. make your model changes, then run
2. flask db migrate -m "reason for the changes"
     * the message should include a new feature reference or a help desk ticket number
     * check the upgrade / downgrade script created in versions
     * if the script looks okay and all constraints referenced have names, then run
3. flask db upgrade
