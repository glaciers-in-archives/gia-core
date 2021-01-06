import json

class TaskList:
    def __init__(self, global_keys: dict={}, global_metadata: dict={}):
        self.global_keys = global_keys
        self.global_metadata = global_metadata
        self.list_of_tasks = []

    def add_task(self, keys: dict, metadata: dict):
        # https://labelstud.io/guide/tasks.html
        task = dict()
        task['data'] = dict()
        task['data']['meta_info'] = dict()
        task['data'] = { **self.global_keys, **keys }
        task['data']['meta_info'] = { **self.global_metadata, **metadata }
        self.list_of_tasks.append(task)
        
    def get_data(self):
        return self.list_of_tasks
    
    def get_data_as_json(self):
        return json.dumps(self.list_of_tasks, separators=(',', ':'), ensure_ascii=False)
