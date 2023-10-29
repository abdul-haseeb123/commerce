from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from auctions.models import User, Listing, Bid, Comment
from auctions.serializers import UserSerializer, ListingSerializer, CommentSerializer, BidSerializer

class UserSerializerTestCase(TestCase):
    """
    Test case for UserSerializer
    """
    def setUp(self):
        self.user_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpass'}
        self.serializer = UserSerializer(data=self.user_data, context={'request': RequestFactory().get('/')})

    def test_contains_expected_fields(self):
        """
        Test that the serializer data contains the expected fields.
        """
        self.assertEqual(self.serializer.is_valid(), True)
        self.serializer.save()
        data = self.serializer.data
        expected_fields = {"url", "id", "username", "email", "listings"}
        self.assertSetEqual(set(data.keys()), expected_fields)

    def test_username_field_content(self):
        """
        Test that the username field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['username'], self.user_data['username'])

    def test_email_field_content(self):
        """
        Test that the email field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['email'], self.user_data['email'])

    def test_password_field_content(self):
        """
        Test that the password field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['password'], self.user_data['password'])

class ListingSerializerTestCase(TestCase):
    """
    Test case for ListingSerializer
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing_data = {'name': 'Test Listing', 'description': 'This is a test listing.', 'starting_bid': 10.0, 'current_bid': 10.0}
        self.serializer = ListingSerializer(data=self.listing_data)

    def test_contains_expected_fields(self):
        """
        Test that the serializer data contains the expected fields
        """
        self.assertEqual(self.serializer.is_valid(), True)
        self.serializer.save(owner=self.user)
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "owner", "name", "description", "starting_bid", "current_bid", "bids","comments", "created_at", "image_url", "active", "category"]))

    def test_name_field_content(self):
        """
        Test that the title field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['name'], self.listing_data['name'])

    def test_description_field_content(self):
        """
        Test that the description field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['description'], self.listing_data['description'])

    def test_starting_bid_field_content(self):
        """
        Test that the starting_bid field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['starting_bid'], self.listing_data['starting_bid'])

class CommentSerializerTestCase(TestCase):
    """
    Test case for CommentSerializer
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)
        self.comment_data = {'text': 'This is a test comment.'}
        self.serializer = CommentSerializer(data=self.comment_data)

    def test_contains_expected_fields(self):
        """
        Test that the serializer data contains the expected fields
        """
        self.assertEqual(self.serializer.is_valid(), True)
        self.serializer.save(commentor=self.user, listing=self.listing)
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['text', 'commentor', 'listing', 'comment_at', 'id']))

    def test_text_field_content(self):
        """
        Test that the text field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['text'], self.comment_data['text'])

class BidSerializerTestCase(TestCase):
    """
    Test case for BidSerializer
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)
        self.bid_data = {'bid_amount': 20.0}
        self.serializer = BidSerializer(data=self.bid_data)

    def test_contains_expected_fields(self):
        """
        Test that the serializer data contains the expected fields
        """
        self.assertEqual(self.serializer.is_valid(), True)
        self.serializer.save(bidder=self.user, listing=self.listing)
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['bid_amount', 'bidder', 'listing', 'bid_date', 'id']))

    def test_bid_amount_field_content(self):
        """
        Test that the bid_amount field content is correct
        """
        data = self.serializer.initial_data
        self.assertEqual(data['bid_amount'], self.bid_data['bid_amount'])

class UserModelTestCase(TestCase):
    """
    Test case for User model
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')

    def test_username_field(self):
        """
        Test that the username field has the correct max length
        """
        username = self.user._meta.get_field('username')
        self.assertEqual(username.max_length, 150)

    def test_email_field(self):
        """
        Test that the email field has the correct max length
        """
        email = self.user._meta.get_field('email')
        self.assertEqual(email.max_length, 254)

    def test_object_name_is_username(self):
        """
        Test that the object name is the username
        """
        expected_object_name = self.user.username
        self.assertEqual(expected_object_name, str(self.user))

class ListingModelTestCase(TestCase):
    """
    Test case for Listing model
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)

    def test_name_field(self):
        """
        Test that the name field has the correct max length
        """
        title = self.listing._meta.get_field('name')
        self.assertEqual(title.max_length, 200)

    def test_description_field(self):
        """
        Test that the description field has the correct max length
        """
        description = self.listing._meta.get_field('description')
        self.assertEqual(description.max_length, 1000)

    def test_starting_bid_field(self):
        """
        Test that the starting_bid field has the correct max digits and decimal places
        """
        starting_bid = self.listing._meta.get_field('starting_bid')
        self.assertEqual(starting_bid.max_digits, 6)
        self.assertEqual(starting_bid.decimal_places, 2)

    def test_current_bid_field(self):
        """
        Test that the current_bid field has the correct max digits and decimal places
        """
        current_bid = self.listing._meta.get_field('current_bid')
        self.assertEqual(current_bid.max_digits, 6)
        self.assertEqual(current_bid.decimal_places, 2)


    def test_owner_field(self):
        """
        Test that the owner field has the correct related model
        """
        owner = self.listing._meta.get_field('owner')
        self.assertEqual(owner.related_model, User)

    def test_object_name_is_name(self):
        """
        Test that the object name is the title
        """
        expected_object_name = self.listing.name
        self.assertEqual(expected_object_name, str(self.listing))

class CommentModelTestCase(TestCase):
    """
    Test case for Comment model
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)
        self.comment = Comment.objects.create(text='This is a test comment.', commentor=self.user, listing=self.listing)

    def test_text_field(self):
        """
        Test that the text field has the correct max length
        """
        text = self.comment._meta.get_field('text')
        self.assertEqual(text.max_length, 1000)

    def test_commentor_field(self):
        """
        Test that the author field has the correct related model
        """
        author = self.comment._meta.get_field('commentor')
        self.assertEqual(author.related_model, User)

    def test_listing_field(self):
        """
        Test that the listing field has the correct related model
        """
        listing = self.comment._meta.get_field('listing')
        self.assertEqual(listing.related_model, Listing)

    def test_object_name_is_text(self):
        """
        Test that the object name is the text
        """
        expected_object_name = self.comment.text
        self.assertEqual(expected_object_name, str(self.comment))

class BidModelTestCase(TestCase):
    """
    Test case for Bid model
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)
        self.bid = Bid.objects.create(bid_amount=20.0, bidder=self.user, listing=self.listing)

    def test_bid_amount_field(self):
        """
        Test that the bid_amount field has the correct max digits and decimal places
        """
        bid_amount = self.bid._meta.get_field('bid_amount')
        self.assertEqual(bid_amount.max_digits, 6)
        self.assertEqual(bid_amount.decimal_places, 2)

    def test_bidder_field(self):
        """
        Test that the bidder field has the correct related model
        """
        bidder = self.bid._meta.get_field('bidder')
        self.assertEqual(bidder.related_model, User)

    def test_listing_field(self):
        """
        Test that the listing field has the correct related model
        """
        listing = self.bid._meta.get_field('listing')
        self.assertEqual(listing.related_model, Listing)

    def test_object_name_is_bid_amount(self):
        """
        Test that the object name is the bid_amount
        """
        expected_object_name = str(self.listing.name) + " " + str(self.bid.bid_amount)
        self.assertEqual(expected_object_name, str(self.bid))

class BidCreateViewTestCase(TestCase):
    """
    Test case for Bid create view
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.listing = Listing.objects.create(name='Test Listing', description='This is a test listing.', starting_bid=10.0, current_bid=10.0, owner=self.user)
        self.url = reverse('bid-list', kwargs={'pk': self.listing.pk})

    def test_unauthenticated_user_cannot_create_bid(self):
        """
        Test that an unauthenticated user cannot create a bid
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {'bid_amount': 20.0})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_bid(self):
        """
        Test that an authenticated user can create a bid
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'bid_amount': 20.0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bid_amount_must_be_greater_than_current_bid(self):
        """
        Test that the bid amount must be greater than the current bid
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'bid_amount': 5.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ['Bid amount must be greater than current bid.'])


class ApiRootViewTestCase(TestCase):
    """
    Test case for API root view
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-root')

    def test_api_root_view_returns_correct_data(self):
        """
        Test that the API root view returns the correct data
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'users': 'http://testserver/api/users/', 'listings': 'http://testserver/api/listings/'})