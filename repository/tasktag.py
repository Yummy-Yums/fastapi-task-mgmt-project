from models.peewee_models import Tag, Task

class TaskTagRepository:
    
    def insert_tags_and_tasks(self):
        # do a bull insert
        task_data = Task.select()
        tag_data = Tag.select()
    
    def get_tasks_associated_with_tag(self, tag_id: int):
        #get all task
        pass
    
    def get_tags_associated_with_task(self, task_id: int):
        #get all tags
        pass
    
    # Assuming you have Peewee models for Task, Tag, and Task_Tag

from peewee import JOIN

# # Suppose you have a task_id for which you want to retrieve associated tags.
# task_id = 1  # Replace with the task_id you're interested in.

# # Query to retrieve a specific task and its associated tags.
# query = (Task
#          .select(Task, Tag)
#          .join(Task_Tag, JOIN.INNER)
#          .join(Tag, JOIN.INNER)
#          .where(Task.task_id == task_id))

# # Execute the query to retrieve the task and associated tags.
# task_with_tags = query.get()

# # Access the task and associated tags.
# print("Task Name:", task_with_tags.task.task_name)
# print("Tags:")
# for tag in task_with_tags.tags:
#     print("- Tag Name:", tag.tag.tag_name)

# from peewee import fn

# # Assume you have your Peewee models defined

# # Select data from Table1
# table1_data = Table1.select()

# # Select data from Table2
# table2_data = Table2.select()

# # Create a list of dictionaries for the join table
# join_table_data = []

# for row1 in table1_data:
#     for row2 in table2_data:
#         join_table_data.append({
#             'table1_id': row1.id,
#             'table2_id': row2.id,
#             'additional_data': 'Additional Data'
#         })

# # Bulk insert data into the JoinTable
# with database.atomic():
#     JoinTable.insert_many(join_table_data).execute()

