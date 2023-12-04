from models.peewee_models import Tag, Task
from typing import Dict, Any

class TagRepository:
    def create_tag(self, id: int, name: str, task: Task):
        try:
            Tag.create(tag_id=id, tag_name=name, task=task)
        except Exception as e:
            print(e)
            return False
        return True
    
    def update_tag(self, id: int, details: Dict[str, Any]):
        try:
            query = Tag.update(**details).where(Tag.tag_id == id)
            query.execute()
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete_tag(self, id):
        Tag.delete_by_id(id)
    
    def get_tag(self, id: int):
        return Tag.get(Tag.id == id)
    
    def get_tags(self):
        return list(Tag.select())