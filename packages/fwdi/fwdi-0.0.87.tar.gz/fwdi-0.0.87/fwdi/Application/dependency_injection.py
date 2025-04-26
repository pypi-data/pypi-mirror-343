from ..Application.Abstractions.base_task_queue_manager import BaseTaskQueueManager
from ..Application.TaskManager.task_queue_manager import TaskQueueManager
from ..Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from .Usecase.user_repository import UserRepositoryFWDI

class DependencyInjection():

    @staticmethod
    def AddApplication(services:BaseServiceCollectionFWDI)->None:
        services.AddTransient(BaseUserRepositoryFWDI, UserRepositoryFWDI)
        services.AddSingleton(BaseTaskQueueManager, TaskQueueManager)