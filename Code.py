from cProfile import label
from manim import *

template = TexTemplate()
template.add_to_preamble(r"\usepackage{wasysym}")

# Table scene
class TableScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        table_data = [
            ["", ""],
            ["", ""],
        ]
        
        table = Table(
            table_data,
            row_labels=[MathTex(r"\text{Impuls} \ p"), MathTex(r"\text{Energie} \ E")],
            col_labels=[MathTex(r"\text{Teilchen}"), MathTex(r"\text{Welle}")],
            include_outer_lines=False,
            line_config={"stroke_width": 2},
        ).scale(1.5).set_color(BLACK)
        
        self.wait(1)
        self.play(Create(table))
        self.wait(1)

        p_t = MathTex(r"mv", color=BLACK).move_to(table.get_cell((2, 2)).get_center())
        E_t = MathTex(r"\frac{1}{2}mv^2", color=BLACK).move_to(table.get_cell((3, 2)).get_center())
        p_w = MathTex(r"\frac{h}{\lambda}", color=BLACK).move_to(table.get_cell((2, 3)).get_center())
        E_w0 = MathTex(r"hf", color=BLACK).move_to(table.get_cell((3, 3)).get_center())
        E_w = MathTex(r"\frac{hc}{\lambda}", color=BLACK).move_to(table.get_cell((3, 3)).get_center())

        self.play(Write(p_t))
        self.wait(1)
        self.play(Write(E_t))
        self.wait(1)
        self.play(Write(p_w))
        self.wait(1)
        self.play(Write(E_w0))
        self.wait(1)
        self.play(Transform(E_w0, E_w))
        self.wait(2)

#Intro, Titel etc
class Szene0(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        quanti = Text("Quantisierung des Lichts", color=BLACK).scale(1.2)
        self.play(Write(quanti))
        self.wait(2)

        arrow = Arrow(UP, DOWN, color=BLACK).next_to(quanti, DOWN, buff=0.5)
        self.play(Create(arrow))
        
        photoe = Text("Photoelektrischer Effekt", color=BLACK).scale(0.8).next_to(arrow, DOWN, buff=0.5)
        self.play(Write(photoe))
        self.wait(2)

        group = VGroup(quanti, arrow, photoe)

        self.play(
            AnimationGroup(
                group.animate.shift(12 * LEFT),
                lag_ratio=0
            ),
            run_time=2
        )

        neuerE = Text("Quantisierung der Leitfähigkeit", color=BLACK).scale(1.2).shift(14 * RIGHT)
        self.play(Write(neuerE))
        self.play(
            AnimationGroup(
                neuerE.animate.shift(14 * LEFT),
                lag_ratio=0
            ),
            run_time=2
        )
        self.wait(2)

#Stromkreis
class Szene1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE

        board = RoundedRectangle(
            corner_radius=0.5,
            width = 7,
            height = 5.5,
            fill_color=GRAY,
            fill_opacity=1,
        ).shift(UP * 0.25)
        self.add(board)

        top_left = LEFT * 3 + UP * 1.5
        top_right = RIGHT * 3 + UP * 1.5
        bottom_left = LEFT * 3 + DOWN * 1.5
        bottom_right = RIGHT * 3 + DOWN * 1.5
        source = Circle(radius=0.4, color=BLACK).move_to(DOWN * 1.5)
        plus = MathTex("+", color=BLACK).next_to(source, DOWN + RIGHT, buff=0.1)
        minus = MathTex("-", color=BLACK).next_to(source, DOWN + LEFT, buff=0.1)
        minus.set_y(plus.get_y())
        bottom_left_line = Line(bottom_left, source.get_left(), color=BLACK)
        bottom_right_line = Line(source.get_right(), bottom_right, color=BLACK)
        left_wire = Line(bottom_left, top_left, color=BLACK)
        right_wire = Line(bottom_right, top_right, color=BLACK)
        top_cross1 = Line(top_left, RIGHT * 0.2 + UP * 2.5, color=GOLD)
        top_cross2 = Line(top_right, LEFT * 0.2 + UP * 2.5, color=GOLD)
        cross_intersection_height = UP * (1.5 + 3/(0.2+3))
        circuit = VGroup(
            bottom_left_line,
            bottom_right_line,
            left_wire,
            right_wire,
            top_cross1,
            top_cross2,
            source,
            plus,
            minus,
        )
        self.play(Create(circuit))

        electron_path = VMobject()
        electron_path.set_points_as_corners([
            source.get_left(),
            bottom_left,
            top_left,
            UP * cross_intersection_height,
            top_right,
            bottom_right,
            source.get_left()
        ])

        electron_trackers = [ValueTracker(i / 6) for i in range(6)]
        electrons = VGroup(*[
            Dot(color=BLUE).move_to(electron_path.point_from_proportion(tracker.get_value()))
            for tracker in electron_trackers
        ])
        for electron, tracker in zip(electrons, electron_trackers):
            electron.add_updater(
                lambda m, a=tracker: (
                    m.move_to(electron_path.point_from_proportion(a.get_value() % 1)),
                    m.set_opacity(0 if np.linalg.norm(m.get_center() - source.get_center()) < source.radius else 1)
                )
            )

        self.play(FadeIn(electrons))
        laps = 0.5
        electron_speed = 1
        lap_length = electron_path.get_arc_length() * laps
        self.play(
            *[tracker.animate.set_value(tracker.get_value() + laps) for tracker in electron_trackers],
            run_time=lap_length/electron_speed,
            rate_func=linear,
        )
        for electron in electrons:
            electron.clear_updaters()
        
        glass = Circle(radius=0.5, color=DARK_BLUE).move_to(UP * 2.35)
        handle = Line(
            glass.get_center() + 0.5*np.sin(np.pi/4) * DR,
            glass.get_center() + 1 * DR,
            color=DARK_BLUE,
        )
        target_position = UP * 2.35
        magnifying_glass = VGroup(glass, handle)
        start_pos = target_position + 8 * RIGHT + 4 * DOWN
        magnifying_glass.shift(start_pos - glass.get_center())
        self.play(FadeIn(magnifying_glass))
        self.play(magnifying_glass.animate.shift(target_position - glass.get_center()), run_time=2)
        self.play(
            self.camera.frame.animate.set(width=2.5).move_to(magnifying_glass.get_center() + UP * 0.2),
            FadeOut(board),
            run_time=2
            )
        self.wait()


        for electron, tracker in zip(electrons, electron_trackers):
            electron.add_updater(
                lambda m, a=tracker: (
                    m.move_to(electron_path.point_from_proportion(a.get_value() % 1)),
                    m.set_opacity(0 if np.linalg.norm(m.get_center() - source.get_center()) < source.radius else 1)
                )
            )
        self.play(
            *[tracker.animate.set_value(tracker.get_value() + laps) for tracker in electron_trackers],
            run_time=lap_length/electron_speed,
            rate_func=linear,
        )
        for electron in electrons:
            electron.clear_updaters()

        self.play(
            FadeOut(electrons),
            top_cross1.animate.put_start_and_end_on(top_left, RIGHT * 0.18 + UP * 2.75),
            run_time=2,
        )
        self.play(self.camera.frame.animate.shift(RIGHT * 0.5), run_time=2)
        text1 = Tex(r"\lightning\ ", tex_template=template, color=RED, font_size=24).next_to(glass, RIGHT, buff=0.2).shift(UP * 0.01)
        text2 = Tex(r"Kein \\ Strom!", tex_template=template, color=BLACK, font_size=24).next_to(text1, RIGHT, buff=0.2).shift(UP * 0.01)
        self.play(Write(text1), Write(text2))
        self.wait(1)
        
        self.play(self.camera.frame.animate.shift(LEFT * 0.5), run_time=2)
        self.play(
            FadeOut(VGroup(
                bottom_left_line,
                bottom_right_line,
                left_wire,
                right_wire,
                source,
                plus,
                minus,
                text1,
                text2,
            )),
            run_time=0.5,
        )

        self.play(
            FadeOut(magnifying_glass),
            top_cross1.animate.put_start_and_end_on(LEFT * 0.25 + UP * 2.1, RIGHT * 0.25 + UP * 2.6),
            top_cross2.animate.put_start_and_end_on(RIGHT * 0.25 + UP * 2.1, LEFT * 0.25 + UP * 2.6),
            run_time=1,
        )
        self.play(
            self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN),
            top_cross1.animate.put_start_and_end_on(LEFT * 4 + DOWN * 3, RIGHT * 2 + UP * 3).set_stroke(width=16),
            top_cross2.animate.put_start_and_end_on(RIGHT * 4 + DOWN * 3, LEFT * 2 + UP * 3).set_stroke(width=16),
            run_time=1,
        )

#Nanodraht bildet sich
class Szene1_2(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        top_cross1 = Line(LEFT * 4 + DOWN * 3, RIGHT * 2 + UP * 3, color=GOLD, stroke_width=16)
        top_cross2 = Line(RIGHT * 4 + DOWN * 3, LEFT * 2 + UP * 3, color=GOLD, stroke_width=16)
        self.play(Create(top_cross1), Create(top_cross2))
        self.wait(1)

        left_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(-PI/4, about_point=ORIGIN)
        right_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(PI/4, about_point=ORIGIN)
        left_wire.shift(LEFT)
        right_wire.shift(RIGHT)
        self.play(Create(right_wire), Create(left_wire), FadeOut(top_cross1), FadeOut(top_cross2))
        self.wait(1)

        self.play(
            left_wire.animate.rotate(PI/4, about_point=ORIGIN).move_to([-0.1, left_wire.get_y(), 0]).set_height(6).set(width=0.2),
            right_wire.animate.rotate(-PI/4, about_point=ORIGIN).move_to([0.1, right_wire.get_y(), 0]).set_height(6).set(width=0.2),
            run_time=2,
        )

        glass = Circle(radius=0.5, color=DARK_BLUE)
        magnifying_glass = VGroup(
            glass,
            Line(
                0.5*np.sin(np.pi/4) * DR,
                1 * DR,
                color=DARK_BLUE,
            )
        ).shift(RIGHT * 9 + DOWN * 2)
        self.play(Create(magnifying_glass), run_time=0.1)
        self.play(magnifying_glass.animate.shift(LEFT * 9 + UP * 2), run_time=2)
        self.wait(1)

        wire_width = 10
        self.play(
            left_wire.animate.set(width=0.2+wire_width).shift(LEFT * wire_width/2),
            right_wire.animate.set(width=0.2+wire_width).shift(RIGHT * wire_width/2),
            magnifying_glass.animate.scale(20, about_point=glass.get_center()),
            run_time=2,
        )


        
        nano_num = 7
        nano_width = 2
        atom_radius = 0.12
        atom_radius = nano_width/(2*nano_num)
        atom_height = -1

        atoms = VGroup(*[
            Dot(
                point=LEFT * ((nano_width-2*atom_radius)/(nano_num-1)*i - nano_width/2+atom_radius) + UP * atom_height,
                radius=atom_radius,
                color=GOLD,
            ).set_stroke(color=BLACK, width=0.5)
            for i in range(nano_num)
        ])

        # Length L marker below the atoms
        L_label = MathTex("L", color=BLACK).next_to(atoms, DOWN, buff=0.5)
        L_arrows = VGroup(
            Arrow(L_label.get_left(), L_label.get_left() + LEFT * 0.8, buff=0, color=BLACK),
            Arrow(L_label.get_right(), L_label.get_right() + RIGHT * 0.8, buff=0, color=BLACK),
        )

        atoms.set_z_index(-10)
        L_label.set_z_index(-10)
        L_arrows.set_z_index(-10)
        self.add(atoms, L_label, L_arrows)
        self.wait(1)
        self.play(
                left_wire.animate.shift(LEFT * 1),
                right_wire.animate.shift(RIGHT * 1),
                run_time=2,
        )


        minus_sign = MathTex("-").scale(1.5).next_to(atoms[0], LEFT, buff=0.5).set_color(BLACK).shift(LEFT*1.5)
        plus_sign = MathTex("+").scale(1.5).next_to(atoms[-1], RIGHT, buff=0.5).set_color(BLACK).shift(RIGHT*1.5)
        minus_sign.set_y(plus_sign.get_y())
        self.add(minus_sign, plus_sign)
        self.wait(1)

#Leitwert im Draht, Elektronen im Draht, Dichten
class Szene1_4(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        Draht_rect = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(-PI/4, about_point=ORIGIN)
        self.play(Write(Draht_rect))
        self.play(
            Draht_rect.animate.rotate(-PI/4, about_point=ORIGIN)
        )
        Draht_upper = Line(LEFT*3*np.sqrt(2) + UP*0.1, RIGHT*3*np.sqrt(2) + UP*0.1, color=BLACK)
        Draht_lower = Line(LEFT*3*np.sqrt(2) - UP*0.1, RIGHT*3*np.sqrt(2) - UP*0.1, color=BLACK)
        Draht = VGroup(Draht_rect, Draht_upper, Draht_lower)
        self.play(Write(Draht_upper), Write(Draht_lower))

        self.play(
            Draht.animate.scale([1.4, 30, 1])
        )
        wire_length = 42*np.sqrt(2)/5

        White_hider = VGroup(
            Rectangle(width=3, height=8, color=WHITE).set_fill(color=WHITE, opacity=1).next_to(Draht, LEFT, buff=0),
            Rectangle(width=3, height=8, color=WHITE).set_fill(color=WHITE, opacity=1).next_to(Draht, RIGHT, buff=0)
        )
        White_hider.set_z_index(+10)
        self.add(White_hider)

        # Elektronen
        electron_positions = [
            LEFT * 5 + UP * 1,
            LEFT * 2 + DOWN * 2,
            ORIGIN,
            RIGHT * 2 + UP * 2,
            RIGHT * 5 + DOWN * 1
        ]
        electrons = VGroup()
        shift = wire_length * LEFT
        num = 10
        for pos in electron_positions:
            electron_balls = [Dot(radius=0.3, color=BLUE).move_to(pos + shift * i) for i in range(num)]
            electron_signs = [MathTex("-", color=WHITE).move_to(electron_balls[i]) for i in range(num)]
            for b, s in zip(electron_balls, electron_signs):
                electron = VGroup(b, s)
                electrons.add(electron)
        self.play(FadeIn(electrons))
        self.electrons = electrons
        self.electron_positions = electron_positions

        self.play(
            Draht.animate.shift(DOWN * 0.8),
            electrons.animate.shift(DOWN * 0.8)
        )


        description = MathTex(
            f"U = R \\cdot I", "\\Rightarrow", f"I=\\frac{{U}}{{R}}"
        ).to_edge(UP).set_color(BLACK).set_z_index(+11)
        
        self.play(Write(description[0]))
        self.wait(1)
        self.play(Write(description[1]))
        self.play(Write(description[2]))
        


        R = 1
        R_label = MathTex(
            f"R={R} \Omega"
        ).to_edge(UP).set_color(BLACK)

        updated_description = MathTex(
            f"I = U / R"
        ).next_to(R_label, LEFT).set_color(BLACK).set_z_index(+11).to_edge(LEFT).align_to(Draht, LEFT)
        self.play(Transform(description, updated_description))
        self.wait(1)


        self.play(Write(R_label))


        minus_sign = MathTex("-", color=BLACK).next_to(Draht, LEFT, buff=0.1)
        plus_sign  = MathTex("+", color=BLACK).next_to(Draht, RIGHT, buff=0.1)
        signs = VGroup(minus_sign, plus_sign)
        signs.set_z_index(+11)
        self.play(
            Write(signs)
        )

        #Animieren
        self.play(
            electrons.animate.shift(RIGHT*wire_length*2),
            run_time = 1 * 2 / 1,
            rate_func = linear
        )
        electrons.shift(LEFT*wire_length*2)
        R = 1 / 2
        self.remove(R_label)
        R_label = MathTex(
            f"R={R} \Omega"
        ).to_edge(UP).set_color(BLACK)
        self.add(R_label)
        self.play(
            electrons.animate.shift(RIGHT*wire_length*4),
            run_time = 1 * 4 / 2,
            rate_func = linear
        )
        electrons.shift(LEFT*wire_length*4)
        
        R = 1 / 4
        self.remove(R_label)
        R_label = MathTex(
            f"R={R} \Omega"
        ).to_edge(UP).set_color(BLACK)
        self.add(R_label)
        self.play(
            electrons.animate.shift(RIGHT*wire_length*8),
            run_time = 1 * 8 / 4,
            rate_func = linear
        )
        electrons.shift(LEFT*wire_length*8)
        self.play(FadeOut(signs))
        
        self.wait(2)

        self.play(FadeOut(R_label), FadeOut(description))
        self.remove(electrons)
        electrons = VGroup()
        for pos in electron_positions:
            electron_ball = Dot(radius=0.3, color=BLUE).move_to(pos)
            electron_sign = MathTex("-", color=WHITE).move_to(electron_ball)
            electron = VGroup(electron_ball, electron_sign)
            electrons.add(electron)
        electrons.move_to(DOWN*0.8)
        self.add(electrons)
        self.play(
            Draht.animate.scale(0.8),
            electrons.animate.scale(0.8)
        )
        
        length = MathTex(
            r"\text{Länge}\;L"
        ).set_color(BLACK).next_to(Draht, UP, buff=0.1)
        arrows = VGroup(
            Arrow(length.get_left(), length.get_left()+LEFT*4.1, color=BLACK),
            Arrow(length.get_right(), length.get_right()+RIGHT*4.1, color=BLACK)
        )
        self.play(Write(length), Create(arrows))

        density = MathTex(
            r"\text{Elektronenanzahl}\;N"
        ).set_color(BLACK).to_edge(UP)
        self.play(Write(density))
        self.wait(1)

#Stehende Wellen
class Szene1_3(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        left_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(-PI/4, about_point=ORIGIN).shift(LEFT * 1)
        right_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(PI/4, about_point=ORIGIN).shift(RIGHT * 1)
        
        left_wire.rotate(PI/4, about_point=ORIGIN).move_to([-0.1, left_wire.get_y(), 0]).set_height(6).set(width=0.2)
        right_wire.rotate(-PI/4, about_point=ORIGIN).move_to([0.1, right_wire.get_y(), 0]).set_height(6).set(width=0.2)
        
        wire_width = 10
        left_wire.set(width=0.2+wire_width).shift(LEFT * wire_width/2)
        right_wire.set(width=0.2+wire_width).shift(RIGHT * wire_width/2)
        

        nano_num = 7
        nano_width = 2
        atom_radius = 0.12
        atom_radius = nano_width/(2*nano_num)
        atom_height = -1

        threshold = ValueTracker(0)
        atoms = VGroup(*[
            Dot(
                point=LEFT * ((nano_width-2*atom_radius)/(nano_num-1)*i - nano_width/2+atom_radius) + UP * atom_height,
                radius=atom_radius,
                color=GOLD,
            ).set_stroke(color=BLACK, width=0.5)
            for i in range(nano_num)
        ])

        L_label = MathTex("L", color=BLACK).next_to(atoms, DOWN, buff=0.5)
        L_arrows = VGroup(
            Arrow(L_label.get_left(), L_label.get_left() + LEFT * 0.8, buff=0, color=BLACK),
            Arrow(L_label.get_right(), L_label.get_right() + RIGHT * 0.8, buff=0, color=BLACK),
        )

        atoms.set_z_index(-10)
        L_label.set_z_index(-10)
        L_arrows.set_z_index(-10)
        left_wire.shift(LEFT * 1)
        right_wire.shift(RIGHT * 1)

        L = 1
        N = 100

        baseline = Line(LEFT * 1 + DOWN * 1, RIGHT * 1 + DOWN * 1, color = BLACK, stroke_width = 3)
        baseline.set_opacity(0.5)
        
        self.play(FadeIn(left_wire), FadeIn(right_wire), FadeIn(atoms))
        self.play(Create(baseline))
        self.play(Write(L_label), Create(L_arrows))


        self.wait(2)

        import math
        psi = [math.sin(2 * math.pi * i / N) for i in range(N)]
        amp = 0.4 * L
        sine_points = [
            LEFT * (2 - L * i / (N - 1)) + UP * (-1 + amp * psi[i])
            for i in range(N)
        ]
        sine_line = VMobject()
        sine_line.set_points_smoothly(sine_points)
        sine_line.set_color(BLUE)
        sine_line.set_stroke(width=3)
        sine_line.set_z_index(-5)
        self.add(sine_line)


        psi = [math.sin(2 * math.pi * i / N) for i in range(N)]
        amp = 0.4 * L
        sine_points = [
            LEFT * (-3 - L * i / (N - 1)) + UP * (-1 + amp * psi[i])
            for i in range(N)
        ]
        sine_line_2 = VMobject()
        sine_line_2.set_points_smoothly(sine_points)
        sine_line_2.set_color(RED)
        sine_line_2.set_stroke(width=3)
        sine_line_2.set_z_index(-5)
        self.add(sine_line_2)

        self.play(
            sine_line.animate.shift(RIGHT * 5),
            sine_line_2.animate.shift(LEFT * 5),
            run_time = 5,
            rate_func = linear
        )

        self.play(FadeOut(sine_line), FadeOut(sine_line_2), L_label.animate.shift(DOWN), L_arrows.animate.shift(DOWN))
        self.wait(1)
        
        L = 2
        num = 2
        psi = [math.sin(2 * math.pi * num/2 * i / N) for i in range(N)]
        amp = 0.4 * L
        sine_points = [
            LEFT * (L/2 - L * i / (N - 1)) + UP * (-1 + amp * psi[i])
            for i in range(N)
        ]
        sine_wave = VMobject()
        sine_wave.set_points_smoothly(sine_points)
        sine_wave.set_color(RED)
        sine_wave.set_stroke(width=3)
        sine_wave.set_z_index(-5)
        self.play(FadeIn(sine_wave))
        self.wait(2)

        def sine_rate(t):
            return np.sin(t*2*np.pi*1/2 - np.pi/2) / 2 + 0.5
        
        for _ in range(6):
            self.play(
                sine_wave.animate.stretch(-1, dim=1),
                run_time=0.5,
                rate_func = sine_rate
                )
        self.play(FadeOut(sine_wave))
        self.wait(1)
        

        num = 2
        L=4
        psi = [math.sin(2 * math.pi * num/2 * i / N) for i in range(N)]
        amp = 0.4 * 2
        sine_points = [
            LEFT * (1 - L * i / (N - 1)) + UP * (-1 + amp * psi[i])
            for i in range(N)
        ]
        sine_wave = VMobject()
        sine_wave.set_points_smoothly(sine_points)
        sine_wave.set_color(RED)
        sine_wave.set_stroke(width=3)
        sine_wave.set_z_index(-5)
        self.play(FadeIn(sine_wave))
        self.wait(2)
        for _ in range(6):
            self.play(
                sine_wave.animate.stretch(-1, dim=1),
                run_time=0.5,
                rate_func = sine_rate
                )
        self.play(FadeOut(sine_wave))
        self.wait(1)


        num = 4
        L=8/3
        psi = [math.sin(2 * math.pi * num/2 * i / N) for i in range(N)]
        amp = 0.4 * 2
        sine_points = [
            LEFT * (1 - L * i / (N - 1)) + UP * (-1 + amp * psi[i])
            for i in range(N)
        ]
        sine_wave = VMobject()
        sine_wave.set_points_smoothly(sine_points)
        sine_wave.set_color(RED)
        sine_wave.set_stroke(width=3)
        sine_wave.set_z_index(-5)
        self.play(FadeIn(sine_wave))
        self.wait(2)
        for _ in range(6):
            self.play(
                sine_wave.animate.stretch(-1, dim=1),
                run_time=0.5,
                rate_func = sine_rate
                )
        self.play(FadeOut(sine_wave), FadeOut(baseline))
        self.wait(2)
        self.play(FadeOut(atoms), FadeOut(L_label), FadeOut(L_arrows), FadeOut(left_wire), FadeOut(right_wire))


class PotentialTopf(Scene):
    def construct(self):
        def highlight(text):
            o_color = text.get_color()
            self.play(text.animate.set_color(RED))
            self.wait(0.25)
            self.play(text.animate.set_color(BLACK))
            self.wait(1)
        self.camera.background_color = WHITE
        axes = Axes(
            x_range=(-8, 8, 1),
            y_range=(-2, 5, 1),
            x_length=17,
            y_length=8,
            axis_config={"include_numbers": True, "color": BLACK, "decimal_number_config": {"num_decimal_places": 0}},
        )
        for label in axes.get_x_axis().numbers + axes.get_y_axis().numbers:
            label.set_color(BLACK)


        L=4
        width=0.5
        height=4.5
        topf = Polygon(
            axes.c2p(L/2, height),
            axes.c2p(L/2+width, height),
            axes.c2p(L/2+width, -1),
            axes.c2p(-L/2-width, -1),
            axes.c2p(-L/2-width, height),
            axes.c2p(-L/2, height),
            axes.c2p(-L/2, -0.5),
            axes.c2p(L/2, -0.5),
            color=GRAY, fill_opacity=0.5
        )
        outline = VGroup(
            Line(axes.c2p(-L/2, height), axes.c2p(-L/2, -0.5), color=BLACK),
            Line(axes.c2p(L/2, height), axes.c2p(L/2, -0.5), color=BLACK),
            Line(axes.c2p(-L/2, -0.5), axes.c2p(L/2, -0.5), color=BLACK)
        )

        L_label = MathTex("L", color=BLACK).move_to(axes.c2p(0, -1.5))
        L_arrows = VGroup(
            Arrow(axes.c2p(0.5, -1.5), axes.c2p(L/2, -1.5), buff=0, color=BLACK),
            Arrow(axes.c2p(-0.5, -1.5), axes.c2p(-L/2, -1.5), buff=0, color=BLACK)
        )
        dotted_lines = VGroup(
            DashedLine(axes.c2p(-L/2, -1.75), axes.c2p(-L/2, -0.5), color=BLACK),
            DashedLine(axes.c2p(L/2, -1.75), axes.c2p(L/2, -0.5), color=BLACK)
        )
        Energy_arrow = Arrow(axes.c2p(L/2+width/2, height), axes.c2p(L/2+width/2, height+0.5), buff=0, color=BLACK)
        Energy_label = Tex("Energie", color=BLACK).next_to(axes.c2p(L/2+width/2, height+0.5-0.25), RIGHT, buff=0.25)
        


        lambdas = [2*L, L, 2*L/3]
        
        sines = []
        heights = []
        i_labels = []
        lambda_labels = []
        for idx, lam in enumerate(lambdas):
            i = idx + 1
            y_offset = idx**2
            sine = axes.plot(lambda x, l=lam, y=y_offset: 0.5*np.sin(2*np.pi/l*(x+L/2))+y, x_range=(-L/2, L/2), color=BLUE)
            height = axes.plot(lambda x, y=y_offset: y, x_range=(-L/2-width/3, L/2+width/3), color=BLACK)
            i_label = MathTex(f"i={i}", color=BLACK).next_to(sine, LEFT, buff=1)
            sines.append(sine)
            heights.append(height)
            i_labels.append(i_label)
        lambda_labels.append(MathTex(f"\\lambda_{{{1}}}=2 L", color=BLACK).next_to(sines[0], RIGHT, buff=1))
        lambda_labels.append(MathTex(f"\\lambda_{{{2}}}=L", color=BLACK).next_to(sines[1], RIGHT, buff=1))
        lambda_labels.append(MathTex(f"\\lambda_{{{3}}}=\\frac{{2 L}}{{3}}", color=BLACK).next_to(sines[2], RIGHT, buff=1))

        self.play(FadeIn(topf), Create(outline))
        self.wait(0.5)
        self.play(Write(L_label), FadeIn(*L_arrows), FadeIn(*dotted_lines), FadeIn(Energy_arrow), Write(Energy_label))
        self.wait(2)
        self.play(FadeIn(heights[0]), FadeIn(sines[0]), Write(i_labels[0]), Write(lambda_labels[0]))
        self.wait(2)
        self.play(FadeIn(heights[1]), FadeIn(sines[1]), Write(i_labels[1]), Write(lambda_labels[1]))
        self.wait(2)
        self.play(FadeIn(heights[2]), FadeIn(sines[2]), Write(i_labels[2]), Write(lambda_labels[2]))
        self.wait(2)

        con_label = MathTex(
            f"i \\cdot \\frac{{\\lambda}}{{2}} = L"
        ).set_color(BLACK).next_to(lambda_labels[2], DOWN, buff=1)
        con_label_2 = MathTex(
            f"\\lambda_{{i}}=\\frac{{2L}}{{i}}"
        ).set_color(BLACK).next_to(lambda_labels[2], DOWN, buff=1)
        self.play(Write(con_label))

        everything = VGroup(
            *sines, *heights, topf, *dotted_lines, outline, *L_arrows, Energy_arrow, Energy_label, *i_labels, *lambda_labels, L_label
        )
        


        table_data = [
            ["", ""],
            ["", ""],
        ]
        table = Table(
            table_data,
            row_labels=[MathTex(r"\text{Impuls} \ p"), MathTex(r"\text{Energie} \ E")],
            col_labels=[MathTex(r"\text{Teilchen}"), MathTex(r"\text{Welle}")],
            include_outer_lines=False,
            line_config={"stroke_width": 2},
        ).scale(1.5).set_color(BLACK)

        self.play(everything.animate.move_to(LEFT*14), con_label.animate.move_to(table.get_cell((1, 1)).get_center()))
        con_label_2.move_to(table.get_cell((1, 1)).get_center())
        self.play(FadeOut(everything))
        self.play(Transform(con_label, con_label_2))
        self.wait(1)

        p_t = MathTex(r"mv", color=BLACK).move_to(table.get_cell((2, 2)).get_center())
        E_t = MathTex(r"\frac{1}{2}mv^2", color=BLACK).move_to(table.get_cell((3, 2)).get_center())
        p_w = MathTex(r"\frac{h}{\lambda}", color=BLACK).move_to(table.get_cell((2, 3)).get_center())
        table_0 = VGroup(table, p_t, E_t, p_w)
        table_0.shift(RIGHT*16)
        self.add(table_0)
        self.play(table_0.animate.shift(LEFT*16))

        p_w_2 = MathTex(r"\frac{h}{\lambda}" "=", r"i\frac{h}{2L}", color=BLACK).move_to(table.get_cell((2, 3)).get_center())
        p_w_3 = MathTex(r"i\frac{h}{2L}", color=BLACK).move_to(table.get_cell((2, 3)).get_center())
        self.play(Transform(p_w, p_w_2))
        self.wait(1)
        self.play(Transform(p_w, p_w_3))
        self.wait(1)
        v = MathTex(r"mv=i\frac{h}{2L}", color=BLACK).move_to(table.get_cell((1, 1)).get_center())
        v_2 = MathTex(r"v=i\frac{h}{2mL}", color=BLACK).move_to(table.get_cell((1, 1)).get_center())
        self.play(con_label.animate.shift(UP*4))
        self.play(Write(v))
        self.wait(1)
        self.play(Transform(v, v_2))
        self.wait(1)
        E_t_2 = MathTex(r"\frac{1}{2}mv^2", "=", r"i^2 \frac{h^2}{8mL^2}", color=BLACK).move_to(table.get_cell((3, 2)).get_center())
        self.play(Transform(E_t, E_t_2))
        self.wait(1)
        self.play(E_t[0].animate.move_to(table.get_cell((3, 2)).get_center()), FadeOut(E_t[1]), E_t[2].animate.move_to(table.get_cell((3, 3)).get_center()))
        self.wait(2)

        highlight(p_w)
        self.wait(1)
        highlight(v)
        self.wait(1)
        highlight(E_t[2])
        self.wait(1)

class Potentialtopf2(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        def highlight(text):
            o_color = text.get_color()
            self.play(text.animate.set_color(RED))
            self.wait(0.25)
            self.play(text.animate.set_color(BLACK))
            self.wait(1)
        def highlight_arr(text, c = BLACK):
            arr = VGroup()
            for t in text:
                arr.add(t)
            self.play(arr.animate.set_color(RED))
            self.wait(0.25)
            self.play(arr.animate.set_color(c))
            self.wait(1)
        self.camera.background_color = WHITE
        axes = Axes(
            x_range=(-8, 8, 1),
            y_range=(-2, 5, 1),
            x_length=17,
            y_length=8,
            axis_config={"include_numbers": True, "color": BLACK, "decimal_number_config": {"num_decimal_places": 0}},
        )
        for label in axes.get_x_axis().numbers + axes.get_y_axis().numbers:
            label.set_color(BLACK)
        L=4
        width=0.5
        height=4.5
        topf = Polygon(
            axes.c2p(L/2, height),
            axes.c2p(L/2+width, height),
            axes.c2p(L/2+width, -1),
            axes.c2p(-L/2-width, -1),
            axes.c2p(-L/2-width, height),
            axes.c2p(-L/2, height),
            axes.c2p(-L/2, -0.5),
            axes.c2p(L/2, -0.5),
            color=GRAY, fill_opacity=0.5
        )
        outline = VGroup(
            Line(axes.c2p(-L/2, height), axes.c2p(-L/2, -0.5), color=BLACK),
            Line(axes.c2p(L/2, height), axes.c2p(L/2, -0.5), color=BLACK),
            Line(axes.c2p(-L/2, -0.5), axes.c2p(L/2, -0.5), color=BLACK)
        )

        L_label = MathTex("L", color=BLACK).move_to(axes.c2p(0, -1.5))
        L_arrows = VGroup(
            Arrow(axes.c2p(0.5, -1.5), axes.c2p(L/2, -1.5), buff=0, color=BLACK),
            Arrow(axes.c2p(-0.5, -1.5), axes.c2p(-L/2, -1.5), buff=0, color=BLACK)
        )
        dotted_lines = VGroup(
            DashedLine(axes.c2p(-L/2, -1.75), axes.c2p(-L/2, -0.5), color=BLACK),
            DashedLine(axes.c2p(L/2, -1.75), axes.c2p(L/2, -0.5), color=BLACK)
        )
        Energy_arrow = Arrow(axes.c2p(L/2+width/2, height), axes.c2p(L/2+width/2, height+0.5), buff=0, color=BLACK)
        Energy_label = Tex("Energie", color=BLACK).next_to(axes.c2p(L/2+width/2, height+0.5-0.25), RIGHT, buff=0.25)
        Topf = VGroup(topf, outline, L_label, L_arrows, dotted_lines, Energy_arrow, Energy_label)
        Topf.shift(LEFT*16)
        self.add(Topf)
        self.play(Topf.animate.shift(RIGHT*16))

        lines = [Line(axes.c2p(-L/2, 0.6*i), axes.c2p(L/2, 0.6*i), color=GRAY) for i in range(0,6)]
        lines.remove(lines[3])
        
        between = MathTex(r". . .").move_to(axes.c2p(0, 0.6*3)).set_color(BLACK)

        dots = [[
            Dot(radius=0.1, color=BLACK).move_to(axes.c2p(-L/6, 0.6*i)),
            Dot(radius=0.1, color=BLACK).move_to(axes.c2p(+L/6, 0.6*i))
        ] for i in range(0, 5)]
        dots.remove(dots[3])
        
        labels = [MathTex(r"E_1", color=BLACK), MathTex(r"E_2", color=BLACK), MathTex(r"E_3", color=BLACK), MathTex(r"E_F=E_{N/2}", color=BLACK)]
        for i in range(0,4):
            labels[i].next_to(lines[i], RIGHT, buff=1)

        
        for i in range(0,3):
            self.play(Create(lines[i]), run_time=0.25)
        self.play(Write(between), run_time=0.25)
        for i in range(3,5):
            self.play(Create(lines[i]), run_time=0.25)
        self.wait(1)
        for i in range(0,3):
            self.play(Write(labels[i]), run_time=0.25)
        self.wait(1)
        for i in range(0, 4):
            self.play(FadeIn(dots[i][0]), run_time=0.25)
            self.play(FadeIn(dots[i][1]), run_time=0.25)
        self.wait(1)

        d_1 = MathTex(r"N \; \text{Elektronen}", color=BLACK).next_to(lines[3], LEFT, buff=1).to_edge(LEFT)
        d_2 = MathTex(
            r"\begin{aligned}"
            r"&N/2\\"
            r"&\text{Energieniveaus}"
            r"\end{aligned}"
        , color=BLACK).next_to(lines[1], LEFT, buff=1).to_edge(LEFT)


        self.play(Write(d_1))
        highlight_arr([item for sublist in dots for item in sublist])
        self.wait(1)
        self.play(Write(d_2))
        for i in range(len(lines)):
            lines[i].set_z_index(-1)
        highlight_arr(lines[0:4], GRAY)
        self.wait(1)

        E_N2 = MathTex(r"E_{N/2}", color=BLACK).next_to(lines[3], RIGHT, buff=1)
        self.play(Write(E_N2), run_time=0.5)
        self.wait(1)
        self.play(Transform(E_N2, labels[3]))
        self.wait(1)

#Kein Strom & Potdiff
class keinStrom(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        Draht_rect = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(-PI/4, about_point=ORIGIN)
        self.add(Draht_rect)
        Draht_rect.rotate(-PI/4, about_point=ORIGIN)
        Draht_upper = Line(LEFT*3*np.sqrt(2) + UP*0.1, RIGHT*3*np.sqrt(2) + UP*0.1, color=BLACK)
        Draht_lower = Line(LEFT*3*np.sqrt(2) - UP*0.1, RIGHT*3*np.sqrt(2) - UP*0.1, color=BLACK)
        Draht = VGroup(Draht_rect, Draht_upper, Draht_lower)
        self.add(Draht_upper)
        self.add(Draht_lower)
        Draht.scale([1.4, 30, 1])
        wire_length = 42*np.sqrt(2)/5

        White_hider = VGroup(
            Rectangle(width=3, height=8, color=WHITE).set_fill(color=WHITE, opacity=1).next_to(Draht, LEFT, buff=0),
            Rectangle(width=3, height=8, color=WHITE).set_fill(color=WHITE, opacity=1).next_to(Draht, RIGHT, buff=0)
        )
        White_hider.set_z_index(10)
        self.add(White_hider)

        electron_positions = [
            LEFT * 5 + UP * (1+0.25),
            LEFT * 2 + DOWN * (2-0.25),
            ORIGIN + UP * 0.25,
            RIGHT * 2 + UP * (2+0.25),
            RIGHT * 5 + DOWN * (1-0.25)
        ]
        electrons = VGroup()
        shift = wire_length * LEFT
        num = 20
        for pos in electron_positions:
            electron_balls = [Dot(radius=0.3, color=BLUE).move_to(pos + shift * i) for i in range(num)]
            electron_signs = [MathTex("-", color=WHITE).move_to(electron_balls[i]) for i in range(num)]
            for b, s in zip(electron_balls, electron_signs):
                electron = VGroup(b, s)
                electrons.add(electron)
        self.add(electrons)
        self.electrons = electrons
        self.electron_positions = electron_positions

        electrons_copy = VGroup()
        for electron in electrons:
            copy_electron = electron.copy()
            pos = electron.get_center()
            new_pos = np.array([-pos[0] + 1.5, pos[1] - 0.25, pos[2]])
            copy_electron.move_to(new_pos)
            electrons_copy.add(copy_electron)
        self.add(electrons_copy)
        self.electrons_copy = electrons_copy

        Draht.shift(DOWN * 0.8)
        electrons.shift(DOWN * 0.8)
        electrons_copy.shift(DOWN * 0.8)
        self.wait(1)

        U = 0
        I = 0
        UI_label = MathTex(
            f"U={U} V,\\;I={I} A"
        ).to_edge(UP).set_color(BLACK).set_z_index(11)
        self.play(Write(UI_label))

        electrons.add_updater(
            lambda electrons, dt, i=electrons: electrons.shift(0.5 * dt * RIGHT)
        )
        electrons_copy.add_updater(
            lambda electrons_copy, dt, i=electrons_copy: electrons_copy.shift(0.5 * dt * LEFT)
        )
        self.wait(1)

        self.play(UI_label.animate.align_to(Draht, LEFT))
        self.wait(12)

        final = MathTex(
            r"N_{\rightarrow}", "=", r"N_{\leftarrow}", r"= N/2", r"= i_{F}"
        ).set_color(BLACK).to_edge(UP).shift(RIGHT*2)
        Nleft = final[0].copy()
        Nright = final[2].copy()
        Nhalb = final[3].copy()
        iF = final[4].copy()
        Neq = final[1].copy()
        self.play(Write(Nleft))
        self.play(Write(Nright))

        self.wait(3)

        self.play(Write(Neq))
        self.play(Write(Nhalb))
        self.wait(1)
        self.play(Write(iF))
        self.add(final)
        self.remove(Nleft, Nright, Neq, Nhalb, iF)

        self.wait(5)
        final.set_z_index(11)
        self.play(
            UI_label.animate.shift(LEFT * 10),
            final.animate.to_edge(RIGHT)
        )
        self.play(FadeOut(electrons), FadeOut(electrons_copy), FadeOut(White_hider))
        self.play(FadeOut(Draht))
        
        self.wait(1)


        left_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(-PI/4, about_point=ORIGIN).shift(LEFT * 1)
        right_wire = Rectangle(width=0.2, height=np.sqrt(36+36)).set_stroke(color=BLACK, width=0.5).set_fill(color=GOLD, opacity=1).rotate(PI/4, about_point=ORIGIN).shift(RIGHT * 1)
        
        left_wire.rotate(PI/4, about_point=ORIGIN).move_to([-0.1, left_wire.get_y(), 0]).set_height(6).set(width=0.2)
        right_wire.rotate(-PI/4, about_point=ORIGIN).move_to([0.1, right_wire.get_y(), 0]).set_height(6).set(width=0.2)
        
        
        wire_width = 10
        left_wire.set(width=0.2+wire_width).shift(LEFT * wire_width/2)
        right_wire.set(width=0.2+wire_width).shift(RIGHT * wire_width/2)

        left_wire.shift(DOWN*218)
        right_wire.shift(DOWN*218)
        self.add(right_wire, left_wire)

        nano_num = 7
        nano_width = 2
        atom_radius = 0.12
        atom_radius = nano_width/(2*nano_num)

        atoms = VGroup(*[
            Dot(
                point=LEFT * ((nano_width-2*atom_radius)/(nano_num-1)*i - nano_width/2+atom_radius) + DOWN * 3,
                radius=atom_radius,
                color=GOLD,
            ).set_stroke(color=BLACK, width=0.5)
            for i in range(nano_num)
        ])

        # Length L marker below the atoms
        L_label = MathTex("L", color=BLACK).next_to(atoms, DOWN, buff=0.25)
        L_arrows = VGroup(
            Arrow(L_label.get_left(), L_label.get_left() + LEFT * 0.8, buff=0, color=BLACK),
            Arrow(L_label.get_right(), L_label.get_right() + RIGHT * 0.8, buff=0, color=BLACK),
        )

        atoms.set_z_index(-10)
        L_label.set_z_index(-10)
        L_arrows.set_z_index(-10)
        self.add(atoms, L_label, L_arrows)
        left_wire.shift(LEFT * 1)
        right_wire.shift(RIGHT * 1)

        g = VGroup(atoms, L_label, L_arrows, left_wire, right_wire)
        g.shift(DOWN * 5)
        self.play(g.animate.shift(UP * 5), run_time=2)
        

        unit = 1
        axes = Axes(
            x_range=(0, 10, 1),
            y_range=(0, 6, 1),
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": False, "color": BLACK, "include_ticks": False},
        )
        axes.x_axis.set_opacity(0)
        self.add(axes)
        axes.shift(UP * 1)
        axes_label = MathTex(
            r"\text{Potential}"
        ).set_color(BLACK).move_to(LEFT*3.9).to_edge(UP)
        self.play(Write(axes_label))

        self.wait(1)

        pot_links = Polygon(
            axes.c2p(-5,2),
            axes.c2p(4,2),
            axes.c2p(4,0),
            axes.c2p(-5,0)
        ).set_fill(BLUE, opacity=1).set_stroke(width=0).set_z_index(-1)
        pot_rechts = Polygon(
            axes.c2p(6,2),
            axes.c2p(15,2),
            axes.c2p(15,0),
            axes.c2p(6,0),
        ).set_fill(BLUE, opacity=1).set_stroke(width=0).set_z_index(-1)
        pot_gap = DashedLine(axes.c2p(4,2), axes.c2p(6,2), color=GRAY, stroke_width=2).set_z_index(-1)
        pot_gap2 = DashedLine(axes.c2p(4,3), axes.c2p(6,1), color=GRAY, stroke_width=2).set_z_index(-1)

        label_links = MathTex(
            r"E_{F,links}"
        ).set_color(BLACK).move_to(axes.c2p(1, 2.25))
        label_rechts = MathTex(
            r"E_{F,rechts}"
        ).set_color(BLACK).move_to(axes.c2p(9, 2.25))

        self.play(Create(pot_links))
        self.play(Create(pot_gap))
        self.play(Create(pot_rechts))
        self.wait(1)

        self.play(Write(label_links))
        self.play(Write(label_rechts))

        self.wait(1)
        self.play(FadeOut(final))
        self.wait(1)

        pot_diff = DoubleArrow(axes.c2p(6.25, 1), axes.c2p(6.25, 3), buff=0.02).set_color(BLACK)
        diff_label = MathTex(r"\Delta E", r"=", r"E_{F,l}-E_{F,r}").set_color(BLACK).next_to(pot_diff, RIGHT)
        diff_label2 = MathTex(r"\Delta E", r"=", r"eU", R"E_{F,li}").set_color(BLACK).next_to(pot_diff, RIGHT)

        self.play(
            pot_links.animate.scale([1,1.5,1]).shift(UP*0.5*unit),
            label_links.animate.shift(1 * unit * UP),
            Transform(pot_gap, pot_gap2),
            pot_rechts.animate.scale([1,0.5,1]).shift(DOWN*0.5*unit),
            label_rechts.animate.shift(1 * unit * DOWN)
        )
        self.wait(1)
        jF = MathTex(r"j_{F}").set_color(BLACK).move_to(axes.c2p(3, 3.25)).to_edge(LEFT)
        iF = MathTex(r"i_{F}").set_color(BLACK).move_to(axes.c2p(7, 1.25)).to_edge(RIGHT)
        self.play(Write(jF), Write(iF))


        self.wait(1)
        self.play(
            FadeIn(pot_diff), Write(diff_label[0])
        )
        self.wait(1)
        self.play(Write(diff_label[1]))
        self.play(Write(diff_label[2]))
        self.wait(1)
        self.play(Unwrite(diff_label[2]))
        self.wait(1)
        self.play(Write(diff_label2[2]))
        self.wait(2)

        
        highlight_oben = Polygon(
            axes.c2p(-5,3),
            axes.c2p(4,3),
            axes.c2p(4,1),
            axes.c2p(-5,1)
        ).set_fill(RED, opacity=0.8).set_stroke(width=0).set_z_index(-0.5)
        self.play(FadeIn(highlight_oben))
        self.play(FadeOut(highlight_oben))

        num = 3
        arrows = VGroup(
            *[Arrow(axes.c2p(4,3 - 2*i/(num-1)), axes.c2p(5 - 0.5*i/(num-1),3 - 2*i/(num-1)), buff=0.01, tip_length=0.15, stroke_width=2) for i in range(0, num)]
        ).set_color(BLACK)
        self.play(Create(arrows))
        self.wait(1)

        brace = Brace(
            Line(axes.c2p(4,1), axes.c2p(4,3)), direction=LEFT
        ).set_color(BLACK)
        self.play(Create(brace))
        
        dN_label = MathTex(r"\Delta N").set_color(BLACK).next_to(brace, LEFT)
        self.play(Write(dN_label))
        self.wait(2)

        Ndiff_label = MathTex(r"\Delta N", r"=", r"N_{\rightarrow}-N_{\leftarrow}").set_color(BLACK).to_edge(UR)
        idiff_label = MathTex(r"\Delta N", r"=", r"j_{F}-i_{F}").set_color(BLACK).to_edge(UR).align_to(Ndiff_label, LEFT)
        self.play(Write(Ndiff_label))
        self.wait(2)
        self.play(Transform(Ndiff_label[2], idiff_label[2]))
        self.wait(2)

#Ende
class Rechnung(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        def align_group(group, index=1, d=1.2):
            for i in range(len(group)):
                l_h = group[i][1].get_center()[0] - group[i].get_center()[0]
                l_v = group[i][1].get_center()[1] - group[i].get_center()[1]
                group[i].shift(LEFT*l_h + DOWN*l_v)
                group[i].shift(DOWN * d * i)


        l1 = MathTex(r"eU", r"=", r"E_{F,links}-E_{F,rechts}").set_color(BLACK)
        l2 = MathTex(r"eU", r"=", r"j_{F}^2\frac{h^2}{8mL^2}-i_{F}^2\frac{h^2}{8mL^2}").set_color(BLACK)
        l3 = MathTex(r"eU", r"=", r"\frac{h^2}{8mL^2}(j_{F}^2-i_{F}^2)").set_color(BLACK)
        l4 = MathTex(r"eU", r"=", r"\frac{h^2}{8mL^2}(j_{F}-i_{F})(j_{F}+i_{F})").set_color(BLACK)
        l5 = MathTex(r"eU", r"=", r"\frac{h^2}{8mL^2}\Delta N(j_{F}+i_{F})").set_color(BLACK)
        l6 = MathTex(r"eU", r"=", r"\frac{h}{4}\frac{\Delta N}{L}\frac{h}{2mL}(j_{F}+i_{F})").set_color(BLACK)
        l7 = MathTex(r"eU", r"=", r"\frac{h}{4}\frac{\Delta N}{L}(v_{j}+v_{i})").set_color(BLACK)
        l8 = MathTex(r"eU", r"=", r"\frac{h}{2}\frac{\Delta N}{L}\bar{v}").set_color(BLACK)
        l9 = MathTex(r"eU", r"=", r"\frac{h}{2}n\bar{v}").set_color(BLACK)
        l10 = MathTex(r"eU", r"=", r"\frac{h}{2e}ne\bar{v}").set_color(BLACK)
        l11 = MathTex(r"eU", r"=", r"\frac{h}{2e}I").set_color(BLACK)
        l12 = MathTex(r"\frac{U}{I}", r"=", r"\frac{h}{2e^2}").set_color(BLACK)
        lines = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12]
        align_group(lines, index=1, d=0)

        self.play(Write(l1))
        for line in lines[1:]:
            self.play(Transform(l1, line))
        self.wait(1)
        
        R = MathTex(
            r"R", r"=", r"\frac{U}{I}", r"=", r"\frac{h}{2e^2}", r"\approx", r"12,9\,\mathrm{k\Omega}"
        ).set_color(BLACK).move_to(DOWN*2)
        self.play(Write(R[0]))
        self.play(Write(R[1:3]))
        self.play(Write(R[3:5]))
        self.play(Write(R[5:]))
        self.wait(1)

        self.play(l1.animate.shift(UP*10), R.animate.shift(UP*2))
        self.wait(1)

        G = MathTex(
            r"G", r"=", r"\frac{1}{R}", r"=", r"\frac{2e^2}{h}", r"\approx", r"77,5\,\mathrm{\mu S}"
        ).set_color(BLACK).move_to(DOWN*2)
        G1 = MathTex(
            r"G", r"=", r"\frac{2e^2}{h}"
        ).set_color(BLACK).move_to(UP*2)
        G2 = MathTex(
            r"G", r"=", r"2\frac{2e^2}{h}"
        ).set_color(BLACK)
        G100 = MathTex(
            r"G", r"=", r"100\frac{2e^2}{h}"
        ).set_color(BLACK)
        Gn = MathTex(
            r"G", r"=", r"n\frac{2e^2}{h}"
        ).set_color(BLACK)

        self.play(Write(G[0]))
        self.play(Write(G[1:3]))
        self.play(Write(G[3:5]))
        self.play(Write(G[5:]))
        self.wait(1)

        self.play(R.animate.shift(UP*10), G.animate.shift(UP*4))
        self.play(Transform(G, G1))

        d2 = MathTex(r"\text{2 Drähte:}", color=BLACK).to_edge(LEFT)
        d100 = MathTex(r"\text{100 Drähte:}", color=BLACK).to_edge(LEFT)
        dn = MathTex(r"\text{n Drähte:}", color=BLACK).to_edge(LEFT)

        self.play(Write(d2))
        self.play(Write(G2))
        self.wait(1)
        self.play(Transform(d2, d100), Transform(G2, G100))
        self.wait(1)
        self.play(Transform(d2, dn), Transform(G2, Gn), FadeOut(G))
        self.wait(1)

#Messung
class Messung(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        board = RoundedRectangle(
            corner_radius=0.5,
            width = 7,
            height = 5.5,
            fill_color=GRAY,
            fill_opacity=1,
            stroke_width=0
        ).shift(UP * 0.25)
        self.add(board)

        top_left = LEFT * 3 + UP * 1.5
        top_right = RIGHT * 3 + UP * 1.5
        bottom_left = LEFT * 3 + DOWN * 1.5
        bottom_right = RIGHT * 3 + DOWN * 1.5
        source = Circle(radius=0.4, color=BLACK).move_to(DOWN * 1.5)
        U_source = MathTex(r"U_{ein}", color=BLACK).move_to(DOWN * 2.2)
        R_cross = MathTex(r"R_{nano}", color=BLACK).move_to(UP*1.8)
        self.add(R_cross)
        plus = MathTex("+", color=BLACK).next_to(source, DOWN + RIGHT, buff=0.1)
        minus = MathTex("-", color=BLACK).next_to(source, DOWN + LEFT, buff=0.1)
        minus.set_y(plus.get_y())
        bottom_left_line = Line(bottom_left, source.get_left(), color=BLACK)
        bottom_right_line = Line(source.get_right(), bottom_right, color=BLACK)
        left_wire = Line(bottom_left, top_left, color=BLACK)
        right_wire = Line(bottom_right, top_right, color=BLACK)
        top_cross1 = Line(top_left, RIGHT * 0.2 + UP * 2.5, color=GOLD)
        top_cross2 = Line(top_right, LEFT * 0.2 + UP * 2.5, color=GOLD)
        circuit = VGroup(
            bottom_left_line,
            bottom_right_line,
            left_wire,
            right_wire,
            top_cross1,
            top_cross2,
            source,
            U_source,
            plus,
            minus,
        )
        self.play(Create(circuit))

        ampere_meter = VGroup(
            Circle(radius=0.4, color=BLACK).move_to(RIGHT*3),
            MathTex("A", color=BLACK).move_to(RIGHT*3)
        )
        right_upper_wire = Line(top_right, RIGHT*3+UP*0.4, color=BLACK)
        right_lower_wire = Line(bottom_right, RIGHT*3+DOWN*0.4, color=BLACK)
        Resistor = Rectangle(width=0.6, height=0.8).move_to(RIGHT*3).set_color(BLACK)
        R_Resistor = MathTex(r"R_1", color=BLACK).move_to(RIGHT*3)
        right_con_1 = Line(RIGHT*3+UP*1, RIGHT*5+UP*1, color=BLACK)
        right_con_2 = Line(RIGHT*5+UP*1, RIGHT*5+UP*0.4, color=BLACK)
        right_con_3 = Line(RIGHT*5+DOWN*0.4, RIGHT*5+DOWN*1, color=BLACK)
        right_con_4 = Line(RIGHT*5+DOWN*1, RIGHT*3+DOWN*1, color=BLACK)
        extra_wires = VGroup(right_con_1, right_con_2, right_con_3, right_con_4)
        volt_meter = VGroup(
            Circle(radius=0.4, color=BLACK).move_to(RIGHT*5),
            MathTex(r"V", color=BLACK).move_to(RIGHT*5),
            MathTex(r"U_{aus}", color=BLACK).move_to(RIGHT*6.2).align_to(R_Resistor, UP)
        )
        new_board = RoundedRectangle(
            corner_radius=0.5,
            width = 7,
            height = 5.5,
            fill_color=GRAY,
            fill_opacity=1,
            stroke_width=0
        ).set_z_index(-10).shift(UP * 0.25)
        self.add(new_board)

        self.play(Write(ampere_meter), FadeOut(right_wire), FadeIn(right_upper_wire), FadeIn(right_lower_wire))
        self.wait(2)
        self.play(FadeOut(ampere_meter), FadeIn(Resistor), FadeIn(R_Resistor))
        self.wait(0.5)
        self.play(new_board.animate.shift(RIGHT*2))
        self.wait(0.5)
        self.play(FadeIn(extra_wires), Write(volt_meter))
        self.wait(1)

class Ende(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        self.wait(1)
        d = 6
        dim = MathTex(r"\text{Nicht eindimensionaler Draht}", color=BLACK, font_size=64)
        chem = MathTex(r"\text{Chemisches Potential}", color=BLACK, font_size=64).move_to(DOWN*d)
        elek = MathTex(r"\text{Elektronenkonfiguration}", color=BLACK, font_size=64).move_to(DOWN*2*d)
        tunn = MathTex(r"\text{Tunneleffekt}", color=BLACK, font_size=64).move_to(DOWN*3*d)
        end = MathTex(r"\text{Jetzt seid ihr an der Reihe!}", color=BLACK, font_size=64).move_to(DOWN*4*d)

        self.play(Write(dim))
        self.add(chem, elek, tunn, end)
        self.wait(2)
        g = VGroup(dim, chem, elek, tunn, end)
        self.play(g.animate.shift(UP*d))
        self.wait(1)
        temp = MathTex(r"\rightarrow", r"\text{Temperaturabhängig}", color=BLACK, font_size=64).next_to(chem, DOWN, buff=0.5).align_to(chem, LEFT)
        self.play(Write(temp))
        g.add(temp)
        self.wait(2)
        self.play(g.animate.shift(UP*d))
        self.wait(2)
        self.play(g.animate.shift(UP*d))
        self.wait(2)
        self.play(g.animate.shift(UP*d))
        self.wait(2)


#alt
class Schaltkreis(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        axes = Axes(
            x_range=[-40, 40, 1],
            y_range=[-20, 20, 1],
            x_length=14,
            y_length=8,
            axis_config={"color": BLACK},
            tips=False
        )
        comp_color = RED_C
        
        conductor = VGroup(
            Line(axes.c2p(-36,12), axes.c2p(-36,-14), color=BLACK),
            Line(axes.c2p(-36,-4), axes.c2p(-30,-4), color=BLACK),
            Line(axes.c2p(-26,-4), axes.c2p(-12,-4), color=BLACK),
            Line(axes.c2p(-28,-3), axes.c2p(-28,3), color=BLACK),
            Line(axes.c2p(-36,12), axes.c2p(-12,12), color=BLACK),
            Line(axes.c2p(-28,3), axes.c2p(-16,3), color=BLACK),
            Line(axes.c2p(-36,-14), axes.c2p(0,-14), color=BLACK),
            Line(axes.c2p(-12,-10), axes.c2p(0,-10), color=BLACK),
            Line(axes.c2p(-12,3), axes.c2p(-12,-10), color=BLACK),
            Line(axes.c2p(-22,14), axes.c2p(-22,7), color=BLACK),
            Line(axes.c2p(-22,7), axes.c2p(-16,7), color=BLACK),
            Line(axes.c2p(-22,14), axes.c2p(-4,14), color=BLACK),
            Line(axes.c2p(-12,12), axes.c2p(-12,7), color=BLACK),
            Line(axes.c2p(-4,14), axes.c2p(-4,5), color=BLACK),
            Line(axes.c2p(-8,5), axes.c2p(0,5), color=BLACK),

            
            Line(axes.c2p(10,5), axes.c2p(18,5), color=BLACK),
            Line(axes.c2p(14,14), axes.c2p(14,5), color=BLACK),
            Line(axes.c2p(14,14), axes.c2p(20,14), color=BLACK),
            Line(axes.c2p(24,14), axes.c2p(30,14), color=BLACK),
            Line(axes.c2p(30,14), axes.c2p(30,3), color=BLACK),
            Line(axes.c2p(2,-10), axes.c2p(4,-10), color=BLACK),
            Line(axes.c2p(2,-14), axes.c2p(4,-14), color=BLACK),
            Line(axes.c2p(4,-10), axes.c2p(4,-14), color=BLACK),
            Line(axes.c2p(4,-12), axes.c2p(14,-12), color=BLACK),
            Line(axes.c2p(14,-12), axes.c2p(14,1), color=BLACK),
            Line(axes.c2p(14,1), axes.c2p(18,1), color=BLACK),
            Line(axes.c2p(26,3), axes.c2p(34,3), color=BLACK),
            Line(axes.c2p(14,-6), axes.c2p(34,-6), color=BLACK),
        )

        connectors = VGroup(
            Dot(axes.c2p(-36,-4), radius=0.075, color=comp_color),
            Dot(axes.c2p(-12,-4), radius=0.075, color=comp_color),
            Dot(axes.c2p(-4,5),   radius=0.075, color=comp_color),
            Dot(axes.c2p(4,-12),  radius=0.075, color=comp_color),
            Dot(axes.c2p(14,-6),  radius=0.075, color=comp_color),
            Dot(axes.c2p(14,5),   radius=0.075, color=comp_color),
            Dot(axes.c2p(30,3),   radius=0.075, color=comp_color)
        )

        connections = VGroup(
            Dot(axes.c2p(1,5), radius=0.175, color=comp_color),
            Dot(axes.c2p(9,5), radius=0.175, color=comp_color),
            Dot(axes.c2p(35,3), radius=0.175, color=comp_color),
            Dot(axes.c2p(35,-6), radius=0.175, color=comp_color),

            Text("Draht 1", color=BLACK, font_size=24, font="MERRYWEATHER SANS").move_to(axes.c2p(1,7.5)),
            Text("Draht 2", color=BLACK, font_size=24, font="MERRYWEATHER SANS").move_to(axes.c2p(9,7.5)),
            Text("OUT", color=BLACK, font_size=24, font="MERRYWEATHER SANS").move_to(axes.c2p(35,5.5)),
            Text("GND", color=BLACK, font_size=24, font="MERRYWEATHER SANS").move_to(axes.c2p(35,-3.5)),
        )
        
        resistor_rect = Polygon(
            axes.c2p(20,15),
            axes.c2p(24,15),
            axes.c2p(24,13),
            axes.c2p(20,13)
        ).set_color(comp_color)
        resistor_ohm = Text("10k", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(22,16))
        resistor_label = Text("R2", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(22,17.5))
        Resistor = VGroup(resistor_rect, resistor_ohm, resistor_label)

        poti_rect = Polygon(
            axes.c2p(-30,-3),
            axes.c2p(-26,-3),
            axes.c2p(-26,-5),
            axes.c2p(-30,-5)
        ).set_color(comp_color)
        poti_arrow = Arrow(axes.c2p(-28,1), axes.c2p(-28,-4.4), color=comp_color, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=10)
        poti_label = Text("Poti", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(-28,-6))
        Poti = VGroup(poti_rect, poti_arrow, poti_label)


        OPA1_tri = Polygon(
            axes.c2p(-16,9),
            axes.c2p(-8,5),
            axes.c2p(-16,1),
        ).set_color(comp_color)
        OPA1_label = Text("OPA1", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(-12,5))
        OPA1_minus = Text("-", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(-15,7))
        OPA1_plus = Text("+", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(-15,3))
        OPA1 = VGroup(OPA1_tri, OPA1_label, OPA1_minus, OPA1_plus)

        OPA2_tri = Polygon(
            axes.c2p(18,7),
            axes.c2p(26,3),
            axes.c2p(18,-1),
        ).set_color(comp_color)
        OPA2_label = Text("OPA2", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(22,3))
        OPA2_minus = Text("-", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(19,5))
        OPA2_plus = Text("+", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(19,1))
        OPA2 = VGroup(OPA2_tri, OPA2_label, OPA2_minus, OPA2_plus)
        
        bat_lines = VGroup(
            Line(axes.c2p(0,-9), axes.c2p(0,-11)),
            Line(axes.c2p(2/3,-8.5), axes.c2p(2/3,-11.5)),
            Line(axes.c2p(4/3,-9), axes.c2p(4/3,-11)),
            Line(axes.c2p(2,-8.5), axes.c2p(2,-11.5)),

            Line(axes.c2p(0,-12.5), axes.c2p(0,-15.5)),
            Line(axes.c2p(2/3,-13), axes.c2p(2/3,-15)),
            Line(axes.c2p(4/3,-12.5), axes.c2p(4/3,-15.5)),
            Line(axes.c2p(2,-13), axes.c2p(2,-15))
        ).set_color(comp_color)
        bat_label = Text("BAT", color=BLACK, font_size=24, font="MERRIWEATHER SANS").move_to(axes.c2p(1,-7.25))
        bat_signs = VGroup(
            Text("-", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(-1.5,-9)),
            Text("+", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(3.5,-9)),
            Text("+", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(-1.5,-15)),
            Text("-", color=BLACK, font_size=40, font="MERRIWEATHER SANS").move_to(axes.c2p(3.5,-15))
        )
        Bat = VGroup(bat_lines, bat_label, bat_signs)

        
        #self.play(Create(axes))
        self.play(Create(conductor))
        self.play(Create(connectors))
        self.play(Create(connections))
        self.play(Create(Resistor))
        self.play(Create(Poti))
        self.play(Create(OPA1))
        self.play(Create(OPA2))
        self.play(Create(Bat))
        self.wait()
        
class Atom(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        radii = [1, 2, 4]
        p_positions = [
            0.2*LEFT+0.2*UP,
            0.2*RIGHT+0.2*UP,
            ORIGIN,
            0.2*LEFT+0.2*DOWN,
            0.2*RIGHT+0.2*DOWN,
            RIGHT*0.25
        ]
        e_positions = [
            UP*radii[0],
            DOWN*radii[0],
            LEFT*radii[1]/np.sqrt(2)+DOWN*radii[1]/np.sqrt(2),
            RIGHT*radii[1]/np.sqrt(2)+DOWN*radii[1]/np.sqrt(2),
            UP*radii[1],
            UP*radii[2]*np.sin(np.pi/16)+RIGHT*radii[2]*np.cos(np.pi/16)
        ]
        Kern = Circle(radius=0.5, color=BLACK, fill_color=RED, fill_opacity=1)
        Schalen = [
            Circle(radius=radii[0], color=BLACK),
            Circle(radius=radii[1], color=BLACK),
            Circle(radius=radii[2], color=BLACK)
            ]
        protons = VGroup()
        electrons = VGroup()
        for pos in p_positions:
            protons.add( MathTex("+", color=BLACK).move_to(pos) )
        for pos in e_positions:
            electrons.add(
                VGroup(
                    Circle(radius=0.2, color=BLACK, fill_color=BLUE, fill_opacity=1).move_to(pos),
                    MathTex("-", color=BLACK).move_to(pos)
                )
            )
        Atom = VGroup(Kern, Schalen[0], Schalen[1], Schalen[2], protons, electrons)
        Atom.scale(0.5)
        self.play(
            Create(Kern), Create(Schalen[0]), Create(Schalen[1]), Create(Schalen[2])
        )
        self.play(
            Create(protons)
        )
        self.play(
            Create(electrons),
            run_time = 5
        )

        self.wait(1)
        self.play(Atom.animate.shift(LEFT*4))

        arrow = Arrow(electrons[-1].get_right(), electrons[-1].get_right()+RIGHT*2, color=BLACK)
        self.play(Create(arrow))
        Fermi_E = MathTex(
            r"\text{Fermi-Energie}\ E_{F}"
        ).set_color(BLACK).next_to(arrow, RIGHT)
        Fermi_i = MathTex(
            r"\text{Fermi-Index}\ ", r"i_{F}"
        ).set_color(BLACK).next_to(Fermi_E, DOWN)
        self.play(Write(Fermi_E), Write(Fermi_i))

        self.wait(1)
        self.play(
            FadeOut(Atom, shift=UP * 5),
            FadeOut(arrow, shift=UP * 5),
            Fermi_E.animate.move_to(LEFT*4 + UP*3),
            Fermi_i.animate.move_to(LEFT*4 + UP*2)
        )

        self.wait(1)
        N_Elektronen = MathTex(r"N \ \mathrm{Elektronen}").set_color(BLACK).move_to(LEFT*4)
        implies = MathTex(r"\Downarrow").set_color(BLACK).move_to(DOWN + LEFT*4)
        Spin = MathTex(r"\mathrm{Spin:\ Zwei\ Elektronen\ pro\ Energieniveau}").set_color(BLACK).next_to(implies, RIGHT)
        N_Niveaus = MathTex(r"N/2 \ \mathrm{Energieniveaus}").set_color(BLACK).move_to(DOWN*2 + LEFT*4)
        self.play(Write(N_Elektronen))
        self.play(Write(implies))
        self.play(Write(Spin))
        self.play(Write(N_Niveaus))
        self.wait(1)
        self.play(
            Fermi_i.animate.align_to(Fermi_E, LEFT),
            N_Elektronen.animate.move_to(LEFT*4 + UP).align_to(Fermi_E, LEFT),
            FadeOut(implies),
            FadeOut(Spin),
            N_Niveaus.animate.move_to(LEFT*4).align_to(Fermi_E, LEFT)
        )
        self.wait(1)
        Fermi_i_2 = MathTex(
            r"\text{Fermi-Index}\ ", r"i_{F}", r"=", r"N/2"
        ).set_color(BLACK).move_to(Fermi_i).align_to(Fermi_E, LEFT)
        self.play(Transform(Fermi_i, Fermi_i_2))
