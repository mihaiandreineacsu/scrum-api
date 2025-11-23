from typing import Any

from django.urls import reverse

from core.models import Board, Category, Contact, ListOfTasks, Subtask, Task, User

TEST_USER_EMAIL = "johndoe@example.com"
TEST_USER_FULL_NAME = "John Doe"
TEST_USER_PASSWORD = "password123"

TEST_OTHER_USER_EMAIL = "johnwick@example.com"
TEST_OTHER_USER_FULL_NAME = "John Wick"
TEST_OTHER_USER_PASSWORD = "wick@example.com"

TEST_ADMIN_EMAIL = "admin@example.com"
TEST_ADMIN_PASSWORD = "admin123"

TEST_CONTACT_EMAIL = "johnconners@example.com"
TEST_CONTACT_FULL_NAME = "John Conners"
TEST_CONTACT_PHONE_NUMBER = "+4915777777777"

TEST_OTHER_CONTACT_EMAIL = "johnwill@example.com"
TEST_OTHER_CONTACT_FULL_NAME = "John Will"
TEST_OTHER_CONTACT_PHONE_NUMBER = "+4915733333333"


def detail_url(detail_id: str | int, view_name: str):
    return reverse(f"{view_name}:{view_name}-detail", args=[detail_id])


def create_test_user(
    email: str = TEST_USER_EMAIL,
    password: str = TEST_USER_PASSWORD,
    **params: Any,
) -> User:
    return User.objects.create_user(email=email, password=password, **params)


def create_test_superuser(
    email: str = TEST_ADMIN_EMAIL, password: str = TEST_ADMIN_PASSWORD, **params: Any
) -> User:
    return User.objects.create_superuser(email=email, password=password, **params)


def create_test_guest_user(**params: Any) -> User:
    return User.objects.create_guest_user(**params)


def create_test_board(
    user: User | None = None,
    title: str = f"{TEST_USER_FULL_NAME}'s Board",
    **params: Any,
) -> Board:
    if not user:
        user = create_test_user()

    board = Board.objects.create(user=user, title=title, **params)
    return board


def create_test_list_of_tasks(
    user: User | None = None,
    board: Board | None = None,
    name: str = "TODO",
    order: int = 0,
    **params: Any,
) -> ListOfTasks:
    if user and board:
        assert board.user == user, "The board's user does not match the provided user."
    if not user:
        user = create_test_user()

    if not board:
        board = create_test_board(user)

    return ListOfTasks.objects.create(name=name, board=board, order=order, **params)


def create_test_contact(
    user: User | None = None,
    email: str = TEST_CONTACT_EMAIL,
    name: str = TEST_CONTACT_FULL_NAME,
    phone_number: str = TEST_CONTACT_PHONE_NUMBER,
    **params: Any,
) -> Contact:
    if not user:
        user = create_test_user()
    return Contact.objects.create(
        user=user, email=email, name=name, phone_number=phone_number, **params
    )


def create_test_category(
    user: User | None = None, name: str = "bug", color: str = "#FF0000", **params: Any
) -> Category:
    if not user:
        user = create_test_user()
    category, _ = Category.objects.get_or_create(
        user=user, name=name, color=color, **params
    )
    return category


def create_test_task(
    user: User | None = None,
    category: Category | None = None,
    list_of_tasks: ListOfTasks | None = None,
    title: str = "Fix broken pipe",
    description: str = "",
    priority: str = "Urgent",
    order: int = 0,
    **params: Any,
) -> Task:
    if user and list_of_tasks:
        assert (
            list_of_tasks.user == user
        ), "The list of tasks' board user does not match the provided user."

    if user and category:
        assert (
            category.user == user
        ), "The category's user does not match the provided user."

    if not user:
        user = create_test_user()

    if not category:
        category = create_test_category(user)

    if not list_of_tasks:
        list_of_tasks = create_test_list_of_tasks(user)

    return Task.objects.create(
        list_of_tasks=list_of_tasks,
        category=category,
        title=title,
        description=description,
        priority=priority,
        order=order,
        **params,
    )


def create_test_subtask(
    user: User | None = None,
    task: Task | None = None,
    title: str = "Write a unit test for the broken pipe",
    done: bool = False,
    **params: Any,
) -> Subtask:

    if user and task:
        assert (
            task.list_of_tasks.board.user == user
        ), "The task's board user does not match the provided user."

    if not user:
        user = create_test_user()

    if not task:
        task = create_test_task(user=user)
    else:
        task.user = user

    return Subtask.objects.create(title=title, task=task, done=done, **params)


def validate_response_data(response: Any) -> dict[str, Any]:
    """Validate that the response has data and return it as a dictionary."""
    if getattr(response, "data", None) is None:
        raise ValueError("Response data is None")
    return getattr(response, "data")
