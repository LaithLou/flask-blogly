from unittest import TestCase

from app import app, db
from models import User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class PostViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="post_test_first",
            last_name="test_last",
            img_url=None
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_post = Post(
            title = "First Post",
            content = "Do or Do not, there is NO try",
            user_id = self.user_id
        )

        db.session.add(test_post)
        db.session.commit() 

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction """

        db.session.rollback()

    def test_add_post(self):
        """ Test adding a new post """

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Add Post</button>',html) 
    
    def test_edit_post(self):
        """ Test edit page of a post """

        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Edit</button>',html)
    
    def test_post(self):
        """ Test post page of a specific post given post id """

        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('created at',html)
    
