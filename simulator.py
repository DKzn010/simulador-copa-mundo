import pygame
import random
import math

pygame.init()

# ============================================================
# CONFIGURAÇÃO - 1920 x 1200
# ============================================================

WIDTH, HEIGHT = 1920, 1200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Copa do Mundo - 64 Seleções")

CLOCK = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 25)
GRAY = (55, 55, 65)
LIGHT_GRAY = (90, 90, 105)
GREEN = (40, 180, 90)
BLUE = (50, 120, 220)
RED = (210, 65, 65)
YELLOW = (235, 190, 50)

# Fontes maiores para 1920x1200
FONT = pygame.font.SysFont("arial", 30)
SMALL = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 44, bold=True)
TITLE = pygame.font.SysFont("arial", 56, bold=True)
TINY = pygame.font.SysFont("arial", 18)

# ============================================================
# 64 SELEÇÕES + OVERALL
# ============================================================

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
    ("Índia", 58),
]

OVR = dict(TEAMS)
NAMES = [name for name, _ in TEAMS]

# ============================================================
# FUNÇÕES GRÁFICAS
# ============================================================

def draw_text(text, pos, font=FONT, color=WHITE):
    surface = font.render(str(text), True, color)
    screen.blit(surface, pos)


def draw_center(text, center, font=FONT, color=WHITE):
    surface = font.render(str(text), True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)


def button(rect, text, active=False):
    rect = pygame.Rect(rect)

    color = GREEN if active else GRAY

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        LIGHT_GRAY,
        rect,
        3,
        border_radius=14
    )

    surface = FONT.render(text, True, WHITE)
    screen.blit(
        surface,
        surface.get_rect(center=rect.center)
    )


# ============================================================
# SIMULAÇÃO
# ============================================================

def poisson(lam):

    l = math.exp(-lam)
    k = 0
    p = 1.0

    while p > l:
        k += 1
        p *= random.random()

    return k - 1


def simulate_match(team_a, team_b):

    oa = OVR[team_a]
    ob = OVR[team_b]

    difference = oa - ob

    base_a = 1.35 + difference * 0.035
    base_b = 1.35 - difference * 0.035

    base_a = max(0.25, min(3.5, base_a))
    base_b = max(0.25, min(3.5, base_b))

    goals_a = poisson(base_a)
    goals_b = poisson(base_b)

    return goals_a, goals_b


def knockout_winner(team_a, team_b, goals_a, goals_b):

    if goals_a > goals_b:
        return team_a

    if goals_b > goals_a:
        return team_b

    oa = OVR[team_a]
    ob = OVR[team_b]

    probability_a = oa / (oa + ob)

    if random.random() < probability_a:
        return team_a

    return team_b


# ============================================================
# GRUPOS
# ============================================================

def create_groups(controlled):

    others = [x for x in NAMES if x != controlled]
    random.shuffle(others)

    groups = []

    group_a = [controlled] + others[:3]
    groups.append(group_a)

    remaining = others[3:]

    for i in range(0, len(remaining), 4):
        groups.append(remaining[i:i + 4])

    return groups


def all_group_matches(group):

    matches = []

    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            matches.append((group[i], group[j]))

    return matches


def create_table(group):

    table = {}

    for team in group:

        table[team] = {
            "P": 0,
            "V": 0,
            "E": 0,
            "D": 0,
            "GP": 0,
            "GC": 0,
            "SG": 0,
            "PTS": 0,
        }

    return table


def add_result(
    table,
    team_a,
    team_b,
    goals_a,
    goals_b
):

    table[team_a]["GP"] += goals_a
    table[team_a]["GC"] += goals_b

    table[team_b]["GP"] += goals_b
    table[team_b]["GC"] += goals_a

    table[team_a]["SG"] = (
        table[team_a]["GP"]
        - table[team_a]["GC"]
    )

    table[team_b]["SG"] = (
        table[team_b]["GP"]
        - table[team_b]["GC"]
    )

    if goals_a > goals_b:

        table[team_a]["V"] += 1
        table[team_a]["PTS"] += 3

        table[team_b]["D"] += 1

    elif goals_b > goals_a:

        table[team_b]["V"] += 1
        table[team_b]["PTS"] += 3

        table[team_a]["D"] += 1

    else:

        table[team_a]["E"] += 1
        table[team_b]["E"] += 1

        table[team_a]["PTS"] += 1
        table[team_b]["PTS"] += 1


def sort_table(table):

    return sorted(
        table.keys(),
        key=lambda team: (
            table[team]["PTS"],
            table[team]["SG"],
            table[team]["GP"],
            OVR[team],
        ),
        reverse=True
    )


# ============================================================
# JOGOS DA FASE DE GRUPOS
# ============================================================

def simulate_group_except_user(
    group,
    controlled,
    table
):

    matches = all_group_matches(group)

    for team_a, team_b in matches:

        if controlled in (team_a, team_b):
            continue

        ga, gb = simulate_match(
            team_a,
            team_b
        )

        add_result(
            table,
            team_a,
            team_b,
            ga,
            gb
        )


# ============================================================
# MATA-MATA
# ============================================================

def random_knockout_pairs(teams):

    teams = teams[:]
    random.shuffle(teams)

    pairs = []

    for i in range(0, len(teams), 2):
        pairs.append(
            (teams[i], teams[i + 1])
        )

    return pairs


# ============================================================
# ESCOLHER SELEÇÃO
# ============================================================

def choose_team_screen():

    selected = 0
    scroll = 0

    while True:

        screen.fill(BLACK)

        draw_center(
            "COPA DO MUNDO - 64 SELEÇÕES",
            (WIDTH // 2, 65),
            TITLE
        )

        draw_center(
            "Escolha a seleção que você vai controlar",
            (WIDTH // 2, 125),
            FONT
        )

        visible = 22

        for i in range(visible):

            index = scroll + i

            if index >= len(NAMES):
                break

            team = NAMES[index]

            rect = pygame.Rect(
                250,
                175 + i * 38,
                760,
                34
            )

            if index == selected:

                pygame.draw.rect(
                    screen,
                    BLUE,
                    rect,
                    border_radius=7
                )

            draw_text(
                f"{index + 1:02d}. {team}",
                (265, 179 + i * 38),
                SMALL
            )

            draw_text(
                f"OVR {OVR[team]}",
                (875, 179 + i * 38),
                SMALL,
                YELLOW
            )

        button(
            (1250, 870, 400, 80),
            "COMEÇAR",
            True
        )

        draw_text(
            "↑ ↓ = escolher",
            (250, 1080),
            SMALL,
            LIGHT_GRAY
        )

        draw_text(
            "ENTER = confirmar",
            (500, 1080),
            SMALL,
            LIGHT_GRAY
        )

        draw_text(
            "Clique também funciona",
            (800, 1080),
            SMALL,
            LIGHT_GRAY
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    selected -= 1

                elif event.key == pygame.K_DOWN:
                    selected += 1

                elif event.key == pygame.K_RETURN:
                    return NAMES[selected]

                selected = max(
                    0,
                    min(
                        len(NAMES) - 1,
                        selected
                    )
                )

                if selected < scroll:
                    scroll = selected

                if selected >= scroll + visible:
                    scroll = selected - visible + 1

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos

                if pygame.Rect(
                    1250,
                    870,
                    400,
                    80
                ).collidepoint(event.pos):

                    return NAMES[selected]

                for i in range(visible):

                    index = scroll + i

                    if index >= len(NAMES):
                        break

                    rect = pygame.Rect(
                        250,
                        175 + i * 38,
                        760,
                        34
                    )

                    if rect.collidepoint(mx, my):
                        selected = index


# ============================================================
# INPUT DE PLACAR
# ============================================================

def ask_score(team_a, team_b):

    home = ""
    away = ""
    active = 0

    while True:

        screen.fill(BLACK)

        draw_center(
            "SEU JOGO",
            (WIDTH // 2, 100),
            TITLE
        )

        draw_center(
            f"{team_a}   x   {team_b}",
            (WIDTH // 2, 200),
            BIG
        )

        draw_center(
            team_a,
            (500, 330),
            FONT
        )

        draw_center(
            team_b,
            (1420, 330),
            FONT
        )

        rect_home = pygame.Rect(
            400,
            390,
            300,
            150
        )

        rect_away = pygame.Rect(
            1220,
            390,
            300,
            150
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 0 else GRAY,
            rect_home,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            BLUE if active == 1 else GRAY,
            rect_away,
            border_radius=15
        )

        draw_center(
            home if home else "0",
            rect_home.center,
            TITLE
        )

        draw_center(
            away if away else "0",
            rect_away.center,
            TITLE
        )

        button(
            (710, 650, 500, 80),
            "CONFIRMAR",
            True
        )

        draw_center(
            "Digite os gols. TAB troca o campo.",
            (WIDTH // 2, 850),
            SMALL,
            LIGHT_GRAY
        )

        draw_center(
            "ENTER confirma",
            (WIDTH // 2, 890),
            SMALL,
            LIGHT_GRAY
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:

                if rect_home.collidepoint(event.pos):
                    active = 0

                elif rect_away.collidepoint(event.pos):
                    active = 1

                elif pygame.Rect(
                    710,
                    650,
                    500,
                    80
                ).collidepoint(event.pos):

                    return (
                        int(home or 0),
                        int(away or 0)
                    )

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:

                    active = 1 - active

                elif event.key == pygame.K_BACKSPACE:

                    if active == 0:
                        home = home[:-1]
                    else:
                        away = away[:-1]

                elif event.key == pygame.K_RETURN:

                    return (
                        int(home or 0),
                        int(away or 0)
                    )

                elif event.unicode.isdigit():

                    if active == 0 and len(home) < 2:
                        home += event.unicode

                    elif active == 1 and len(away) < 2:
                        away += event.unicode


# ============================================================
# MOSTRAR GRUPO
# ============================================================

def show_group(
    group,
    table,
    group_name
):

    while True:

        screen.fill(BLACK)

        draw_center(
            f"GRUPO {group_name}",
            (WIDTH // 2, 75),
            TITLE
        )

        draw_text(
            "POS",
            (250, 160),
            SMALL,
            YELLOW
        )

        draw_text(
            "SELEÇÃO",
            (340, 160),
            SMALL,
            YELLOW
        )

        draw_text(
            "PTS",
            (900, 160),
            SMALL,
            YELLOW
        )

        draw_text(
            "SG",
            (1020, 160),
            SMALL,
            YELLOW
        )

        draw_text(
            "OVR",
            (1140, 160),
            SMALL,
            YELLOW
        )

        sorted_teams = sort_table(table)

        for i, team in enumerate(sorted_teams):

            y = 230 + i * 85

            draw_text(
                str(i + 1),
                (255, y),
                FONT
            )

            draw_text(
                team,
                (340, y),
                FONT
            )

            draw_text(
                str(table[team]["PTS"]),
                (905, y),
                FONT
            )

            draw_text(
                str(table[team]["SG"]),
                (1025, y),
                FONT
            )

            draw_text(
                str(OVR[team]),
                (1145, y),
                FONT,
                YELLOW
            )

        button(
            (1400, 930, 350, 80),
            "CONTINUAR",
            True
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.Rect(
                    1400,
                    930,
                    350,
                    80
                ).collidepoint(event.pos):

                    return


# ============================================================
# TODOS OS GRUPOS
# ============================================================

def show_all_groups(
    groups,
    tables
):

    group_index = 0

    while True:

        screen.fill(BLACK)

        group = groups[group_index]
        table = tables[group_index]

        draw_center(
            f"GRUPO {chr(65 + group_index)}",
            (WIDTH // 2, 75),
            TITLE
        )

        sorted_teams = sort_table(table)

        for i, team in enumerate(sorted_teams):

            y = 220 + i * 105

            draw_text(
                f"{i + 1}.",
                (250, y),
                FONT
            )

            draw_text(
                team,
                (340, y),
                FONT
            )

            draw_text(
                f"{table[team]['PTS']} pts",
                (950, y),
                FONT
            )

            draw_text(
                f"SG {table[team]['SG']}",
                (1120, y),
                SMALL,
                LIGHT_GRAY
            )

            if i < 2:

                draw_text(
                    "CLASSIFICADO",
                    (1400, y),
                    SMALL,
                    GREEN
                )

        draw_text(
            f"Grupo {group_index + 1}/16",
            (250, 1050),
            SMALL,
            LIGHT_GRAY
        )

        draw_text(
            "← → muda o grupo",
            (250, 1090),
            SMALL,
            LIGHT_GRAY
        )

        draw_text(
            "ENTER continua",
            (1450, 1090),
            SMALL,
            LIGHT_GRAY
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    group_index -= 1

                elif event.key == pygame.K_RIGHT:
                    group_index += 1

                elif event.key == pygame.K_RETURN:
                    return

                group_index = max(
                    0,
                    min(15, group_index)
                )


# ============================================================
# MATA-MATA
# ============================================================

def knockout_round(
    teams,
    controlled,
    round_name
):

    pairs = random_knockout_pairs(teams)

    winners = []

    for team_a, team_b in pairs:

        screen.fill(BLACK)

        draw_center(
            round_name,
            (WIDTH // 2, 80),
            TITLE
        )

        draw_center(
            f"{team_a} x {team_b}",
            (WIDTH // 2, 230),
            BIG
        )

        draw_center(
            f"OVR {OVR[team_a]}       OVR {OVR[team_b]}",
            (WIDTH // 2, 310),
            FONT,
            YELLOW
        )

        pygame.display.flip()

        pygame.time.delay(700)

        if controlled in (team_a, team_b):

            ga, gb = ask_score(
                team_a,
                team_b
            )

        else:

            ga, gb = simulate_match(
                team_a,
                team_b
            )

        winner = knockout_winner(
            team_a,
            team_b,
            ga,
            gb
        )

        winners.append(winner)

        screen.fill(BLACK)

        draw_center(
            round_name,
            (WIDTH // 2, 90),
            TITLE
        )

        draw_center(
            f"{team_a} {ga} x {gb} {team_b}",
            (WIDTH // 2, 260),
            BIG
        )

        draw_center(
            f"PASSOU: {winner}",
            (WIDTH // 2, 400),
            BIG,
            GREEN
        )

        draw_center(
            "ENTER para continuar",
            (WIDTH // 2, 700),
            FONT
        )

        pygame.display.flip()

        waiting = True

        while waiting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    waiting = False

    return winners


# ============================================================
# CAMPEÃO
# ============================================================

def champion_screen(
    champion,
    controlled
):

    while True:

        screen.fill(BLACK)

        if champion == controlled:

            draw_center(
                "VOCÊ FOI CAMPEÃO!",
                (WIDTH // 2, 330),
                TITLE,
                GREEN
            )

            draw_center(
                f"{champion} conquistou a Copa!",
                (WIDTH // 2, 450),
                BIG
            )

        else:

            draw_center(
                "VOCÊ FOI ELIMINADO",
                (WIDTH // 2, 330),
                TITLE,
                RED
            )

            draw_center(
                f"Campeão: {champion}",
                (WIDTH // 2, 450),
                BIG,
                YELLOW
            )

        draw_center(
            "ENTER para fechar",
            (WIDTH // 2, 750),
            FONT
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return


# ============================================================
# MAIN
# ============================================================

def main():

    controlled = choose_team_screen()

    groups = create_groups(controlled)

    tables = []

    # ========================================================
    # FASE DE GRUPOS
    # ========================================================

    for index, group in enumerate(groups):

        table = create_table(group)

        if controlled in group:

            matches = all_group_matches(group)

            for team_a, team_b in matches:

                if controlled not in (
                    team_a,
                    team_b
                ):
                    continue

                goals_a, goals_b = ask_score(
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

            simulate_group_except_user(
                group,
                controlled,
                table
            )

        else:

            simulate_group_except_user(
                group,
                None,
                table
            )

        tables.append(table)

        show_group(
            group,
            table,
            chr(65 + index)
        )

    # ========================================================
    # MOSTRA TODOS OS GRUPOS
    # ========================================================

    show_all_groups(
        groups,
        tables
    )

    # ========================================================
    # CLASSIFICADOS
    # ========================================================

    qualified = []

    for table in tables:

        ranking = sort_table(table)

        qualified.extend(
            ranking[:2]
        )

    qualified = qualified[:32]

    # ========================================================
    # MATA-MATA
    # ========================================================

    teams = qualified

    round_names = [
        "16-avos de final",
        "Oitavas de final",
        "Quartas de final",
        "Semifinal",
        "FINAL"
    ]

    for round_name in round_names:

        if len(teams) == 1:
            break

        teams = knockout_round(
            teams,
            controlled,
            round_name
        )

    champion = teams[0]

    # ========================================================
    # CAMPEÃO
    # ========================================================

    champion_screen(
        champion,
        controlled
    )

    pygame.quit()


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()

