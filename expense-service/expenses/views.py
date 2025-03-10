# ✅ JWT Authentication (No manual decoding needed, let DRF handle it)
# ✅ CRUD Operations (List, Create, Retrieve, Update, Delete)
# ✅ Filtering by Date & Amount
# ✅ Pagination
# ✅ Permissions (Only owner can edit/delete their expenses)

from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.exceptions import PermissionDenied

# ✅ Custom Pagination for Expenses
class ExpensePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# ✅ List & Create Expenses
class ExpenseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # ✅ Requires JWT Authentication
    serializer_class = ExpenseSerializer
    pagination_class = ExpensePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["category"]
    search_fields = ["description", "category"]
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user
        print(f"DEBUG: request.user -> {user} (ID: {getattr(user, 'id', None)}) Role: {getattr(user, 'role', None)}")

        if user.is_anonymous:
            raise AuthenticationFailed("User is not authenticated")

        # ✅ Apply role-based filtering
        if getattr(user, "role", None) == "admin":
            return Expense.objects.all()  # Admin sees all expenses
        elif getattr(user, "role", None) == "manager":
            user_ids = Expense.objects.values_list("user_id", flat=True).distinct()
            return Expense.objects.filter(user_id__in=user_ids)
        return Expense.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        user = self.request.user  # User is authenticated via JWT

        if not user or not user.id:
            raise ValidationError("Authenticated user not found")

        serializer.save(user_id=user.id)  # Store user_id instead of ForeignKey
        


# ✅ Retrieve, Update, Delete Expense
class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        """Ensure users can only access their own expenses unless admin."""
        user = self.request.user
        if user.role == "admin":
            return Expense.objects.all()  # Admin can see all expenses
        elif user.role == "manager":
            return Expense.objects.none()  # Manager cannot edit expenses
        return Expense.objects.filter(user=user)  # Users see only their own expenses

    def perform_update(self, serializer):
        """Ensure only the owner (or admin) can update the expense."""
        if self.request.user.role != "admin" and serializer.instance.user_id != self.request.user.id:
            raise PermissionDenied("You do not have permission to edit this expense.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the owner (or admin) can delete the expense."""
        if self.request.user.role != "admin" and instance.user_id != self.request.user.id:
            raise PermissionDenied("You do not have permission to delete this expense.")
        instance.delete()

# ✅ Get Total Expenses for a Given Period
class ExpenseSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filters = {
            "date__gte": request.query_params.get("date_from"),
            "date__lte": request.query_params.get("date_to"),
        }

        # ✅ Role-Based Filtering
        user = request.user
        queryset = Expense.objects.all() if user.role == "admin" else Expense.objects.filter(user_id=user.id)
        total_expense = (
            queryset.filter(**{k: v for k, v in filters.items() if v})
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )

        return Response({"total_expense": total_expense})
    

# ✅ Get Total Expenses Grouped by Category
class CategoryExpenseSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filters = {
            "date__gte": request.query_params.get("date_from"),
            "date__lte": request.query_params.get("date_to"),
        }

        # ✅ Role-Based Filtering
        user = request.user
        queryset = Expense.objects.all() if user.role == "admin" else Expense.objects.filter(user_id=user.id)
        category_summary = (
            queryset.filter(**{k: v for k, v in filters.items() if v})
            .values("category")
            .annotate(total=Sum("amount"))
        )

        return Response({"category_expenses": list(category_summary)})