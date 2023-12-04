from models.peewee_models import Category, Task
from typing import Dict, Any
from util import safe_query

class CategoryRepository:

    
    def create_category(self, id: int, name: str, task_id: Task):
        try:
            Category.create(id=id, name=name, task=task_id)
        except Exception as e:
            print(e)
            return False
        return True
    
    def create_category_concise(self, id: int, name: str, task_id: int):
        print(id, name, task_id)
        query = Category.insert(id=id, name=name, task=None)
        res = safe_query(query)
      
        return res
    
    def update_category(self, id: int, details: Dict[str, Any]):
        try:
            query = Category.update(**details).where(Category.category_id == id)
            query.execute()
        except Exception as e:
            print(e)
            return False
        return True
    
    def update_category_concise(self, id: int, details: Dict[str, Any]):
        
        query = Category.update(**details).where(Category.category_id == id)
        res = safe_query(query)
        
        return res
    
    def delete_category(self, id: int):
        try:
            Category.delete_by_id(id)
        except Exception as e:
            print(e)
            return False
        return True
    
    def delete_category_concise(self, id: int):
       
        query = Category.delete_by_id(id)
        res = safe_query(query)
        
        return res
    
    
    def get_category(self, id: int):
        return Category.get(Category.id == id)
    
    def get_category_concise(self, id: int):
        query = Category.select().where(Category.id == id)
        # query = Category.get(Category.id == id)
       
        res = safe_query(query)
        
        return res
    
    def get_categories(self):
        # should return all tasks under a particular category
        return list(Category.select())
    
    def get_categories_concise(self):
        # should return all tasks under a particular category
        query = Category.select()
        res = safe_query(query)
        
        return list(res)