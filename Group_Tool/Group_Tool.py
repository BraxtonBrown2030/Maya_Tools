from fnmatch import fnmatch
import maya.cmds as mc

def group_function(*args):
    # Create a group for the grouped objects
    main_group_text = mc.textField('main_name', query=True, text=True)
    main_group = mc.group(name=f"{main_group_text}", em=True)
    box_value = mc.checkBox('child_group_check', query=True, value=False)

    # Find all objects in the scene that relate to the user input and group them
    for i in args:
        main_selection = mc.ls()
        cur_selection = [obj for obj in main_selection if fnmatch(obj, f'*{i}*')]
        # checks current selection to see if it is empty
        # also checks if the checkbox is checked to see if the objects should be child grouped
        if box_value:
            if cur_selection:
                group = mc.group(cur_selection, name=f'{i}_group')
                mc.parent(group, main_group)
        else:
            if cur_selection:      
                mc.parent(cur_selection, main_group)

def get_text_field():
    text = mc.textField('name_input', query=True, text=True)

    # Check if the text field is empty
    if text == '':
        mc.warning("Please enter a name")
        return

    # Split the text field input into a list
    user_input = text.split()

    # Call the group_function with the user input list
    group_function(*user_input)

# Window creation for inputting the name of the objects to group
def create_window():
    if mc.window('new_window', exists=True):
        mc.deleteUI('new_window', window=True)

    mc.window('new_window', title='Group Tool', widthHeight=(345, 280))
    mc.columnLayout(adjustableColumn=True)
    mc.textField("main_name", placeholderText='Enter main group name')
    mc.textField('name_input', placeholderText='Enter object names')
    child_group_check = mc.checkBox('child_group_check',label='Group Child Objects', value=False)
    mc.button(label='Confirm', command=lambda _: get_text_field())
    mc.button(label='Close', command='mc.deleteUI(\"new_window\", window=True)')
    mc.text(label="Enter the name of the objects you want to group in the text field."
                  "\nEach name should be separated by a space for each name convention."
                  "\nall item will be sorted into the group with he given name."
                  "\n")
    mc.text(label='<a href="https://outgoing-meerkat-d9e.notion.site/Maya-tools-help-page-18405ab91f9c80a79bb2e33197a3af27">Click here to visit help page</a>', hyperlink=True)
    # text can use urls to create a hyperlink als long as the link is set up like this.

    mc.showWindow('new_window')

create_window()