from fastapi import Depends
from repository.factory import get_reminder_repo_factory


class ReminderService:
    
    def __init__(self, repo=Depends(get_reminder_repo_factory)) -> None:
        pass
        self.repo = repo
        
        
    # add utility method related to this service here  
        
    