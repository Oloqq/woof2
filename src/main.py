import pygame
import pygame_gui
from .ui import manager, ui_elements
from .drawing import draw_ground, draw_agents, Camera
from .wolf_simulation import Simulation
from .params import WINDOW_SIZE, Params

window = pygame.display.set_mode(WINDOW_SIZE)

camera = Camera(0, 0, 0.5)
running = True

simulation = Simulation(Params.grid_size)
overlay = None
autostep = False
seconds_per_step = 1

def process_events():
    global running, overlay, autostep, seconds_per_step

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("run/pause")
                if event.key == pygame.K_TAB:
                    simulation.step()
            case pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui_elements["next_step_btn"]:
                    simulation.step()
                elif event.ui_element == ui_elements["run_sim_btn"]:
                    autostep = not autostep
                    print(f"Autostep: {autostep}")
                elif event.ui_element == ui_elements["reset_sim_btn"]:
                    print('reset sim button pressed!')
                elif event.ui_element == ui_elements["normal_view_btn"]:
                    print("default display")
                    overlay = None
                elif event.ui_element == ui_elements["scent_overlay_btn"]:
                    print("scent overlay")
                    overlay = "scent"
            case pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == ui_elements["steps_ps_slider"]:
                    seconds_per_step = 1 / event.value
                    print(f"seconds_per_step: {seconds_per_step}")
        manager.process_events(event)

def main():
    clock = pygame.time.Clock()

    autostep_countdown = 0

    while running:
        process_events()
        camera.update()

        time_delta = clock.tick(60)/1000.0
        manager.update(time_delta)

        if autostep:
            autostep_countdown += time_delta
            while autostep_countdown > 0:
                simulation.step()
                autostep_countdown -= seconds_per_step

        window.fill((255, 255, 255))
        window.blit(draw_ground(simulation, camera, overlay), (0, 0))
        window.blit(draw_agents(simulation, camera, overlay), (0, 0))
        manager.draw_ui(window)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()