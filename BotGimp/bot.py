from botcity.core import DesktopBot, Backend
from pynput.keyboard import Key
import os

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def open_gimp(bot, gimp_executable_path):
    # Launching the app
    bot.execute(gimp_executable_path)
    bot.connect_to_app(backend=Backend.UIA, path=gimp_executable_path)        
    gimp_main_window = bot.find_app_window(title_re="GNU", waiting_time=30000)
    if gimp_main_window.exists():
        bot.clickAt(bot.display_size()[0]/2-500, bot.display_size()[1]/2)
        bot.maximize_window()
    return gimp_main_window.exists()    

def open_files(bot, input_path):
    bot.control_key("o")
    bot.wait(500)
    bot.type_down()
    bot.kb_type(input_path)
    bot.enter()
    
    bot.control_a()
    bot.type_left()
    bot.type_down()
    bot.control_a() 
    bot.enter()
    bot.wait(8000)

def crop_to_content(bot):
    bot.clickAt(bot.display_size()[0]/2-500, bot.display_size()[1]/2)

    #Crop to content
    bot._kb_controller.press(key=Key.alt)
    bot.kb_type("i")
    bot._kb_controller.release(key=Key.alt)
    
    for _ in range(9):
        bot.type_down()
    bot.enter()

def export_file(bot, output_path):
    #Export
    bot.control_key("e")
    bot.wait(500)
    bot.type_left()
    
    bot.kb_type(output_path+"\\")
    bot.enter()
    
    bot.wait(3000)

    bot.enter()


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = DesktopBot()
    # Implement here your logic...

    # Application path
    gimp_executable_path = r"C:\Program Files\GIMP 2\bin\gimp-2.10.exe"

    if open_gimp(bot, gimp_executable_path):

        script_directory = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(os.path.dirname(script_directory), "Input")
        output_path = os.path.join(os.path.dirname(script_directory), "Output")

        
        open_files(bot, input_path)

        number_files_inputs = len(os.listdir(input_path))
        for _ in range(number_files_inputs):
            crop_to_content(bot)
            export_file(bot, output_path)

            bot.wait(1000)
            #Close file
            bot.control_key("w")
            bot.control_key("d")

        #Close gimp
        bot.alt_f4()


    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

if __name__ == '__main__':
    main()