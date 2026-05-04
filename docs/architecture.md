# Architecture Documentation

This document describes the observed architecture of the current `lab8-pygame` codebase based on `main.py`.

## 1) Module Dependency Graph

```mermaid
flowchart LR
    subgraph "Project"
        M["main.py"]
    end

    subgraph "Standard Library"
        R["random"]
        T["math"]
    end

    subgraph "Third-Party Library"
        P["pygame"]
    end

    M --> R
    M --> T
    M --> P
```

Notes:
- The project runtime is implemented in a single module: `main.py`.
- `random` and `math` support movement and steering calculations.
- `pygame` provides windowing, timing, drawing, events, and font rendering.

## 2) High-Level Runtime Flow

```mermaid
flowchart TD
    A["Import Module"] --> B["pygame.init()"]
    B --> C["Create Window and Clock"]
    C --> D["Define Constants, Class, and Functions"]
    D --> E["Script Entry Check"]
    E --> F["main()"]
    F --> G["Create Squares and Font"]
    G --> H["Start Main Loop"]

    H --> I["Read Events"]
    I --> J["Check QUIT Event"]
    J --> K["Update Time and Direction Refresh"]
    K --> L["Run Chase Computation"]
    L --> M["Run Flee Computation"]
    M --> N["Move Squares and Bounce on Borders"]
    N --> O["Replace Expired Squares"]
    O --> P["Render Background, Squares, and FPS"]
    P --> Q["pygame.display.flip()"]
    Q --> H

    J --> R["Set running = False"]
    R --> S["pygame.quit()"]
```

Notes:
- The game loop is frame-based and throttled to target FPS.
- Direction refresh and lifespan replacement happen inside the loop.

## 3) Function-Level Call Graph

```mermaid
flowchart LR
    subgraph "Top-Level Calls"
        T0["Module Import Time"] --> T1["pygame.init()"]
        T0 --> T2["pygame.display.set_mode()"]
        T0 --> T3["pygame.display.set_caption()"]
        T0 --> T4["pygame.time.Clock()"]
        T0 --> T5["if __name__ == '__main__' -> main()"]
    end

    subgraph "Main Function"
        M0["main()"] --> M1["Square.__init__() (x NUM_SQUARES)"]
        M0 --> M2["pygame.font.SysFont()"]
        M0 --> M3["CLOCK.tick()"]
        M0 --> M4["pygame.event.get()"]
        M0 --> M5["handle_chassing()"]
        M0 --> M6["Square.handle_fleeing()"]
        M0 --> M7["Square.move()"]
        M0 --> M8["Square.is_expired()"]
        M0 --> M9["Square.__init__() (replacement)"]
        M0 --> M10["Square.draw()"]
        M0 --> M11["draw_fps()"]
        M0 --> M12["pygame.display.flip()"]
        M0 --> M13["pygame.quit()"]
    end

    subgraph "Square Internals"
        S0["Square.__init__()"] --> S1["pygame.time.get_ticks()"]
        S0 --> S2["Square.set_random_direction()"]
        S2 --> S3["math.cos() / math.sin()"]
        S4["Square.handle_fleeing()"] --> S5["Square.center()"]
        S4 --> S6["math.hypot()"]
        S4 --> S7["random.uniform()"]
        S8["Square.move()"] --> S9["Border Bounce Logic"]
        S10["Square.draw()"] --> S11["pygame.draw.rect()"]
    end

    subgraph "Other Functions"
        H0["handle_chassing()"] --> H1["Square.center()"]
        H0 --> H2["math.hypot()"]
        D0["draw_fps()"] --> D1["clock.get_fps()"]
        D0 --> D2["font.render()"]
        D0 --> D3["surface.blit()"]
    end
```

Notes:
- `handle_chassing()` currently computes chase vectors but does not write updated velocity values back to squares.
- Fleeing logic does directly update `square.vx` and `square.vy`.

## 4) Primary Execution Sequence

```mermaid
sequenceDiagram
    participant Boot as "Python Runtime"
    participant Mod as "main.py Module"
    participant Main as "main()"
    participant Pg as "pygame"
    participant Sq as "Square Objects"

    Boot->>Mod: "Import and Execute Top-Level Statements"
    Mod->>Pg: "Initialize pygame and create window/clock"
    Mod->>Main: "Call main() from script entry"

    Main->>Sq: "Instantiate initial square list"
    Main->>Pg: "Create font"

    loop "Each Frame While running == True"
        Main->>Pg: "CLOCK.tick(FPS) and poll events"
        alt "QUIT Event Received"
            Main->>Main: "Set running = False"
        else "Continue Simulation"
            Main->>Pg: "Read current ticks"
            alt "Direction Interval Reached"
                Main->>Sq: "Call set_random_direction() for each square"
            else "No Refresh"
                Main->>Main: "Keep current direction"
            end

            Main->>Sq: "Run handle_chassing(squares)"
            Main->>Sq: "Run Square.handle_fleeing(squares)"
            Main->>Sq: "Move each square with delta_time"
            Main->>Sq: "Replace expired squares with new Square()"

            Main->>Pg: "Fill screen and draw squares"
            Main->>Pg: "Draw FPS text"
            Main->>Pg: "Flip display"
        end
    end

    Main->>Pg: "pygame.quit()"
```

## Assumptions and Observations

- The architecture is documented from `main.py` as the single executable source.
- The README mentions 10 squares, while code currently uses `NUM_SQUARES = 20`.
- No additional modules were inferred beyond what is explicitly imported or called.
