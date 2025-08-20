import csv
from datetime import datetime

from sqlalchemy import select, inspect, insert

from path_utils.utils import get_project_root
from podcast.adapters.orm import mapper_registry

def test_database_populate_inspect_table_names(database_engine):
    """Test that all required tables are created in the database."""
    inspector = inspect(database_engine)
    expected_tables = ['authors', 'podcasts', 'categories', 'episodes', 'podcasts_categories', 'users', 'reviews', 'playlists', 'playlists_episodes']
    actual_tables = inspector.get_table_names()
    assert set(expected_tables) == set(actual_tables)

def test_database_populate_select_all_authors(database_engine):
    """Test that the authors table is populated correctly."""
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])
        result = connection.execute(select_statement)

        all_authors = []
        all_author_id = []
        for row in result:
            all_authors.append(row[1])

        assert all_authors == ['MISSING: No Author provided', 'D Hour Radio Network', 'Brian Denny', 'Radio Popolare', 'Tallin Country Church', 'Eric Toohey', 'msafoschnik', 'Janelle Vecchio and Phil Vecchio']


def test_database_populate_select_all_podcasts(database_engine):
    """Test that the podcasts table is populated correctly."""
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])
        result = connection.execute(select_statement)

        all_podcasts = []
        for row in result:
            all_podcasts.append(row[2])

        assert all_podcasts == ["D-Hour Radio Network","Brian Denny Radio","Onde Road - Radio Popolare","Tallin Messages","Bethel Presbyterian Church (EPC) Sermons","Mike Safo","The Mandarian Orange Show"]

def test_database_populate_select_all_categories(database_engine):
    """Test that the categories table is populated correctly."""
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])
        result = connection.execute(select_statement)

        all_categories = []
        for row in result:
            all_categories.append(row[1])

        assert all_categories == ['Society & Culture', 'Personal Journals', 'Professional', 'News & Politics', 'Sports & Recreation', 'Comedy', 'Religion & Spirituality', 'Christianity', 'Amateur']

def test_database_populate_select_all_episodes(database_engine):
    """Test that the episodes table is populated correctly."""
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append((row[0], row[2]))

        assert len(all_episodes) == 4
        assert all_episodes[0] == (1, 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3')  # Replace with expected episode title
        assert all_episodes[1] == (2, 'Finding yourself in the character by justifying your actions')
        assert all_episodes[2] == (3, 'Episode 182 - Lyrically Weak')
        assert all_episodes[3] == (4, 'Week 16 Day 5')

#helper method to populate the table
def populate_users_from_csv(database_engine, user_file=get_project_root() / "tests" / "data"/ "users.csv"):
    """Populate the users table using data from a CSV file."""
    with open(user_file, mode='r') as file:
        reader = csv.DictReader(file)
        users = []
        for row in reader:
            users.append({
                'id': row['id'],
                'user_name': row['username'],
                'password': row['password']
            })
    # Insert the users into the database
    with database_engine.connect() as connection:
        users_table = mapper_registry.metadata.tables['users']
        insert_statement = insert(users_table)
        connection.execute(insert_statement, users)
        connection.commit()


def test_database_populate_select_all_users(database_engine):
    """Test that the users table is populated correctly."""
    populate_users_from_csv(database_engine, user_file=get_project_root() / "tests" / "data"/ "users.csv")
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[name_of_users_table])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row[1])
        assert all_users == ['thorke', 'fmercury']


#helper method to populate the table
def populate_reviews_from_csv(database_engine, review_file=get_project_root() / "tests" / "data" / "reviews.csv"):
    """Populate the reviews table using data from a CSV file."""
    with open(review_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reviews = []
        for row in reader:
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
            reviews.append({
                'id': int(row['id']),
                'podcast_id': int(row['podcast_id']),
                'episode_id': int(row['episode_id']) if row['episode_id'] else None,
                'user_id': int(row['user_id']),
                'rating': int(row['rating']),
                'content': row['content'],
                'timestamp':timestamp
            })

    # Insert the reviews into the database
    with database_engine.connect() as connection:
        reviews_table = mapper_registry.metadata.tables['reviews']
        insert_statement = insert(reviews_table)
        connection.execute(insert_statement, reviews)
        connection.commit()

def test_database_populate_select_all_reviews(database_engine):
    """Test that the reviews table is populated correctly."""
    populate_reviews_from_csv(database_engine, review_file=get_project_root() / "tests" / "data" / "reviews.csv")
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    name_of_reviews_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # Query for records in the reviews table
        select_statement = select(mapper_registry.metadata.tables[name_of_reviews_table])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row[0], row[2], row[1], row[3], row[4], row[5], row[6]))

        expected_reviews = [
            (1, 1, 101, 5, 5, 'This episode was amazing, very insightful!', datetime(2024, 10, 10, 12, 30, 0)),
            (2, 2, 102, 3, 4, 'I really enjoyed this podcast, but it could have had more details.',
             datetime(2024, 10, 9, 14, 0, 0)),
            (3, 1, 103, 5, 3, 'The podcast was good, but I expected more from the episode.',
             datetime(2024, 10, 8, 9, 15, 0)),
            (4, 3, 104, 6, 5, 'This was exactly what I needed to hear. Great job!', datetime(2024, 10, 7, 18, 45, 0)),
            (5, 4, 105, 3, 2, "Unfortunately, this episode didn't live up to my expectations.",
             datetime(2024, 10, 6, 20, 10, 0))
        ]
        assert all_reviews == expected_reviews

#helper method to help populate the playlist
def populate_playlists_from_csv(database_engine, playlist_file=get_project_root() / "tests" / "data" / "playlist.csv"):
    """Populate the playlists table using data from a CSV file."""
    with open(playlist_file, mode='r') as file:
        reader = csv.DictReader(file)
        playlists = []
        playlist_episodes = []

        for row in reader:
            # Add playlist data (without episodes yet)
            playlists.append({
                'id': int(row['playlist_id']),
                'owner_id': int(row['owner_id']),
                'title': row['title']
            })

            episode_ids = row['episode_ids'].split(',')
            for episode_id in episode_ids:
                playlist_episodes.append({
                    'playlist_id': int(row['playlist_id']),
                    'episode_id': int(episode_id)
                })

    # Insert playlist data into the playlists table
    with database_engine.connect() as connection:
        playlists_table = mapper_registry.metadata.tables['playlists']
        insert_statement = insert(playlists_table)
        connection.execute(insert_statement, playlists)
        connection.commit()

    # Insert playlist-episode associations into the association table
    with database_engine.connect() as connection:
        playlist_episodes_table = mapper_registry.metadata.tables['playlists_episodes']
        insert_statement = insert(playlist_episodes_table)
        connection.execute(insert_statement, playlist_episodes)
        connection.commit()


def test_database_populate_select_all_playlists(database_engine):
    """Test that the playlists table is populated correctly with all variables."""
    #populate the database
    populate_playlists_from_csv(database_engine, playlist_file=get_project_root() / "tests" / "data" / "playlist.csv")

    inspector = inspect(database_engine)

    name_of_playlists_table = inspector.get_table_names()[3]
    name_of_playlist_episodes_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # Query for records in the playlists table
        select_statement = select(mapper_registry.metadata.tables[name_of_playlists_table])
        result = connection.execute(select_statement)

        all_playlists = []
        for row in result:
            playlist_data = {
                'id': row[0],         # row[0] corresponds to 'id'
                'owner_id': row[1],    # row[1] corresponds to 'owner_id'
                'title': row[2],       # row[2] corresponds to 'title'
            }

            # Fetch the associated episodes from the playlist_episodes table
            select_episodes = select(mapper_registry.metadata.tables[name_of_playlist_episodes_table]).where(
                mapper_registry.metadata.tables[name_of_playlist_episodes_table].c.playlist_id == row[0])  # Using row[0] for 'id'
            episode_result = connection.execute(select_episodes)

            # Collect all associated episode_ids
            episode_ids = [episode_row[2] for episode_row in episode_result]
            playlist_data['episode_ids'] = episode_ids
            all_playlists.append(playlist_data)

        # Expected values for all playlists
        expected_playlists = [
            {
                'id': 1,
                'owner_id': 101,
                'title': "My Favorite Episodes",
                'episode_ids': [1, 2, 3],
            },
            {
                'id': 2,
                'owner_id': 102,
                'title': "Tech Talks",
                'episode_ids': [4, 5],
            },
            {
                'id': 3,
                'owner_id': 103,
                'title': "Inspiration",
                'episode_ids': [6],
            }
        ]

        # Check if the playlists match the expected values
        assert all_playlists == expected_playlists