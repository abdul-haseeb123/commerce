from auctions.models import User, Listing, Bid, Comment
from rest_framework import serializers

class BidSerializer(serializers.ModelSerializer):
    bidder = serializers.ReadOnlyField(source='bidder.username')
    listing = serializers.ReadOnlyField(source='listing.name')
    
    class Meta:
        model = Bid
        fields = ["id", "listing", "bidder", "bid_amount", "bid_date"]

class CommentSerializer(serializers.ModelSerializer):
    commentor = serializers.ReadOnlyField(source='commentor.username')
    listing = serializers.ReadOnlyField(source='listing.name')

    class Meta:
        model = Comment
        fields = ["id", "listing", "commentor", "text", "comment_at"]

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    bids = BidSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = ["id", "owner", "name", "description", "starting_bid", "current_bid", "bids","comments", "created_at", "image_url", "active", "category"]



class UserSerializer(serializers.HyperlinkedModelSerializer):
    listings = serializers.HyperlinkedRelatedField(many=True, view_name='listing-detail', read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ["url", "id", "username", "email", "password", "listings"]

# class UserSerializer(serializers.ModelSerializer):
#     listings = serializers.PrimaryKeyRelatedField(many=True, queryset=Listing.objects.all())

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "password", "listings"]