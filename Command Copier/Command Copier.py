import maya.api.OpenMaya as om
import maya.cmds as cmds
import os
import fnmatch as fm
import maya.mel as mel
import re

# Set log file path
log_file = "C:/Command_files/maya_command_log.txt"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Globals
callback_id = None
log_text_field = None
executing_commands = False  # Global flag to prevent recursion

def filter_writing(code):
    # Define patterns to match
    patterns = ["*-*", "*;*"]
    keywords = ["import", "cmds", "eval"]

    # Check if the code matches all patterns
    if all(fm.fnmatch(code, pattern) for pattern in patterns):
        # Additional condition: Check if specific keywords are present
        return code
    elif all(keyword in code for keyword in keywords):
        return code  # Return the code if all conditions are met

    # If no conditions are met, return None
    return None

def run_code():
    global executing_commands
    executing_commands = True  # Set flag to prevent logging during execution
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            commands = f.readlines()

        buffer = []  # for multi-line Python code blocks
        for cmd in commands:
            cmd = cmd.strip()
            if not cmd:
                continue

            lang = detect_language(cmd)

            try:
                if lang == "Python":
                    buffer.append(cmd)
                    # Try executing accumulated Python code
                    try:
                        compiled = compile("\n".join(buffer), "<log>", "exec")
                        exec(compiled, globals())
                        buffer = []  # clear buffer if it succeeded
                    except SyntaxError:
                        # not a complete block yet → keep buffering
                        pass

                elif lang == "MEL":
                    mel.eval(cmd)

            except Exception as e:
                print(f"Error executing {lang} command:\n{cmd}\n{e}")

        # In case leftover Python never executed
        if buffer:
            try:
                exec("\n".join(buffer), globals())
            except Exception as e:
                print("Error in leftover Python block:", e)

    finally:
        executing_commands = False  # Reset flag after execution

# Function to guess language
def detect_language(cmd):
    if "(" in cmd or "import " in cmd or "=" in cmd:
        return "Python"
    return "MEL"

def clear_log_file():
    with open(log_file, "w", encoding="utf-8") as f:
        pass

def command_callback(message, *args):
    global executing_commands
    if executing_commands:
        return

    cmd = message.strip()

    if not (cmd.endswith(";") and "-" in cmd):
        return

    lang = detect_language(cmd)
    log_entry = f"{cmd}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

    if log_text_field:
        old_text = cmds.scrollField(log_text_field, q=True, text=True)
        ui_entry = f"[{lang}]  {log_entry}\n"
        cmds.scrollField(log_text_field, e=True, text=old_text + ui_entry)

def start_logging(*args):
    global callback_id
    if callback_id is None:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n")
        callback_id = om.MCommandMessage.addCommandOutputCallback(command_callback)

# Stop logging
def stop_logging(*args):
    global callback_id
    if callback_id:
        om.MMessage.removeCallback(callback_id)
        callback_id = None
    print("Command logging stopped.")


def command_logger_ui():
    global log_text_field

    if cmds.window("cmdLoggerWin", exists=True):
        cmds.deleteUI("cmdLoggerWin")

    window = cmds.window("cmdLoggerWin", title="Maya Command Logger", widthHeight=(400, 320))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="Maya Command Logger (MEL & Python)", align="center", height=20)
    cmds.rowLayout(numberOfColumns=4, columnWidth3=(133, 133, 133))
    cmds.button(label="Start Logging", command=start_logging, bgc=(0.4, 0.8, 0.4))
    cmds.button(label="Stop Logging", command=stop_logging, bgc=(0.8, 0.4, 0.4))
    cmds.button(label="Clear Log File", command=lambda *args: clear_log_file(), bgc=(0.4, 0.4, 0.8))
    cmds.button(label="Run Logged Code", command=lambda *args: run_code(), bgc=(0.8, 0.8, 0.4))
    cmds.setParent("..")

    log_text_field = cmds.scrollField(editable=False, wordWrap=True, text="Command log will appear here...\n", height=200)

    cmds.button(label="Close", command=lambda *args: cmds.deleteUI(window))

    cmds.showWindow(window)

# Run UI
command_logger_ui()
