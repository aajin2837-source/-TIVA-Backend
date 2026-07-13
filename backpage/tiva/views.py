from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .models import (
    Coats, Shirts, Pants, Tshirt,
    Watches, Perfumes, Shoes,
    Sandals, Cart
)

from .serializer import (
    CoatSerializer, ShirtsSerializer,
    PantsSerializer, TshirtSerializer,
    WatchesSerializer, PerfumesSerializer,
    ShoesSerializer, SandalsSerializer,
    CartSerializer
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializer import RegisterSerializer
from .models import UserProfile
from rest_framework.decorators import api_view
import json
import razorpay

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



MODEL_MAP = {
    'coats': (Coats, CoatSerializer),
    'shirts': (Shirts, ShirtsSerializer),
    'pants': (Pants, PantsSerializer),
    'tshirt': (Tshirt, TshirtSerializer),
    'watches': (Watches, WatchesSerializer),
    'perfumes': (Perfumes, PerfumesSerializer),
    'shoes': (Shoes, ShoesSerializer),
    'sandals': (Sandals, SandalsSerializer),
}


class ProductListView(APIView):
    def get(self, request, category):
        model, serializer_class = MODEL_MAP.get(
            category.lower(),
            (None, None)
        )

        if model is None:
            return Response(
                {"error": "Invalid category"},
                status=status.HTTP_404_NOT_FOUND
            )

        items = model.objects.all()
        serializer = serializer_class(items, many=True)

        return Response(serializer.data)


from django.contrib.auth.models import User

class AddToCartView(APIView):
    def post(self, request):

        user_id = request.data.get("user_id")
        title = request.data.get("title")
        price = request.data.get("price")
        image = request.data.get("image")

        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=400
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=400
            )

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            title=title,
            defaults={
                "price": price,
                "image": image,
                "quantity": 1
            }
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response({
            "message": "Added To Cart",
            "item": serializer.data
        })
class CartListView(APIView):
    def get(self, request):

        user_id = request.GET.get("user_id")

        if not user_id:
            return Response(
                {"error": "User ID required"},
                status=400
            )

        items = Cart.objects.filter(user_id=user_id)

        serializer = CartSerializer(
            items,
            many=True
        )

        return Response(serializer.data)


class DeleteFromCartView(APIView):
    def delete(self, request, pk):
        try:
            item = Cart.objects.get(pk=pk)
            item.delete()

            return Response(
                {"message": "Item removed from cart"},
                status=status.HTTP_200_OK
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class UpdateCartQuantityView(APIView):
    def patch(self, request, pk):
        try:
            # Use Cart model because that's what your CartListView uses
            item = Cart.objects.get(pk=pk)
            # Get the new quantity from the request body
            new_quantity = request.data.get('quantity')
            
            if new_quantity is not None and int(new_quantity) > 0:
                item.quantity = int(new_quantity)
                item.save()
                return Response({"message": "Quantity updated"}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Cart.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):

    def post(self, request):

        username = request.data.get("username")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=400
            )

        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=400
            )

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "Registration Successful"
            })

        return Response(
            serializer.errors,
            status=400
        )


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            profile = UserProfile.objects.get(
                user=user
            )

            return Response({
                "success": True,
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": profile.full_name,
                "phone": profile.phone
            })

        return Response(
            {
                "success": False,
                "message": "Invalid Credentials"
            },
            status=401
        )
@api_view(["POST"])
def add_to_cart(request):
    Cart.objects.create(
        user=request.user,
        title=request.data["title"],
        price=request.data["price"],
        image=request.data["image"],
        quantity=1
    )

    return Response({"message": "Added"})
@api_view(["GET"])
def cart_list(request):
    items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)
@api_view(["POST"])
def update_profile(request):

    user_id = request.data.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)

        profile.full_name = request.data.get(
            "full_name",
            profile.full_name
        )

        profile.phone = request.data.get(
            "phone",
            profile.phone
        )

        profile.date_of_birth = request.data.get(
            "date_of_birth",
            profile.date_of_birth
        )

        profile.save()

        return Response({
            "message": "Profile Updated"
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )
@api_view(["GET"])
def get_profile(request):

    user_id = request.GET.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)

        return Response({
            "username": user.username,
            "email": user.email,
            "full_name": profile.full_name,
            "phone": profile.phone,
            "date_of_birth": profile.date_of_birth
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )
@api_view(["GET"])
def get_reviews(request):

    category = request.GET.get("category")
    product_id = request.GET.get("product_id")

    reviews = Review.objects.filter(
        category=category,
        product_id=product_id
    )

    data = []

    for review in reviews:
        data.append({
            "user_name": review.user_name,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at
        })

    return Response(data)
@csrf_exempt
def create_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        amount = int(float(data["amount"]) * 100)

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return JsonResponse({
            "order_id": order["id"],
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID
        })
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def save_order(request):

    payment_id = request.data.get("payment_id")
    user_id = request.data.get("user_id")
    amount = request.data.get("amount")

    print("Payment ID:", payment_id)
    print("User ID:", user_id)
    print("Amount:", amount)

    return Response({
        "message": "Order Saved Successfully"
    })