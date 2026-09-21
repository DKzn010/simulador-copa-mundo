import pygame
import random
import math
import sys

pygame.init()

WIDTH = 1920
HEIGHT = 1200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Copa do Mundo - 64 Seleções")

FONT = pygame.font.SysFont("arial", 30)
SMALL = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 44, bold=True)
TITLE = pygame.font.SysFont("arial", 56, bold=True)

WHITE = (255, 255, 255)

TEXT_BLACK = (20, 20, 20)

PANEL_BLACK = (15, 55, 130)

GRAY = (90, 90, 90)
LIGHT_GRAY = (220, 220, 220)
GREEN = (40, 160, 70)
BLUE = (40, 100, 200)
RED = (190, 50, 50)
YELLOW = (230, 190, 40)


TEAMS = [
    ("Brasil", 86),
    ("Argentina", 88),
    ("França", 87),
    ("Espanha", 86),
    ("Inglaterra", 85),
    ("Portugal", 85),
    ("Alemanha", 84),
    ("Países Baixos", 83),
    ("Itália", 82),
    ("Bélgica", 82),
    ("Croácia", 81),
    ("Uruguai", 81),
    ("Colômbia", 80),
    ("Marrocos", 80),
    ("Japão", 78),
    ("EUA", 77),
    ("México", 77),
    ("Suíça", 77),
    ("Dinamarca", 77),
    ("Turquia", 76),
    ("Senegal", 76),
    ("Coreia do Sul", 75),
    ("Irã", 74),
    ("Equador", 74),
    ("Áustria", 76),
    ("Ucrânia", 75),
    ("Polônia", 75),
    ("Sérvia", 74),
    ("Canadá", 74),
    ("Austrália", 73),
    ("Nigéria", 73),
    ("Egito", 72),
    ("Argélia", 72),
    ("Camarões", 71),
    ("Gana", 71),
    ("Costa do Marfim", 72),
    ("Tunísia", 70),
    ("África do Sul", 69),
    ("Catar", 68),
    ("Arábia Saudita", 70),
    ("Iraque", 67),
    ("Uzbequistão", 67),
    ("China", 65),
    ("Jordânia", 66),
    ("Chile", 74),
    ("Peru", 71),
    ("Paraguai", 73),
    ("Venezuela", 72),
    ("Costa Rica", 68),
    ("Panamá", 68),
    ("Jamaica", 67),
    ("Honduras", 64),
    ("Guatemala", 62),
    ("Bolívia", 62),
    ("Nova Zelândia", 62),
    ("Fiji", 55),
    ("RD Congo", 68),
    ("Mali", 69),
    ("Burkina Faso", 68),
    ("Grécia", 73),
    ("Escócia", 72),
    ("República Tcheca", 73),
    ("Romênia", 70),
    ("Índia", 58)
]


def draw_text(text, x, y, font=FONT, color=WHITE, center=False):
    surface = font.render(str(text), True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


def menu_panel(x=250, y=40, w=1420, h=1120):
    pygame.draw.rect(
        screen,
        PANEL_BLACK,
        (x, y, w, h),
        border_radius=25
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, w, h),
        4,
        border_radius=25
    )


def button(rect, text, active=True):
    x, y, w, h = rect

    color = BLUE if active else GRAY

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=12
    )

    draw_text(
        text,
        x + w // 2,
        y + h // 2,
        SMALL,
        WHITE,
        True
    )


def wait_enter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        pygame.time.delay(10)


def poisson(lam):
    l = math.exp(-lam)
    k = 0
    p = 1.0

    while p > l:
        k += 1
        p *= random.random()

    return k - 1


def simulate_match(team_a, team_b):
    name_a, rating_a = team_a
    name_b, rating_b = team_b

    difference = rating_a - rating_b

    base_a = 1.35 + difference * 0.035
    base_b = 1.35 - difference * 0.035

    base_a = max(0.25, min(3.5, base_a))
    base_b = max(0.25, min(3.5, base_b))

    goals_a = poisson(base_a)
    goals_b = poisson(base_b)

    return goals_a, goals_b


def automatic_penalties(team_a, team_b):
    score_a = 0
    score_b = 0

    for _ in range(5):
        score_a += random.choice([0, 1])
        score_b += random.choice([0, 1])

    if score_a != score_b:
        return score_a, score_b, False

    while True:
        a = random.choice([0, 1])
        b = random.choice([0, 1])

        score_a += a
        score_b += b

        if a != b:
            return score_a, score_b, True


def user_penalty_screen(team_a, team_b):
    input_a = "0"
    input_b = "0"

    active = 0
    sudden_death = False

    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "DISPUTA DE PÊNALTIS",
            WIDTH // 2,
            130,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            team_a[0],
            600,
            330,
            BIG,
            WHITE,
            True
        )

        draw_text(
            team_b[0],
            1320,
            330,
            BIG,
            WHITE,
            True
        )

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (450, 420, 300, 110),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (1170, 420, 300, 110),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 0 else GRAY,
            (450, 420, 300, 110),
            4,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 1 else GRAY,
            (1170, 420, 300, 110),
            4,
            border_radius=10
        )

        draw_text(
            input_a,
            600,
            475,
            BIG,
            TEXT_BLACK,
            True
        )

        draw_text(
            input_b,
            1320,
            475,
            BIG,
            TEXT_BLACK,
            True
        )

        checkbox = pygame.Rect(
            620,
            650,
            680,
            80
        )

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            checkbox,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            GREEN if sudden_death else GRAY,
            checkbox,
            4,
            border_radius=10
        )

        square = pygame.Rect(
            650,
            675,
            30,
            30
        )

        pygame.draw.rect(
            screen,
            WHITE,
            square
        )

        pygame.draw.rect(
            screen,
            PANEL_BLACK,
            square,
            2
        )

        if sudden_death:
            pygame.draw.line(
                screen,
                GREEN,
                (655, 690),
                (665, 700),
                5
            )

            pygame.draw.line(
                screen,
                GREEN,
                (665, 700),
                (678, 678),
                5
            )

        draw_text(
            "Gol de ouro",
            710,
            690,
            FONT,
            TEXT_BLACK,
            True
        )

        button(
            (760, 830, 400, 80),
            "CONFIRMAR",
            True
        )

        draw_text(
            "TAB = trocar campo | ESPAÇO = marcar gol de ouro",
            WIDTH // 2,
            970,
            SMALL,
            LIGHT_GRAY,
            True
        )

        draw_text(
            "O placar dos pênaltis deve ser diferente.",
            WIDTH // 2,
            1020,
            SMALL,
            LIGHT_GRAY,
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 450 <= mx <= 750 and 420 <= my <= 530:
                    active = 0

                elif 1170 <= mx <= 1470 and 420 <= my <= 530:
                    active = 1

                elif checkbox.collidepoint(mx, my):
                    sudden_death = not sudden_death

                elif 760 <= mx <= 1160 and 830 <= my <= 910:
                    if input_a != "" and input_b != "":
                        score_a = int(input_a)
                        score_b = int(input_b)

                        if score_a != score_b:
                            return score_a, score_b, sudden_death

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active = 1 - active

                elif event.key == pygame.K_SPACE:
                    sudden_death = not sudden_death

                elif event.key == pygame.K_BACKSPACE:
                    if active == 0:
                        input_a = input_a[:-1]
                    else:
                        input_b = input_b[:-1]

                elif event.key == pygame.K_RETURN:
                    if input_a != "" and input_b != "":
                        score_a = int(input_a)
                        score_b = int(input_b)

                        if score_a != score_b:
                            return score_a, score_b, sudden_death

                elif event.unicode.isdigit():
                    if active == 0:
                        if input_a == "0":
                            input_a = event.unicode
                        elif len(input_a) < 2:
                            input_a += event.unicode
                    else:
                        if input_b == "0":
                            input_b = event.unicode
                        elif len(input_b) < 2:
                            input_b += event.unicode

        clock.tick(60)


def show_penalty_result(team_a, team_b, score_a, score_b, sudden_death):
    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "RESULTADO DOS PÊNALTIS",
            WIDTH // 2,
            150,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            team_a[0],
            600,
            390,
            BIG,
            WHITE,
            True
        )

        draw_text(
            team_b[0],
            1320,
            390,
            BIG,
            WHITE,
            True
        )

        draw_text(
            str(score_a),
            600,
            520,
            TITLE,
            GREEN,
            True
        )

        draw_text(
            str(score_b),
            1320,
            520,
            TITLE,
            RED,
            True
        )

        if sudden_death:
            draw_text(
                "GOL DE OURO",
                WIDTH // 2,
                680,
                BIG,
                YELLOW,
                True
            )
        else:
            draw_text(
                "PÊNALTIS",
                WIDTH // 2,
                680,
                BIG,
                WHITE,
                True
            )

        winner = team_a if score_a > score_b else team_b

        draw_text(
            "Vencedor: " + winner[0],
            WIDTH // 2,
            790,
            BIG,
            GREEN,
            True
        )

        button(
            (760, 900, 400, 80),
            "CONTINUAR",
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return winner

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 760 <= mx <= 1160 and 900 <= my <= 980:
                    return winner


def ask_score(team_a, team_b):
    input_a = "0"
    input_b = "0"

    active = 0

    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "DIGITE O PLACAR",
            WIDTH // 2,
            140,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            team_a[0],
            600,
            350,
            BIG,
            WHITE,
            True
        )

        draw_text(
            team_b[0],
            1320,
            350,
            BIG,
            WHITE,
            True
        )

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (450, 430, 300, 100),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            (1170, 430, 300, 100),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 0 else GRAY,
            (450, 430, 300, 100),
            4,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 1 else GRAY,
            (1170, 430, 300, 100),
            4,
            border_radius=10
        )

        draw_text(
            input_a,
            600,
            480,
            BIG,
            TEXT_BLACK,
            True
        )

        draw_text(
            input_b,
            1320,
            480,
            BIG,
            TEXT_BLACK,
            True
        )

        button(
            (760, 700, 400, 80),
            "CONFIRMAR",
            True
        )

        draw_text(
            "TAB troca o campo",
            WIDTH // 2,
            900,
            SMALL,
            LIGHT_GRAY,
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 450 <= mx <= 750 and 430 <= my <= 530:
                    active = 0

                elif 1170 <= mx <= 1470 and 430 <= my <= 530:
                    active = 1

                elif 760 <= mx <= 1160 and 700 <= my <= 780:
                    if input_a != "" and input_b != "":
                        return int(input_a), int(input_b)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active = 1 - active

                elif event.key == pygame.K_BACKSPACE:
                    if active == 0:
                        input_a = input_a[:-1]
                    else:
                        input_b = input_b[:-1]

                elif event.key == pygame.K_RETURN:
                    if input_a != "" and input_b != "":
                        return int(input_a), int(input_b)

                elif event.unicode.isdigit():
                    if active == 0:
                        if input_a == "0":
                            input_a = event.unicode
                        elif len(input_a) < 2:
                            input_a += event.unicode
                    else:
                        if input_b == "0":
                            input_b = event.unicode
                        elif len(input_b) < 2:
                            input_b += event.unicode

        clock.tick(60)


def choose_team_screen():
    selected = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "ESCOLHA SUA SELEÇÃO",
            WIDTH // 2,
            80,
            TITLE,
            YELLOW,
            True
        )

        start = max(0, selected - 8)
        end = min(len(TEAMS), start + 16)

        for i in range(start, end):
            y = 180 + (i - start) * 50

            if i == selected:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (500, y - 5, 920, 42),
                    border_radius=8
                )

            name, rating = TEAMS[i]

            draw_text(
                name,
                530,
                y,
                FONT,
                WHITE
            )

            draw_text(
                "Força: " + str(rating),
                1200,
                y,
                FONT,
                WHITE
            )

        button(
            (760, 1050, 400, 80),
            "COMEÇAR",
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(TEAMS)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(TEAMS)

                elif event.key == pygame.K_RETURN:
                    return TEAMS[selected]

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 760 <= mx <= 1160 and 1050 <= my <= 1130:
                    return TEAMS[selected]

        clock.tick(60)


def create_groups(controlled):
    teams = TEAMS.copy()
    teams.remove(controlled)
    random.shuffle(teams)

    groups = []

    first_group = [controlled]
    first_group.extend(teams[:3])
    groups.append(first_group)

    remaining = teams[3:]

    for i in range(15):
        groups.append(
            remaining[i * 4:(i + 1) * 4]
        )

    return groups


def all_group_matches(group):
    matches = []

    for i in range(4):
        for j in range(i + 1, 4):
            matches.append(
                (group[i], group[j])
            )

    return matches


def create_table(group):
    table = {}

    for team in group:
        table[team[0]] = {
            "team": team,
            "P": 0,
            "V": 0,
            "E": 0,
            "D": 0,
            "GP": 0,
            "GC": 0,
            "SG": 0,
            "PTS": 0
        }

    return table


def add_result(table, team_a, team_b, goals_a, goals_b):
    a = table[team_a[0]]
    b = table[team_b[0]]

    a["P"] += 1
    b["P"] += 1

    a["GP"] += goals_a
    a["GC"] += goals_b

    b["GP"] += goals_b
    b["GC"] += goals_a

    if goals_a > goals_b:
        a["V"] += 1
        b["D"] += 1
        a["PTS"] += 3

    elif goals_b > goals_a:
        b["V"] += 1
        a["D"] += 1
        b["PTS"] += 3

    else:
        a["E"] += 1
        b["E"] += 1
        a["PTS"] += 1
        b["PTS"] += 1

    a["SG"] = a["GP"] - a["GC"]
    b["SG"] = b["GP"] - b["GC"]


def sort_table(table):
    return sorted(
        table.values(),
        key=lambda x: (
            x["PTS"],
            x["V"],
            x["SG"],
            x["GP"]
        ),
        reverse=True
    )


def show_group(group_number, group, table):
    clock = pygame.time.Clock()

    sorted_teams = sort_table(table)

    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "GRUPO " + chr(65 + group_number),
            WIDTH // 2,
            100,
            TITLE,
            YELLOW,
            True
        )

        headers = [
            "POS",
            "SELEÇÃO",
            "P",
            "V",
            "E",
            "D",
            "GP",
            "GC",
            "SG",
            "PTS"
        ]

        positions = [
            400,
            520,
            1080,
            1160,
            1240,
            1320,
            1400,
            1480,
            1560,
            1660
        ]

        for i, header in enumerate(headers):
            draw_text(
                header,
                positions[i],
                220,
                SMALL,
                WHITE,
                True
            )

        for index, data in enumerate(sorted_teams):
            y = 290 + index * 100

            if index < 2:
                pygame.draw.rect(
                    screen,
                    (30, 100, 50),
                    (350, y - 10, 1300, 75),
                    border_radius=8
                )

            values = [
                str(index + 1),
                data["team"][0],
                str(data["P"]),
                str(data["V"]),
                str(data["E"]),
                str(data["D"]),
                str(data["GP"]),
                str(data["GC"]),
                str(data["SG"]),
                str(data["PTS"])
            ]

            for i, value in enumerate(values):
                draw_text(
                    value,
                    positions[i],
                    y + 25,
                    SMALL,
                    WHITE,
                    True
                )

        button(
            (760, 1030, 400, 80),
            "CONTINUAR",
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 760 <= mx <= 1160 and 1030 <= my <= 1110:
                    return

        clock.tick(60)


def play_group(group_number, group, controlled):
    table = create_table(group)

    matches = all_group_matches(group)

    for team_a, team_b in matches:
        if team_a == controlled or team_b == controlled:
            goals_a, goals_b = ask_score(
                team_a,
                team_b
            )
        else:
            goals_a, goals_b = simulate_match(
                team_a,
                team_b
            )

        add_result(
            table,
            team_a,
            team_b,
            goals_a,
            goals_b
        )

    show_group(
        group_number,
        group,
        table
    )

    return sort_table(table)


def show_all_groups(group_results):
    current = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "CLASSIFICAÇÃO DOS GRUPOS",
            WIDTH // 2,
            80,
            TITLE,
            YELLOW,
            True
        )

        group = group_results[current]

        draw_text(
            "GRUPO " + chr(65 + current),
            WIDTH // 2,
            170,
            BIG,
            WHITE,
            True
        )

        for index, data in enumerate(group):
            y = 280 + index * 100

            if index < 2:
                pygame.draw.rect(
                    screen,
                    (30, 100, 50),
                    (500, y - 10, 920, 75),
                    border_radius=8
                )

            draw_text(
                str(index + 1),
                550,
                y + 20,
                FONT,
                WHITE
            )

            draw_text(
                data["team"][0],
                650,
                y + 20,
                FONT,
                WHITE
            )

            draw_text(
                str(data["PTS"]) + " pts",
                1200,
                y + 20,
                FONT,
                WHITE
            )

        draw_text(
            "← / → para trocar de grupo",
            WIDTH // 2,
            850,
            SMALL,
            LIGHT_GRAY,
            True
        )

        button(
            (760, 970, 400, 80),
            "CONTINUAR",
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current = (current - 1) % 16

                elif event.key == pygame.K_RIGHT:
                    current = (current + 1) % 16

                elif event.key == pygame.K_RETURN:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if 760 <= mx <= 1160 and 970 <= my <= 1050:
                    return

        clock.tick(60)


def knockout_match(team_a, team_b, controlled):
    if team_a == controlled or team_b == controlled:
        goals_a, goals_b = ask_score(
            team_a,
            team_b
        )
    else:
        goals_a, goals_b = simulate_match(
            team_a,
            team_b
        )

    if goals_a > goals_b:
        return team_a

    if goals_b > goals_a:
        return team_b

    if team_a == controlled or team_b == controlled:
        pen_a, pen_b, sudden = user_penalty_screen(
            team_a,
            team_b
        )
    else:
        pen_a, pen_b, sudden = automatic_penalties(
            team_a,
            team_b
        )

    winner = show_penalty_result(
        team_a,
        team_b,
        pen_a,
        pen_b,
        sudden
    )

    return winner


def knockout_round(teams, controlled, round_name):
    random.shuffle(teams)

    winners = []

    for i in range(0, len(teams), 2):
        team_a = teams[i]
        team_b = teams[i + 1]

        screen.fill(GREEN)
        menu_panel()

        draw_text(
            round_name,
            WIDTH // 2,
            120,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            team_a[0],
            600,
            400,
            BIG,
            WHITE,
            True
        )

        draw_text(
            "X",
            WIDTH // 2,
            400,
            BIG,
            YELLOW,
            True
        )

        draw_text(
            team_b[0],
            1320,
            400,
            BIG,
            WHITE,
            True
        )

        pygame.display.flip()
        pygame.time.delay(1000)

        winner = knockout_match(
            team_a,
            team_b,
            controlled
        )

        winners.append(winner)

        screen.fill(GREEN)
        menu_panel()

        draw_text(
            "VENCEDOR",
            WIDTH // 2,
            250,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            winner[0],
            WIDTH // 2,
            450,
            BIG,
            GREEN,
            True
        )

        button(
            (760, 800, 400, 80),
            "CONTINUAR",
            True
        )

        pygame.display.flip()

        wait_enter()

    return winners


def champion_screen(champion, controlled):
    screen.fill(GREEN)
    menu_panel()

    if champion == controlled:
        draw_text(
            "VOCÊ FOI CAMPEÃO!",
            WIDTH // 2,
            300,
            TITLE,
            YELLOW,
            True
        )

        draw_text(
            controlled[0],
            WIDTH // 2,
            500,
            BIG,
            GREEN,
            True
        )

        draw_text(
            "CAMPEÃO DA COPA DO MUNDO",
            WIDTH // 2,
            650,
            BIG,
            WHITE,
            True
        )

    else:
        draw_text(
            "VOCÊ FOI ELIMINADO",
            WIDTH // 2,
            300,
            TITLE,
            RED,
            True
        )

        draw_text(
            "CAMPEÃO:",
            WIDTH // 2,
            500,
            BIG,
            WHITE,
            True
        )

        draw_text(
            champion[0],
            WIDTH // 2,
            600,
            BIG,
            YELLOW,
            True
        )

    draw_text(
        "Pressione ENTER para fechar",
        WIDTH // 2,
        900,
        SMALL,
        LIGHT_GRAY,
        True
    )

    pygame.display.flip()

    wait_enter()


def main():
    controlled = choose_team_screen()

    groups = create_groups(controlled)

    group_results = []

    for i, group in enumerate(groups):
        result = play_group(
            i,
            group,
            controlled
        )

        group_results.append(result)

    show_all_groups(group_results)

    qualified = []

    for group in group_results:
        qualified.append(group[0]["team"])
        qualified.append(group[1]["team"])

    rounds = [
        "16-avos de final",
        "Oitavas de final",
        "Quartas de final",
        "Semifinal",
        "FINAL"
    ]

    teams = qualified

    for round_name in rounds:
        teams = knockout_round(
            teams,
            controlled,
            round_name
        )

    champion = teams[0]

    champion_screen(
        champion,
        controlled
    )


if __name__ == "__main__":
    main()