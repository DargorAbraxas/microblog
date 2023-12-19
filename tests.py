
import os
os.environ["DATABASE_URL"] = "sqlite://"
import unittest
from app import app, db
from app.models import User, Post
from datetime import datetime, timezone, timedelta


# import logging
# import sys

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Create and add users to database
        self.u1 = User(username = "john", email = "john@example.com")
        self.u2 = User(username = "susan", email = "susan@example.com")
        self.u3 = User(username='mary', email='mary@example.com')
        self.u4 = User(username='david', email='david@example.com')
        db.session.add_all([self.u1, self.u2, self.u3, self.u4])
        db.session.commit()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        self.u2.set_password("cat")
        self.assertFalse(self.u2.check_password("dog"))
        self.assertTrue(self.u2.check_password("cat"))

    def test_avatar(self):
        self.assertEqual(self.u1.avatar(128), "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128")

    def test_follow_creation(self):
        following = db.session.scalars(self.u1.following.select()).all()
        followers = db.session.scalars(self.u2.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

    def test_following(self):
        self.u1.follow(self.u2)
        db.session.commit()

        # log = logging.getLogger()
        # log.debug("\n*************\n")
        # log.debug(self.u1.id)

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertEqual(self.u1.following_count(), 1)
        self.assertEqual(self.u2.followers_count(), 1)
        u1_following = db.session.scalars(self.u1.following.select()).all()
        u2_followers = db.session.scalars(self.u2.followers.select()).all()
        self.assertEqual(u1_following[0].username, "susan")
        self.assertEqual(u2_followers[0].username, "john")

    def test_unfollow(self):
        self.u1.follow(self.u2)
        db.session.commit()
        self.u1.unfollow(self.u2)
        db.session.commit()
        self.assertFalse(self.u1.is_following(self.u2))
        self.assertEqual(self.u1.following_count(), 0)
        self.assertEqual(self.u2.followers_count(), 0)

    def test_follow_posts(self):
        # Create posts
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=self.u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=self.u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=self.u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=self.u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup followers
        self.u1.follow(self.u2)
        self.u1.follow(self.u4)
        self.u2.follow(self.u3)
        self.u3.follow(self.u4)
        db.session.commit()

        # check the following posts
        f1 = db.session.scalars(self.u1.following_posts()).all()
        f2 = db.session.scalars(self.u2.following_posts()).all()
        f3 = db.session.scalars(self.u3.following_posts()).all()
        f4 = db.session.scalars(self.u4.following_posts()).all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])
        
if __name__ == "__main__":
    # logging.basicConfig( stream=sys.stderr )
    # logging.getLogger().setLevel( logging.DEBUG )
    unittest.main(verbosity=2)
