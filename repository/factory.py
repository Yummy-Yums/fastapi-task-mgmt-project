from category import CategoryRepository
from reminder import ReminderRepository
from tag import TagRepository
from task import TaskRepository
from user import UserRepository

from fastapi import Depends

def get_user_repo_factory(repo=Depends(UserRepository)):
    return repo

def get_task_repo_factory(repo=Depends(TaskRepository)):
    return repo

def get_tag_repo_factory(repo=Depends(TagRepository)):
    return repo

def get_reminder_repo_factory(repo=Depends(ReminderRepository)):
    return repo

def get_category_repo_factory(repo=Depends(CategoryRepository)):
    return repo
