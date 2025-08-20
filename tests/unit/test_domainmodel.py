import pytest

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from datetime import datetime
import os
import random

def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_podcast_2(my_author):
    return Podcast(101, my_author, "I am super mario!")


@pytest.fixture
def my_podcast_3(my_author):
    return Podcast(99, my_author, "And I'm Luigi!")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast)


@pytest.fixture
def my_review(my_user, my_podcast, my_episode):
    return Review(1, my_user, 5.0, "I can't believe they got Joe Biden on.", my_podcast, my_episode)


@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user)

@pytest.fixture
def csv_reader():
    return CSVDataReader()


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Review classes.


def test_episode_initialisation(my_episode, my_podcast):
    assert my_episode.id == 1
    assert my_episode.podcast.id == 100
    assert repr(my_episode) == "<Episode 1: 'Untitled' from podcast 100>"

    episode2 = Episode(2, my_podcast, "To be or not to be ")
    with pytest.raises(ValueError):
        episode3 = Episode(-2, my_podcast)

    episode4 = Episode(4, my_podcast, "That is the question", "https://audiojungle.com",
                       54,"Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, ",
                       datetime(2004, 5, 6))
    assert repr(episode2) == "<Episode 2: 'To be or not to be' from podcast 100>"
    assert repr(episode4) == "<Episode 4: 'That is the question' from podcast 100>"


def test_episode_set_title(my_episode):
    assert my_episode.title == "Untitled"
    my_episode.title = "Saturn "
    assert my_episode.title == "Saturn"
    with pytest.raises(ValueError):
        my_episode.title = ""
    with pytest.raises(ValueError):
        my_episode.title = 6
    with pytest.raises(ValueError):
        my_episode.title = " "
    with pytest.raises(ValueError):
        my_episode.title = None


def test_episode_audio_setter(my_episode):
    assert my_episode.audio == "No link"
    my_episode.audio = "https://google.com"
    assert my_episode.audio == "https://google.com"
    with pytest.raises(ValueError):
        my_episode.audio = ""
    with pytest.raises(ValueError):
        my_episode.audio = 6
    with pytest.raises(ValueError):
        my_episode.audio = " "
    with pytest.raises(ValueError):
        my_episode.audio = None


def test_episode_description_setter(my_episode):
    assert my_episode.description == "No description"
    my_episode.description = "The planet with the largest rings"
    assert my_episode.description == "The planet with the largest rings"
    with pytest.raises(ValueError):
        my_episode.description = ""
    with pytest.raises(ValueError):
        my_episode.description = 6
    with pytest.raises(ValueError):
        my_episode.description = " "
    with pytest.raises(ValueError):
        my_episode.description = None


def test_episode_equality(my_episode, my_podcast, my_podcast_2):
    episode1 = Episode(2, my_podcast)
    assert episode1 != my_episode
    episode2 = Episode(1, my_podcast_2)  # In practice this cannot exist; only one episode of each id.
    assert episode2 == my_episode
    episode3 = Episode(1, my_podcast)
    assert episode3 == my_episode
    assert my_episode != "Banana"
    assert my_episode != repr(my_episode)


def test_episode_inequality(my_episode, my_podcast, my_podcast_3):
    episode1 = Episode(2, my_podcast)
    assert episode1 > my_episode
    episode2 = Episode(1, my_podcast_3)
    assert episode2 < episode1
    assert not episode2 < "Banana"
    assert not episode1 > repr(my_episode)


def test_episode_hash(my_episode, my_podcast, my_podcast_3):
    episode1 = Episode(2, my_podcast)
    assert hash(episode1) != hash(my_episode)
    episode2 = Episode(1, my_podcast)
    assert hash(episode2) == hash(my_episode)
    episode3 = Episode(1, my_podcast_3)
    assert hash(episode3) != hash(my_episode)


def test_playlist_initialisation(my_playlist, my_user):
    assert my_playlist.id == 1
    assert my_playlist.owner == my_user
    assert my_playlist.title == "Untitled"
    assert len(my_playlist.episodes) == 0
    playlist1 = Playlist(2, my_user, "Favourites ")
    assert playlist1.id == 2
    assert playlist1.owner == my_playlist.owner
    assert playlist1.title == "Favourites"


def test_playlist_set_title(my_playlist):
    assert my_playlist.title == "Untitled"
    my_playlist.title = "  Favourites "
    assert my_playlist.title == "Favourites"
    with pytest.raises(ValueError):
        my_playlist.title = ""
    with pytest.raises(ValueError):
        my_playlist.title = 6
    with pytest.raises(ValueError):
        my_playlist.title = None
    with pytest.raises(ValueError):
        my_playlist.title = " "


def test_playlist_add_and_remove_episode(my_playlist, my_episode, my_podcast):
    assert my_playlist.episodes == []
    my_playlist.add_episode(my_episode)
    assert len(my_playlist) == 1
    my_playlist.add_episode(my_episode)
    assert len(my_playlist) == 1
    episode1 = Episode(2, my_podcast)
    my_playlist.add_episode(episode1)
    assert len(my_playlist) == 2
    my_playlist.remove_episode(my_episode)
    assert len(my_playlist) == 1
    my_playlist.remove_episode(my_episode)
    assert len(my_playlist) == 1
    my_playlist.remove_episode(episode1)
    assert len(my_playlist) == 0
    with pytest.raises(TypeError):
        my_playlist.add_episode(my_podcast)
    with pytest.raises(TypeError):
        my_playlist.add_episode(6)


def test_playlist_get_total_runtime(my_playlist, my_episode, my_podcast):
    assert my_playlist.get_total_runtime() == 0
    my_playlist.add_episode(my_episode)
    assert my_playlist.get_total_runtime() == 0
    episode1 = Episode(2, my_podcast, "Episode 2", "No link", 100)
    episode2 = Episode(3, my_podcast, "Episode 3", "No link", 200)
    my_playlist.add_episode(episode1)
    assert my_playlist.get_total_runtime() == 100
    my_playlist.add_episode(episode2)
    assert my_playlist.get_total_runtime() == 300


def test_playlist_inequality(my_playlist, my_episode, my_user):
    assert not my_playlist < 5
    my_playlist.add_episode(my_episode)
    playlist1 = Playlist(2, my_user)
    assert playlist1 < my_playlist
    assert not playlist1 > my_playlist
    assert not playlist1 < len(my_playlist)


def test_playlist_equality(my_playlist, my_episode, my_user):
    assert not my_playlist == 1
    playlist1 = Playlist(2, my_user)
    assert not my_playlist == playlist1
    playlist2 = Playlist(1, my_user)
    assert my_playlist == playlist2
    user1 = User(2, "Adam", "Password")
    playlist3 = Playlist(1, user1)
    assert not my_playlist == playlist3


def test_playlist_hash(my_playlist, my_episode, my_user):
    playlist1 = Playlist(2, my_user)
    assert not hash(my_playlist) == hash(playlist1)
    playlist2 = Playlist(1, my_user)
    assert hash(my_playlist) == hash(playlist2)
    playlist3 = Playlist(1, my_user, "Favourites")
    assert not hash(my_playlist) == hash(playlist3)


def test_playlist_swap_element(my_playlist, my_podcast):
    episode1 = Episode(2, my_podcast, "Apple")
    episode2 = Episode(3, my_podcast, "Banana")
    episode3 = Episode(4, my_podcast, "Orange")
    my_playlist.add_episode(episode1)
    my_playlist.add_episode(episode2)
    my_playlist.add_episode(episode3)
    titles = ",".join([e.title for e in my_playlist.episodes])
    assert titles == "Apple,Banana,Orange"
    my_playlist.swap_element(0, 2)
    titles = ",".join([e.title for e in my_playlist.episodes])
    assert titles == "Orange,Banana,Apple"


def test_playlist_shuffle(my_playlist, my_podcast):
    episode1 = Episode(2, my_podcast, "Apple")
    episode2 = Episode(3, my_podcast, "Banana")
    episode3 = Episode(4, my_podcast, "Orange")
    my_playlist.add_episode(episode1)
    my_playlist.add_episode(episode2)
    my_playlist.add_episode(episode3)
    shuffled_list1 = my_playlist.episodes.copy()
    random.seed(10)
    random.shuffle(shuffled_list1)
    random.seed(10)
    shuffled_list2 = my_playlist.shuffle()
    assert shuffled_list1 == shuffled_list2


def test_load_podcast(csv_reader):
    """Ignore git blame. Code written by skuxxxxx(gsan089)"""
    csv_reader.load_podcasts()
    assert len(csv_reader.podcasts) == list(csv_reader.podcasts.values())[-1].id #checks last id of podcast with len of list
    podcast_1 = Podcast(
        1,  # podcast_id
        "D Hour Radio Network",  # author
        "D-Hour Radio Network",  # title
        "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg",
        # image
        """The D-Hour Radio Network is the home of real entertainment radio and "THE" premiere online radio network. We showcase dynamically dynamite radio shows for the sole purpose of entertaining your listening ear. Here on the D-hour Show Radio network we take pride in providing an outlet for Celebrity Artists, Underground Artists, Indie Artists, Producers, Entertainers, Entrepreneurs, Internet Stars and future business owners. We discuss topics of all forms and have a great time while doing so. We play all your favorite hits in the forms of Celebrity, Indie, Hip Hop, Soul/R&B, Pop, and everything else you want and consider popular. If you would like yourself and or your music to be showcased on our radio network submit email requests for music airplay, interviews and etc.. to:  dhourshow@gmail.com and we will get back to you promptly. Here at the D-Hour Radio Network we are Family and all of our guests, listeners and loyal fans are family too.  So tune into the D-Hour Radio Network and join the Family! """,
        # description
        "http://www.blogtalkradio.com/dhourshow",  # website
        538283940,  # itunes_id
        "English"  # language
    )
    podcast_2 = Podcast(
        2,  # podcast_id
        "Brian Denny",  # author
        "Brian Denny Radio",  # title
        "http://is5.mzstatic.com/image/thumb/Music111/v4/49/c8/19/49c8190a-ca0f-f32c-c089-d7ae502d2cb8/source/600x600bb.jpg",
        # image
        """5-in-1: Brian Denny Radio is the fastest podcast in all the land. Each episode is 5 minutes and done in 1 take. Brian covers news, politics, sports, pro wrestling, life & more!
        No one does it faster or better, probably. #BDR""",  # description
        "http://thebdshow.libsyn.com/podcast",  # website
        1132261215,  # itunes_id
        "English"  # language
    )
    assert csv_reader.podcasts[1] == podcast_1
    assert csv_reader.podcasts[2] == podcast_2


def test_load_episodes(csv_reader):
    csv_reader.load_episodes()
    episode_1 = Episode(
        1,  # episode_id
        csv_reader.episodes[1].podcast,  # podcast_id
        "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3",  # episode_title
        "http://archive.org/download/mandarian-orange-show-episode-74/mandarian-orange-show-episode-74.mp3",
        # episode_audio
        2739,  # episode_length (in seconds)
        """<p><img data-attachment-id="360" data-permalink="http://www.janelleandphil.com/2017/12/01/the-mandarian-orange-show-episode-74-bad-hammer-time-or-30-day-moviepass-challenge-part-3/mandarian-74/" data-orig-file="https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?fit=1080%2C1080" data-orig-size="1080,1080" data-comments-opened="1" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;1&quot;}" data-image-title="mandarian 74" data-image-description="" data-medium-file="https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?fit=300%2C300" data-large-file="https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?fit=530%2C530" src="https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?resize=300%2C300" alt="" class="alignnone size-medium wp-image-360" srcset="https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?resize=300%2C300 300w, https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?resize=150%2C150 150w, https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?resize=768%2C768 768w, https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?resize=1024%2C1024 1024w, https://i0.wp.com/www.janelleandphil.com/wp-content/uploads/2017/12/mandarian-74.jpg?w=1080 1080w" sizes="(max-width: 300px) 100vw, 300px" data-recalc-dims="1" /></p>
        <p>In this episode, Phil and Janelle talk about the next movies in the 30 Day MoviePass Challenge!  They also discuss Thanksgiving, Back to the Future, a really bad movie, Tom Cruise, Lyndon B Johnson, Laughlin, bad construction timing, and more.</p>""",
        # episode_desc
        datetime(2017, 12, 1, 0, 9, 47)  # upload_date
    )
    episode_2 = Episode(
        2,  # episode_id
        csv_reader.episodes[1].podcast,
        "Finding yourself in the character by justifying your actions",  # episode_title
        "http://reallifeactor.podomatic.com/enclosure/2017-11-30T19_09_56-08_00.mp3",  # episode_audio
        1875,  # episode_length (in seconds)
        """<img src="http://assets.podomatic.net/ts/ee/8d/9e/jeff62500/1400x1400_12508930.jpg" alt="itunes pic" /><br />The best way to find authenticity in characters outside of your wheelhouse. Powerful stuff.""",
        # episode_desc
        datetime(2017, 12, 1, 3, 9, 56)  # upload_date
    )
    assert csv_reader.episodes[0] == episode_1
    assert csv_reader.episodes[1] == episode_2

#test add_to_playlist

def test_add_episode_to_playlist(my_playlist, my_episode):
    # Initially, the playlist should be empty
    assert len(my_playlist.episodes) == 0

    # Add the episode to the playlist
    my_playlist.add_episode(my_episode)

    # Check that the episode was added to the playlist
    assert len(my_playlist.episodes) == 1
    assert my_episode in my_playlist.episodes

    # Check that the same episode isn't added again (assuming unique episodes in a playlist)
    my_playlist.add_episode(my_episode)
    assert len(my_playlist.episodes) == 1  # Still 1, because it's not duplicated

def test_remove_episode_from_playlist(my_playlist, my_episode):
    # Add the episode to the playlist first
    my_playlist.add_episode(my_episode)
    assert len(my_playlist.episodes) == 1

    # Remove the episode from the playlist
    my_playlist.remove_episode(my_episode)

    # Check that the playlist is empty after removal
    assert len(my_playlist.episodes) == 0
    assert my_episode not in my_playlist.episodes


def test_podcast_episodes(my_podcast, my_episode):
    # Add an episode to the podcast
    my_podcast.episodes.append(my_episode)

    # Create a mock Playlist instance (or whatever class the podcast_episodes method belongs to)

    # Get episodes of the podcast using the method
    episodes = my_podcast.podcast_episodes(my_podcast)

    # Assert that the returned episodes match the episodes in the podcast
    assert episodes == my_podcast.episodes
    #assert len(episodes) == 1
    assert my_episode in episodes

    # Add another episode and test again
    new_episode = Episode(2, my_podcast, "Another Episode", "https://audio-url.com")
    my_podcast.episodes.append(new_episode)

    episodes = my_podcast.podcast_episodes(my_podcast)

    # Check that both episodes are now in the list
    #assert len(episodes) == 2
    assert new_episode in episodes
    assert my_episode in episodes

