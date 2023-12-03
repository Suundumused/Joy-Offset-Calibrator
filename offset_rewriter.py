import os
import platform
import sys
import time
import pygame

from msg_window import show_message

def filter_val(value_a, value_b): #interpolate
    if value_a >= 0:
        acc_result = value_a + value_b * (1 - value_a)
    
    else:
        acc_result = value_a + value_b * (1 + value_a)
    
    return acc_result

def install_drivers():
    bits = platform.architecture()[0]
    
    config_name = 'Driver'
    
    try:
        if getattr(sys, 'frozen', False): 
            # Executando como executable (PyInstaller)
            path = os.path.dirname(sys.executable)
        else:
            # Executando como  script .py
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        if bits == '32bit':
            installer=os.path.join(path, config_name+"\DriverX86\ViGEmBusSetup_x86.msi")
            
            show_message('Error: "Driver not installed."')
            
            os.startfile(installer)
            
            sys.exit()
            
        elif bits == '64bit':
            installer=os.path.join(path, config_name+"\DriverX64\ViGEmBusSetup_x64.msi")
            
            show_message('Error: "Driver not installed."')
            
            os.startfile(installer)
            
            sys.exit()
        else:
            show_message('Error: "Architecture information not available."')
            
            sys.exit()
            
    except Exception as e:
        show_message(f'{repr(e)}')
        
        sys.exit()
        
try:
    import vgamepad as vg
    
except Exception as e:
    install_drivers()

def read_joystick(vars):
    gamepad = vg.VX360Gamepad()
    
    button_mappings = {
        0: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        1: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        2: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        3: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        4: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        5: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        6: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        7: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        8: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
        9: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        10: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        11: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        12: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        13: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        14: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        # Add more button mappings as needed...
    }
                
    pygame.init()
    pygame.joystick.init()
    
    try:
        while pygame.joystick.get_count() < 2 and vars.ReadInput:
            vars.msg = 'No joysticks found'
            time.sleep(0.33)
            
    except Exception as e:
        show_message(f'{repr(e)}')
        
        vars.ReadInput = False
        vars.KeepMain = False
        
        sys.exit()
        
    while vars.joy_id == -1 and vars.ReadInput:
        vars.msg = "Joystick not found. Set your joystick ID. Usually it's 1"
        time.sleep(0.33)
    
    while vars.ReadInput:
        try:
            joystick = pygame.joystick.Joystick(vars.joy_id)
            joystick.init()
            
            num_axes = joystick.get_numaxes()
            
            print(f"Joystick name: {joystick.get_name()}")
            print(f"Number of axes: {num_axes}")
            
            break
        
        except Exception as e:
            vars.joy_id = -1
            vars.msg = repr(e)
            time.sleep(0.33)
    
    while vars.ReadInput:
        try:
            try:
                pygame.joystick.Joystick(vars.joy_id)
                
            except:
                raise Exception('Invalid ID')
            
            if pygame.joystick.get_count() < 2:
                vars.msg = 'No joysticks found'
                raise Exception('Joystick not found')
            
            if vars.config['usages']['replicate_btns']:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        button = event.button
                        if button in button_mappings:
                            gamepad.press_button(button=button_mappings[button])

                    elif event.type == pygame.JOYBUTTONUP:
                        button = event.button
                        if button in button_mappings:
                            gamepad.release_button(button=button_mappings[button])
                        
            vars.axis[0] = joystick.get_axis(0)
            vars.axis[1] = joystick.get_axis(1) * -1
            vars.axis[2] = joystick.get_axis(2)
            vars.axis[3] = joystick.get_axis(3) * -1
            vars.axis[4] = joystick.get_axis(4)
            vars.axis[5] = joystick.get_axis(5)
               
            pygame.event.pump()  # Process events
            
            if vars.config['usages']['use_l_analog']:
                vars.new_axis[0] = filter_val(vars.axis[0], vars.config['offsets']['l_analog_offset_x'])
                vars.new_axis[1] = filter_val(vars.axis[1], vars.config['offsets']['l_analog_offset_y'])
                 
                gamepad.left_joystick_float(vars.new_axis[0], vars.new_axis[1])
            '''else:
                gamepad.left_joystick_float(vars.axis[0], vars.axis[1])'''
            
            if vars.config['usages']['use_r_analog']:
                vars.new_axis[2] = filter_val(vars.axis[2], vars.config['offsets']['r_analog_offset_x'])
                vars.new_axis[3] = filter_val(vars.axis[3], vars.config['offsets']['r_analog_offset_y'])
                
                gamepad.right_joystick_float(vars.new_axis[2], vars.new_axis[3])  
            '''else:
                gamepad.right_joystick_float(vars.axis[2], vars.axis[3])'''
                
            if vars.config['usages']['use_l_trigger']:    
                vars.new_axis[4] = filter_val(vars.axis[4], vars.config['offsets']['l_trigger_offset'])
                            
                gamepad.left_trigger_float(vars.new_axis[4])
            '''else:
                gamepad.left_trigger_float(vars.axis[4])'''
                
            if vars.config['usages']['use_r_trigger']:
                vars.new_axis[5] = filter_val(vars.axis[5], vars.config['offsets']['r_trigger_offset'])
                
                gamepad.right_trigger_float(vars.new_axis[5])
            '''else:
                gamepad.right_trigger_float(vars.axis[5])'''
                
            gamepad.update()

            vars.msg = ''
            
            pygame.time.Clock().tick(250)
            
        except Exception as e:
            show_message(f'{repr(e)}')
            pygame.quit()
            pygame.joystick.quit()
            
            gamepad.reset()
            del gamepad

            read_joystick(vars)
                          
            break
    
    try:
        pygame.quit()
        pygame.joystick.quit()
        
        gamepad.reset()
        del gamepad
    except:
        pass
