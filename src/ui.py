import pygame
import pygame_gui

# Initialize pygame
pygame.init()

def draw_ui() -> pygame.Surface:
    manager = pygame_gui.UIManager((800, 600))
    next_step_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (200, 50)),
                                                text='Next step',
                                                manager=manager)
    run_sim_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 70), (200, 50)),
                                                text='Run simulation',
                                                manager=manager)
    reset_sim_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 130), (200, 50)),
                                                text='Reset simulation',
                                                manager=manager)
    pygame_gui.elements.UITextBox(
        html_text="Steps per second",
        relative_rect=pygame.Rect(10, 190, 200, 30),
        manager=manager)
    steps_ps_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 220), (200, 50))
                                                             ,start_value=0.5, value_range=(0, 10),
                                                             manager=manager)

    elements = {
        "next_step_btn": next_step_btn,
        "steps_ps_slider": steps_ps_slider,
        "run_sim_btn": run_sim_btn,
        "reset_sim_btn": reset_sim_btn
    }
    return manager, elements

manager, ui_elements = draw_ui()