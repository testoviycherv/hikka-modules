from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class AppManager(loader.Module):
    """Module for managing applications"""
    strings = {"name": "AppManager"}

    def __init__(self):
        self.app_list = []  # List to store applications
        self.removed_count = 0  # Counter for removed applications

    @loader.command()
    async def addapp(self, message: Message):
        """Add one or multiple applications. Example: .addapp App1, App2"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Please provide application names to add.")
            return
        
        apps_to_add = [app.strip() for app in args.split(",")]
        self.app_list.extend(apps_to_add)
        app_list_str = "\n".join(f"{i+1}. {app}" for i, app in enumerate(self.app_list))
        await utils.answer(message, f"Applications added successfully!\n\nCurrent list:\n{app_list_str}")

    @loader.command()
    async def removeapp(self, message: Message):
        """Remove an application by its number. Example: .removeapp 1"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await utils.answer(message, "Please provide the number of the application to remove.")
            return
        
        index_to_remove = int(args) - 1
        if 0 <= index_to_remove < len(self.app_list):
            removed_app = self.app_list.pop(index_to_remove)
            self.removed_count += 1
            app_list_str = "\n".join(f"{i+1}. {app}" for i, app in enumerate(self.app_list))
            await utils.answer(
                message,
                f"Application '{removed_app}' removed successfully!\n\nUpdated list:\n{app_list_str or 'No applications left.'}\n\n"
                f"Total removed applications: {self.removed_count}"
            )
        else:
            await utils.answer(message, "Invalid application number.")

    @loader.command()
    async def clearcount(self, message: Message):
        """Clear the removed applications counter. Example: .clearcount"""
        self.removed_count = 0
        await utils.answer(message, "Removed applications counter has been reset.")