from auctions.models import User, Listing, Bid, Comment
from auctions.serializers import UserSerializer, ListingSerializer, CommentSerializer, BidSerializer
from auctions.permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import serializers

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'listings': reverse('listing-list', request=request, format=format)
    })

@api_view(['POST'])
def login_view(request):
    try:
        user = User.objects.get(username=request.data["username"])
    except User.DoesNotExist:
        return Response({"message":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(request.data["password"]):
        return Response({"message":"bad request"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(user.password)
        user.save()
        serializer.data["password"] = user.password
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class ListingList(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class BidList(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        listing = get_object_or_404(Listing, pk=pk)
        bid_amount = serializer.validated_data["bid_amount"]
        if float(bid_amount) > listing.current_bid:
            serializer.save(bidder=self.request.user, listing=listing)
            listing.current_bid = bid_amount
            listing.save()
        else:
            raise serializers.ValidationError("Bid amount must be greater than current bid.")
        
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        listing = get_object_or_404(Listing, pk=pk)
        comment_text = serializer.validated_data["text"]
        if len(comment_text) > 0:
            serializer.save(commentor=self.request.user, listing=listing)
        else:
            raise serializers.ValidationError("Comment must not be empty.")